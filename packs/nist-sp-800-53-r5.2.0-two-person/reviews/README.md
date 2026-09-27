# reviews/ — the reviewer's signed file

`reviewed_by` is null on every row of `scenarios.jsonl` as authored and stays so: the author never types
a reviewer's name. A reviewer returns ONE file here, `<reviewer-slug>.json`:

```json
{
  "reviewer": "name, affiliation",
  "reviewed_at": "2026-09-30",
  "scenarios_sha256": "<the sha256 of the scenarios.jsonl reviewed -- printed by bin/pack-check>",
  "reviewed_pack_sha256": "<the digest of the WHOLE reviewed pack -- rows, source/, SOURCE.md, predicates/, roster.json; printed by bin/pack-check>",
  "rows": [
    {"id": "T1-F5-no-coapproval-001", "agree": true},
    {"id": "T1-F5-expired-boundary-001", "agree": false, "note": "the window is open at the deadline under our reading; re-pin the Assignment"},
    ...
  ]
}
```

The registration check JOINS this file to the rows: a row is reviewed when a review at the CURRENT
digests agrees with it. A review at another digest is `review_stale`, naming which — the rows moved, or
anything else the reviewer read did (a source page, an Assignment pin in `SOURCE.md`, the roster, a
predicate); the reviewer re-reads. A disputed row is `row_disputed` and the pack does not register until
an erratum retires or re-issues it. A reviewer whose name is a pack author is `review_self` and never
joins. A row named twice in one file, a `reviewed_at` that is not an ISO date, or an id the pack does not
have is `review_malformed`. A row nobody has agreed is `rows_unreviewed` — a finding on `check`, a refusal
on `register`. Every row's resolved `reviewed_by` is written into `MANIFEST.json` at registration.
