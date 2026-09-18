# Verifying a cross-plane run from its run directory

This file ships with the package `bin/campaign-package` assembles (or with the run directory and
the report on their own). Needs: Python 3 (standard library), `sha256sum`, and the Dogwood binary
built from [github.com/dogwood-policy/dogwood](https://github.com/dogwood-policy/dogwood) at the commit `run.json` names as `dogwood_sha`
(`cargo build --release -p dogwood-cli`; the executable is `target/release/dogwood`). Nothing
else: no network, no access to the authority plane's code.

## The package

    runs/<run id>/            the run directory: run.json, trials.jsonl, t2-provenance.json,
                              pack/ (the assembled pack, its schemas, its rules, its manifest),
                              traces/ (one trace per row), NOTICE, SHA256SUMS; from v0.2.0 also
                              receipts/ (one file per scored row) and registry-used.json
    findings.md               the report
    verify_dogwood_side.py    the reader
    README-verification.md    this file
    pack-source/              the pack SOURCE the report's section e cites: rules/, census/ (the
                              preserved failed encodings, the validator's recorded output on each,
                              the R1 exhibit), fixtures/ (data only)
    PACKS.md                  the pack contract a foreign author writes against
    PACKAGE-SHA256SUMS        over every file above; VERIFY.txt is the reader's transcript when
                              the package was proved before it left. The sums are taken over
                              this layout, run at runs/<run id>: a repository that carries the
                              package adds README.md and PROVENANCE.md and regenerates the sums
                              over everything but itself and VERIFY.txt

## Run

    sha256sum -c PACKAGE-SHA256SUMS
    ./verify_dogwood_side.py runs/<run id> --dogwood /path/to/dogwood --pack-source pack-source

Last line `VERIFY DOGWOOD SIDE: PASS`, or `FAIL <n> finding(s)` with each finding named by row,
or `REFUSED <why>`. In one sentence: every trace is replayed with the binary against the pack and
must give the verdicts the record carries; the digests, the deny-provenance classes and the counts
are recomputed; every rejected encoding in the census is run through the validator and must fail
with the recorded words; the R1 exhibit is replayed under its own pack; the Requisition side (the
plane's refusals) is the plane's own record and is read, not re-run. What is re-derived and what is
not is listed in the script's own header.

## The three-way split, in one paragraph

A claim in the report rests on one of three kinds of evidence, and this package lets you check
two of them. **The Dogwood half is re-derivable**: every trace is replayed through the public
binary and must give the recorded verdicts (steps 1–6 of the reader). **The Requisition half is
signed**: from v0.2.0 on, each scored row ships the receipt chain the plane signed for its subject
event under a key whose public half is in the published HolyTrinity-Benchmark registry, and the
reader's step 7 checks registry → signature → chain → the signed status and refusal code against
`trials.jsonl` — so the allow/deny and the code are what *this plane signed*, hash-chained,
inspectable. **The Requisition half is not re-executable**: the plane's code is not here, so
whether it *should* have refused is the report's argument and the pre-registration, not something
a reader can run. The receipts prove provenance, not correctness.

## Run all three checks

    sha256sum -c PACKAGE-SHA256SUMS                                             # 1. the checksums
    ./verify_dogwood_side.py runs/<run id> --dogwood /path/to/dogwood --pack-source pack-source \
        --verifier /path/to/verify_receipt.py --registry /path/to/evaluation-registry.json
                                                                                 # 2. the Dogwood reader (steps 1-6)
                                                                                 # 3. the receipt reader (step 7)

`verify_receipt.py` and `evaluation-registry.json` come from
[HolyTrinity-Benchmark](https://github.com/ScriptKittyOS/HolyTrinity-Benchmark)
(`receipt-verification/verifier/`, `receipt-verification/keys/`), obtained separately from this
package: a registry that arrived with the evidence proves nothing. `registry-used.json` in the run
directory names the key id, its public key and the registry commit the run was checked against;
step 7 requires the registry you supply to say the same. A run without `receipts/` (v0.1.0) is read
by steps 1–6 alone and the reader says so.

**Epochs.** The campaign pins its clock; every instant in a trace is the epoch plus the row's
offset. v0.1.0 (`2026-09-17-49489219`) used epoch `2026-01-01T00:00:00Z`. From v0.2.0 the epoch is
`2026-09-06T00:00:00Z`, the earliest midnight inside the evaluation key's signing window, so the
receipts fall inside it; offsets, windows and verdicts are unchanged.

## Which citations in the report resolve here

Every claim in `findings.md` is followed by its source in brackets.

- `run.json`, `trials.jsonl`, `t2-provenance.json`, `traces/...`, `pack/...`, a trial id such as
  `T1-F5-kill-switch-001`: in the run directory. The reader checks these.
- `test/support/campaigns/dogwood/pack/...` (rules, census, fixtures): in `pack-source/` under the
  same relative path. The reader checks `census/`; `fixtures/` are Elixir-rendered traces
  (`trace.exs`) that need the campaign harness to render and are shipped as data only.
- `docs/...`, `test/support/campaigns/dogwood/*.ex`, `ops/...`, `artifacts/...-qualification/`,
  `artifacts/...-reproduction/`, G-ids and D-ids, and "spec section N": the authority plane's
  private tree (its gaps register, its slice records, its harness code, the qualification of the
  tree the run was taken on, the fresh-clone reproduction). These are not in the package and
  cannot be resolved outside it. The report's Requisition-side statements rest on them; its
  Dogwood-side statements rest on the run directory alone.
- The one URL (NIST SP 800-207) is the published document; its sha256 is in the report.

## Record

Two builds of the pinned commit have been run against `2026-09-17-49489219`: the campaign's
workspace build (sha256 `0fb979e9…`) and a fresh `cargo build` from a clone (`42b4786a…`); both
PASS (`verify_dogwood_side.txt`, `verify_dogwood_side-from-source.txt` in the slice folder
`docs/slices/requisition/REQ-141-dogwood-run-cannot-fail-but-on-merit/`). With `--pack-source`
the reader makes 317 checks; without it, 296. A second deliverable taken on the tree at
`cd5f7df2` (the REQ-141 series, the qualification's suite runs stubbed) differed from
`49489219`'s `trials.jsonl` in `tree_sha` only: every measured value the same.
