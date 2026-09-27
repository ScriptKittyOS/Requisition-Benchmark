# The first pack — NIST SP 800-53 r5.2.0, the two-person class

**Status: DRAFT, unregistered.** Every row's `reviewed_by` is null and no review file exists under `reviews/`.
Nothing here is a benchmark result; a run against an unregistered pack is an exploratory run by the contract.

What is here, in the contract's shape (`docs/internal/benchmark-specification-authorization-planes-2026-09-19.md`
§The pack contract): `pack.json`, `SOURCE.md` + `source/`, `scenarios.jsonl` (28 rows), `predicates/`,
`roster.json`, `generators/` (a stated absence), `reviews/` (the reviewer's file, the join that fills
`reviewed_by`), `ERRATA.md`. `MANIFEST.json` and `SHA256SUMS` appear only when `bin/pack-register` succeeds.

    bin/pack-check    bench/requisition/packs/nist-sp-800-53-r5.2.0-two-person   # the contract's rules, the join, the digests
    bin/pack-register bench/requisition/packs/nist-sp-800-53-r5.2.0-two-person   # refuses until every row is reviewed
    sha256sum -c SHA256SUMS                                                       # a stranger's check, no Elixir

The rows were assembled from the author's draft (`docs/internal/first-pack-draft-nist-800-53-UNREVIEWED-2026-09-21.md`)
by `docs/slices/requisition/REQ-155-pack-registration-shape/assemble_rows.py`; the draft is what the reviewer reads,
this file is what registers. The two must say the same thing; the assembler is how. Two expansions it makes,
stated: a draft cell reading only `inexpressible` receives the pack's one stated reason (`predicates/index.json`
→ `inexpressible.reason`); a draft locator receives the control's operative units as `rule_text`
(`assemble_rows.py` → `RULE_TEXT`), which `bin/pack-check` verifies against `source/` unit by unit.
