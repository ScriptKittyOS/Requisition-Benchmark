# Verifying a cross-plane run from its run directory

This file ships with the package `bin/campaign-package` assembles (or with the run directory and
the report on their own). Needs: Python 3 (standard library), `sha256sum`, and the Dogwood binary
built from github.com/dogwood-policy/dogwood at the commit `run.json` names as `dogwood_sha`
(`cargo build --release -p dogwood-cli`; the executable is `target/release/dogwood`). Nothing
else: no network, no access to the authority plane's code.

## The package

    <run id>/                 the run directory: run.json, trials.jsonl, t2-provenance.json,
                              pack/ (the assembled pack, its schemas, its rules, its manifest),
                              traces/ (one trace per row), NOTICE, SHA256SUMS
    findings.md               the report
    verify_dogwood_side.py    the reader
    README-verification.md    this file
    pack-source/              the pack SOURCE the report's section e cites: rules/, census/ (the
                              preserved failed encodings, the validator's recorded output on each,
                              the R1 exhibit), fixtures/ (data only)
    PACKAGE-SHA256SUMS        over every file above; VERIFY.txt is the reader's transcript when
                              the package was proved before it left

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
