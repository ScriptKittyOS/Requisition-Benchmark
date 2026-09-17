#!/usr/bin/env python3
"""VERIFY THE DOGWOOD SIDE OF A CROSS-PLANE RUN FROM ITS RUN DIRECTORY ALONE.

    verify_dogwood_side.py RUN_DIR --dogwood PATH/TO/dogwood

For a reader who holds the run directory (run.json, trials.jsonl, t2-provenance.json, pack/,
traces/, SHA256SUMS) and the Dogwood binary, and nothing else. Python 3 standard library only;
no network; nothing from the tree that produced the run.

The binary: build github.com/dogwood-policy/dogwood at the commit run.json names as
`dogwood_sha` (`cargo build --release -p dogwood-cli`; the executable is target/release/dogwood).
The commit is printed first; this script cannot read a commit out of a binary and says so.

What is re-derived (every value read from the records, never typed here):
  1. SHA256SUMS verifies; pack/manifest.json's digests equal the digests of pack.dw, the two
     schemas and every rule file; run.json's pack_sha256 and dogwood_sha equal the manifest's.
  2. Every trace in trials.jsonl is REPLAYED with the binary against the pack (the same command
     line the campaign used: `dogwood replay pack.dw --policy-schema ... --event-schema ...
     --trace ... --format json`) and the verdict vector -- index, timestamp, verdict, the
     determining rules named through the manifest's index-to-id table (sorted), the errors --
     must equal the record's `dogwood.verdicts`; the exit code must equal `dogwood.exit_code`;
     the subject's verdict must equal `dogwood.verdict`.
  3. `dogwood.undeclared_lines` (trace lines whose action the Cedar schema does not declare, or
     is not qualified with the schema's namespace; the binary is silent about them) is
     re-derived from the trace text and the schema.
  4. `dogwood.deny_provenance` is re-derived from the subject verdict: a firing forbid names a
     rule (`forbid_fired`); no rule and no error is `implicit_deny`; a non-empty `errors` is
     `cedar_failed`; an undeclared subject line is `undeclared_deny`; an ALLOW has none.
  5. t2-provenance.json's `dogwood_denied_rows` and `dogwood_deny_provenance` are re-derived
     from the records, and run.json's `agreements` from each row's `agreement`; each row's
     measured Dogwood verdict is compared with its pre-registered `dogwood.expected.verdict`.

  6. With `--pack-source DIR` (the pack SOURCE the report's section e cites, shipped beside the
     run directory as `pack-source/`): every `census/*.dw.rejected` is run through
     `dogwood validate` against the run's two schemas and must fail with exit 2 and the first
     error line the recorded `*.validate.txt` carries (the class-E claims: each inexpressible
     hypothesis ships with its failed encoding and the validator's own words); the R1 exhibit
     (`census/R1_scope_unbound_first_pack/`: the first pack, its schemas, an attacker-authored
     trace) is replayed under ITS OWN pack and schemas and must give its recorded `replay.json`.
     The fixture bundles under `fixtures/` are Elixir-rendered traces (`trace.exs`) that need the
     campaign harness to render; they are not re-run here, and this is said.

What is NOT re-derived, stated: the Requisition side (`requisition.*` on every row, the plane's
refusals and codes) was produced by the authority plane's own code and cannot be re-run from
this directory; this script reads it only to re-add the counts.

The verdict is the last line, always:
  VERIFY DOGWOOD SIDE: PASS                 exit 0
  VERIFY DOGWOOD SIDE: FAIL <n> finding(s)  exit 1   (each finding printed with the row)
  VERIFY DOGWOOD SIDE: REFUSED <why>        exit 2   (a record or the binary is missing)
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

findings = []
checked = 0


def refuse(why):
    print(f"VERIFY DOGWOOD SIDE: REFUSED {why}")
    sys.exit(2)


def check(claim, recorded, derived):
    global checked
    checked += 1
    if recorded != derived:
        findings.append(claim)
        print(f"  FAIL {claim}: recorded={recorded!r} derived={derived!r}")


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


ANSI = re.compile(r"\x1b\[[0-9;]*m")


# the validator's first error line, the way the in-tree check (PackTest P9) reads it: ANSI
# stripped, the first line carrying `×` or `error`, trimmed
ERROR_LINE = re.compile(r"(^|\s)(error|×)(:|\s|$)")


def first_error(text):
    # `error` as a token, not a substring: "OK: validation passed with no errors or warnings."
    # matched the substring and read as an error line (the review of the resumed series, finding 3)
    for line in ANSI.sub("", text).split("\n"):
        if ERROR_LINE.search(line):
            return line.strip()
    return ""


# a verdict vector with its determining rules sorted (the binary emits them in process order)
def canonical_verdicts(verdicts):
    if verdicts is None:
        return None
    return [dict(v, determining_rules=sorted(v.get("determining_rules") or [])) for v in verdicts]


def declared_actions(cedar_text):
    ns = re.search(r"^namespace\s+([A-Za-z_][A-Za-z0-9_:]*)\s*\{", cedar_text, re.M)
    actions = re.findall(r'^\s*action\s+"([A-Za-z0-9_]+)"', cedar_text, re.M)
    return (ns.group(1) if ns else None), set(actions)


def undeclared_lines(trace_text, ns, actions):
    """1-based line numbers the campaign's replayer records: an action the schema does not
    declare, or an Action reference not qualified with the namespace."""
    qualified = re.compile(r'(?<![A-Za-z0-9_:])' + re.escape(ns) + r'::Action::"([A-Za-z0-9_]+)"::(request|response)')
    bare = re.compile(r'(?:[A-Za-z0-9_]+::)*Action::"([A-Za-z0-9_]+)"::(request|response)')
    out = []
    for n, line in enumerate(trace_text.split("\n"), 1):
        if not line.strip():
            continue
        m = qualified.search(line)
        if m:
            if m.group(1) not in actions:
                out.append(n)
            continue
        out.append(n)  # bare, or no action at all
    return out


def provenance(subject, undeclared, subject_line_undeclared):
    if subject is None:
        return None
    if subject["verdict"] == "allow":
        return None
    if subject_line_undeclared:
        return "undeclared_deny"
    if subject["errors"]:
        return "cedar_failed"
    if subject["determining_rules"]:
        return "forbid_fired"
    return "implicit_deny"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--dogwood", required=True, help="the dogwood executable built at run.json's dogwood_sha")
    ap.add_argument("--pack-source", default=None, help="the pack source directory (rules/, fixtures/, census/) the report's section e cites")
    args = ap.parse_args()
    d = os.path.abspath(args.run_dir)
    for f in ("run.json", "trials.jsonl", "t2-provenance.json", "SHA256SUMS", "pack/manifest.json", "pack/pack.dw", "pack/schema.cedarschema", "pack/events.dwschema"):
        if not os.path.isfile(os.path.join(d, f)):
            refuse(f"no {f} under {d}")
    if not (os.path.isfile(args.dogwood) and os.access(args.dogwood, os.X_OK)):
        refuse(f"no executable at {args.dogwood}")
    run = json.load(open(os.path.join(d, "run.json")))
    manifest = json.load(open(os.path.join(d, "pack", "manifest.json")))
    t2 = json.load(open(os.path.join(d, "t2-provenance.json")))
    trials = [json.loads(l) for l in open(os.path.join(d, "trials.jsonl")) if l.strip()]
    print(f"run: {d}")
    print(f"run_id {run.get('run_id')}; tree_sha {run.get('tree_sha')}; status {run.get('status')}; recorded {run.get('recorded')}")
    print(f"dogwood commit to build: {run.get('dogwood_sha')} (this script cannot read a commit out of the binary; the reader builds it)")
    try:
        ver = subprocess.run([args.dogwood, "--version"], capture_output=True, text=True, timeout=30)
        print(f"binary: {args.dogwood} sha256 {sha256(args.dogwood)}; --version: {(ver.stdout or ver.stderr).strip()}")
    except Exception as e:  # noqa: BLE001
        refuse(f"the binary did not answer --version ({e})")

    # ---- 1. the records' integrity ----------------------------------------------------------
    print("== 1. digests ==")
    rc = subprocess.run(["sha256sum", "-c", "--quiet", "SHA256SUMS"], cwd=d, capture_output=True, text=True)
    check("SHA256SUMS verifies", 0, rc.returncode)
    if rc.returncode != 0:
        print("  " + rc.stdout.strip().replace("\n", "\n  "))
    check("manifest pack_sha256 == sha256(pack/pack.dw)", manifest.get("pack_sha256"), sha256(os.path.join(d, "pack", "pack.dw")))
    check("manifest cedar_schema_sha256", manifest.get("cedar_schema_sha256"), sha256(os.path.join(d, "pack", "schema.cedarschema")))
    check("manifest dwschema_sha256", manifest.get("dwschema_sha256"), sha256(os.path.join(d, "pack", "events.dwschema")))
    for r in manifest.get("rules", []):
        p = os.path.join(d, "pack", r["source"])
        check(f"manifest rule {r['index']} ({r['id']}) sha256", r.get("sha256"), sha256(p) if os.path.isfile(p) else None)
    check("run.json pack_sha256 == manifest", run.get("pack_sha256"), manifest.get("pack_sha256"))
    check("run.json dogwood_sha == manifest", run.get("dogwood_sha"), manifest.get("dogwood_sha"))
    check("run.json recorded == trials.jsonl lines", run.get("recorded"), len(trials))
    id_for = {r["index"]: r["id"] for r in manifest.get("rules", [])}
    ns, actions = declared_actions(open(os.path.join(d, "pack", "schema.cedarschema")).read())
    if not ns or not actions:
        refuse("the Cedar schema names no namespace or no actions")
    print(f"  namespace {ns}; declared actions {sorted(actions)}; rules {[id_for[i] for i in sorted(id_for)]}")

    # ---- 2-4. every trace replayed ----------------------------------------------------------
    print("== 2. replay ==")
    derived_rows = []
    for t in trials:
        tid = t["trial_id"]
        dw = t["dogwood"]
        trace = os.path.join(d, dw["trace_ref"]) if dw.get("trace_ref") else None
        if not trace or not os.path.isfile(trace):
            check(f"{tid}: trace file present", True, False)
            derived_rows.append((tid, None, None))
            continue
        cmd = [args.dogwood, "replay", os.path.join(d, "pack", "pack.dw"),
               "--policy-schema", os.path.join(d, "pack", "schema.cedarschema"),
               "--event-schema", os.path.join(d, "pack", "events.dwschema"),
               "--trace", trace, "--format", "json"]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        out = p.stdout + p.stderr
        check(f"{tid}: exit code", dw.get("exit_code"), p.returncode)
        verdicts = None
        if p.returncode == 0:
            try:
                raw = json.loads(p.stdout)["verdicts"]
            except Exception:  # noqa: BLE001
                check(f"{tid}: replay output parses", True, False)
                raw = []
            verdicts = []
            for v in raw:
                names = []
                for i in v.get("determining_rules", []) or []:
                    if i not in id_for:
                        check(f"{tid}: rule index {i} is in the manifest", True, False)
                    names.append(id_for.get(i, f"<index {i}>"))
                verdicts.append({
                    "determining_rules": sorted(names),
                    "errors": v.get("errors", []) or [],
                    "index": v.get("index"),
                    "timestamp": v.get("timestamp"),
                    "verdict": v.get("verdict"),
                })
            check(f"{tid}: verdict vector", dw.get("verdicts"), verdicts)
        text = open(trace).read()
        und = undeclared_lines(text, ns, actions)
        check(f"{tid}: undeclared_lines", dw.get("undeclared_lines"), und)
        si = dw.get("subject_index")
        subject = verdicts[si] if verdicts is not None and si is not None and si < len(verdicts) else None
        subj_verdict = subject["verdict"].upper() if subject else None
        check(f"{tid}: subject verdict", dw.get("verdict"), subj_verdict)
        # the subject line: the decision line the subject verdict judged is the (si+1)-th
        # `::request` line of the trace; undeclared when its number is in `und`
        request_lines = [n for n, line in enumerate(text.split("\n"), 1) if re.search(r'Action::"[A-Za-z0-9_]+"::request', line)]
        subject_line = request_lines[si] if si is not None and si < len(request_lines) else None
        prov = provenance(subject, und, subject_line in und if subject_line else False)
        check(f"{tid}: deny_provenance", dw.get("deny_provenance"), prov)
        check(f"{tid}: measured verdict vs pre-registered", (dw.get("expected") or {}).get("verdict"), subject["verdict"] if subject else None)
        derived_rows.append((tid, subj_verdict, prov))
        mark = "ok  " if not [f for f in findings if f.startswith(tid + ":")] else "FAIL"
        print(f"  {mark} {tid}: {subj_verdict} {prov or ''} {subject['determining_rules'] if subject else ''}")

    # ---- 5. the populations -----------------------------------------------------------------
    print("== 3. populations ==")
    denied = sum(1 for _, v, _ in derived_rows if v == "DENY")
    check("t2 dogwood_denied_rows", t2.get("dogwood_denied_rows"), denied)
    prov_counts = {}
    for _, v, p in derived_rows:
        if v == "DENY" and p:
            prov_counts[p] = prov_counts.get(p, 0) + 1
    check("t2 dogwood_deny_provenance", t2.get("dogwood_deny_provenance"), prov_counts)
    by_t2 = {r["trial_id"]: r for r in t2.get("by_trial", [])}
    for tid, v, p in derived_rows:
        r = by_t2.get(tid)
        check(f"t2 by_trial {tid} dogwood_verdict", (r or {}).get("dogwood_verdict"), v)
        check(f"t2 by_trial {tid} deny_provenance", (r or {}).get("deny_provenance"), p)
    agreements = {}
    for t in trials:
        agreements[t["agreement"]] = agreements.get(t["agreement"], 0) + 1
    check("run.json agreements == count of each row's agreement", run.get("agreements"), agreements)
    for t in trials:
        check(f"{t['trial_id']}: agreement == expected_agreement", t.get("expected_agreement"), t.get("agreement"))
        check(f"{t['trial_id']}: no halt", None, t.get("halt"))
    print(f"  denied {denied}; provenance {prov_counts}; agreements {agreements}")
    print("  the Requisition side (requisition.* on every row) is the plane's own record and is not re-run here")

    # ---- 6. the pack source: the census and the R1 exhibit (section e of the report) --------
    if args.pack_source:
        print("== 6. pack source: the census's rejected encodings and the R1 exhibit ==")
        src = os.path.abspath(args.pack_source)
        census = os.path.join(src, "census")
        if not os.path.isdir(census):
            refuse(f"no census/ under {src}")
        rejected = sorted(f for f in os.listdir(census) if f.endswith(".dw.rejected"))
        check("census: at least one preserved failed encoding", True, len(rejected) > 0)
        for f in rejected:
            recorded_path = os.path.join(census, f[: -len(".dw.rejected")] + ".validate.txt")
            if not os.path.isfile(recorded_path):
                check(f"census {f}: recorded validate output present", True, False)
                continue
            p = subprocess.run([args.dogwood, "validate", os.path.join(census, f),
                                "--policy-schema", os.path.join(d, "pack", "schema.cedarschema"),
                                "--event-schema", os.path.join(d, "pack", "events.dwschema")],
                               capture_output=True, text=True, timeout=120)
            check(f"census {f}: validate exit (2 = the encoding is refused; 1 would be an IO fault)", 2, p.returncode)
            check(f"census {f}: the validator's first error line is the recorded one",
                  first_error(open(recorded_path).read()), first_error(p.stdout + p.stderr))
        hyps = sorted({f[:2] for f in rejected})
        # the one TYPED list in this script, stated: the campaign's pre-registered inexpressible
        # hypotheses (the spec's section 4, T4), which no file in the run directory names
        for h in ("E2", "E4", "E5", "E6"):
            check(f"census: a preserved attempt for {h}", True, h in hyps)
        r1 = os.path.join(census, "R1_scope_unbound_first_pack")
        # the exhibit the report's section e cites is REQUIRED (finding 8: a source without it
        # read PASS with three checks fewer)
        check("R1 exhibit: census/R1_scope_unbound_first_pack/ present", True, os.path.isdir(r1))
        if os.path.isdir(r1):
            need = ["pack.dw", "schema.cedarschema", "events.dwschema", "spliced.log", "replay.json"]
            missing = [n for n in need if not os.path.isfile(os.path.join(r1, n))]
            check("R1 exhibit: its five files present", [], missing)
            if not missing:
                p = subprocess.run([args.dogwood, "replay", os.path.join(r1, "pack.dw"),
                                    "--policy-schema", os.path.join(r1, "schema.cedarschema"),
                                    "--event-schema", os.path.join(r1, "events.dwschema"),
                                    "--trace", os.path.join(r1, "spliced.log"), "--format", "json"],
                                   capture_output=True, text=True, timeout=120)
                check("R1 exhibit: replay exit", 0, p.returncode)
                try:
                    live = canonical_verdicts(json.loads(p.stdout).get("verdicts"))
                except Exception:  # noqa: BLE001
                    live = None
                recorded = canonical_verdicts(json.load(open(os.path.join(r1, "replay.json"))).get("verdicts"))
                check("R1 exhibit: the first pack replays the spliced trace to its recorded verdicts (allow on rule 0)", recorded, live)
        print("  fixtures/ (Elixir-rendered trace.exs bundles) need the campaign harness to render and are not re-run here")

    print(f"checks: {checked}; findings: {len(findings)}")
    if findings:
        print(f"VERIFY DOGWOOD SIDE: FAIL {len(findings)} finding(s)")
        sys.exit(1)
    print("VERIFY DOGWOOD SIDE: PASS")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001 -- the verdict is the last line, always, never a traceback
        refuse(f"{type(e).__name__}: {e}")
