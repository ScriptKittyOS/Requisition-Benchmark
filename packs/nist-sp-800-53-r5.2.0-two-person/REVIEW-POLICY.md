# Review, adjudication and disagreement policy

Written 2026-09-25, after the first independent review refused 21 of 28 rows. Until then this pack
had a registration rule (`reviews/README.md`) and no policy for what happens when a reviewer
disagrees, what counts as enough review, or what gets reported. Established practice has answers for
all three and this pack was below the bar on each.

## 1. How much review is enough

**Two independent non-author reviews, then a meta-review.** One non-author reviewer is below
established practice: BIG-bench requires two public, non-anonymous reviews per task for technical
correctness and construct validity, followed by a meta-review committee. This pack adopts that bar.

`bin/pack-register` already refuses a reviewer who is a pack author (`review_self`). The policy adds,
and the registration check does **not** enforce, two conditions a human must confirm:

- the two reviewers are independent of each other, and
- at least one is outside the authoring organization.

Those are recorded in the meta-review note, not machine-checked, and that limit is stated rather than
papered over.

## 2. What a reviewer decides

A reviewer decides one question per row: **is the pre-registered expected verdict independently
derivable from the cited rule text, the pinned parameters (`source/parameters.json`), and the
materials shipped in this packet?** Not "is the safety behaviour right" — a row can be refused while
its intent is correct, which is exactly what happened on 2026-09-25.

Since that review the packet also contains, for every row: typed facts over a closed vocabulary
(`facts/dimensions.json`), each fact marked `assumption` or `observed`; the pre-registered source of
each stipulation (`provenance/<id>.md`, digested into `reviewed_pack_sha256`); a counterfactual row
with the exact facts that differ and whether the verdict changes; and the denial-code vocabulary
(`source/denial_codes.json`).

## 3. Adjudication when a reviewer disagrees

Following standard inter-coder practice:

1. Independent review by both reviewers, without seeing each other's file.
2. Disagreements — reviewer against pack, or reviewer against reviewer — go to a **third adjudicator**
   who rules against this document and `SOURCE.md`, not against the author's intent.
3. **If the disagreement is systematic, the guidelines are revised and the affected rows re-issued —
   the items are not patched one by one.** The 2026-09-25 review was systematic (one defect class,
   nine rows), and patching row by row is precisely the mistake the first correction attempt made.
4. A row whose expected verdict changes is **retired and re-issued under a new id** (`ERRATA.md`), so
   runs against the old id stay interpretable. A row whose supporting material changes is corrected
   by erratum and keeps its id.

## 4. The agreement statistic

Report the **named** coefficient, never a bare number: **Cohen's κ** for two raters, **Fleiss' κ** for
three or more. They use different chance models and are not interchangeable. Report per-aspect rather
than one figure for the pack, since a single number cannot characterise a whole task.

**First review, 2026-09-25 — reported rather than buried.** One reviewer, 28 rows, 7 agree / 21
disagree: **raw agreement 25.0%** against the pack's pre-registered labels. **No κ is reported, and
none can be**: κ requires at least two independent raters, and this pack had one. That absence is
itself the finding that motivated §1.

Disagreements by cause: 9 the deciding fact was absent from the packaged evidence; 3 an
organization-defined value was named but never pinned; 5 the locator cited the enhancement where the
decisive rule sits in the base control; 4 a comparator-encoding condition scored as a policy row.

## 5. Residual non-derivability is published, not hidden

Following GPQA, which publishes a conservative objectivity estimate rather than implying its labels
are certain: each review cycle reports the count of rows no independent reviewer could derive, and
that figure ships with any scored result. **A scored run whose pack has an unreported residual
non-derivability rate is not a valid result of this benchmark.**

## 6. Pre-registration — the known weakness

The pack pins its scenario catalogue at a git commit (`catalogue_frozen_at`). **A git commit is not
pre-registration by any established standard.** OSF registration is a frozen, time-stamped copy held
by a *third party*; ICMJE/WHO requires a public registry entry with prespecified outcomes; neither
accepts self-custodied, rewritable history. A commit gives integrity and a self-asserted time, which
is strictly less.

Required before any scored release, and **not yet done**:

- a **third-party witness** of the pre-registration: a signed annotated tag pushed to the public
  remote, or an RFC 3161 timestamp over the catalogue digest, or a registry DOI;
- an **amendment log** — registrations are versioned, never overwritten (`ERRATA.md` serves this for
  the pack; the catalogue pin needs its own);
- a declared **minimum field list** a row must fill or be refused. `@row_required` in
  `RequisitionBench.Pack` is that list, and it is now machine-enforced.

Until the third-party witness exists, any claim that an expectation was registered *before* the
result was known rests on the author's word. Stated here so a reader does not have to infer it.

## 7. What a `refusal_code` may name

A row's `refusal_code` may name **either** a code from `source/denial_codes.json` — the plane's
denial taxonomy — **or** an extra outcome code declared in `pack.json`'s `codes.extra`. The second
set exists because not every scored `deny` is a denial: `replayed` records that a served replay
produced **no second effect** and returned the first effect's receipt, which is the answer to the
rule's question even though the plane refused nothing.

The permission is **enforced, not merely stated**: `Pack.check/1` resolves a row's `refusal_code`
against the union of both sets and refuses `refusal_code_unknown` for anything in neither.

Written after the 2026-09-26 independent review found `replayed` in four rows and absent from the
denial vocabulary, with nothing in the contract permitting it. The review offered two remedies —
move the value to a separate field, or extend the contract. The contract was extended, because the
pack already reasoned its way to scoring these rows this way and `codes.extra` already existed to
carry exactly this case; moving the field would also have left the extras mechanism declared and
untested.
