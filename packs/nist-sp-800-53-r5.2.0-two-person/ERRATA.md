# ERRATA — append-only, dated

A correction is a dated entry naming the scenario, the field, the old value and the new value. Nothing
above a correction is edited. A scenario whose expected verdict changes is RETIRED and re-issued under a
new id, so runs against the old id stay interpretable. A source edition change re-registers the pack.

## 2026-09-25 — eleven rows gain a stated witness set (`witnesses.given`); no verdict changes

**Why.** The first pack's independent review (Zaid Hasan Khan, 2026-09-25, 28/28 rows, 7 agree /
21 disagree) refused nine rows because the fact each verdict turns on was not in the evidence
packaged with the row. All 28 rows carried the same `witnesses` value — `{"ref": "trace", …}` — so
the exported trace was the whole witness set, and for those nine the trace cannot carry the
deciding fact. Measured: masking the idempotency key (which embeds the row id, and so made every
trace trivially unique) collapses the 28 traces to 20 shapes, with one group of FIVE rows carrying
two different verdicts on byte-identical evidence.

**The correction.** Each row below gains, in `witnesses`:

- `given` — an ordered list of `{at, fact}` entries: the facts the scenario POSITS, transcribed
  from the pre-registered drive in the frozen catalogue (`catalogue.ex` at `22216be`, the
  `catalogue_frozen_at` pin) and from the run record (`trials.jsonl`). Nothing is invented; every
  entry is checkable against those two sources.
- `given_source` — the `%Variant{}` slug, drive and params it was transcribed from.

and its `derivation` gains a sentence naming the stipulated fact the verdict turns on.

| # | scenario | field | old | new |
|---|---|---|---|---|
| 1 | `T1-F5-no-coapproval-001` | `witnesses.given` | absent | 4 facts: no co-approval is ever attempted (`coapprove_at: nil`) |
| 2 | `T1-F5-same-approver-001` | `witnesses.given` | absent | 4 facts: the same individual's countersign is SOUGHT at +10 and refused at the API (`:second_approver_required`, G-176) |
| 4 | `T1-F5-distinct-coapprover-001` | `witnesses.given` | absent | 4 facts, incl. the control's negatives: nothing revoked, no standing change, no hold, payload bound |
| 9 | `T1-F5-approver-revoked-001` | `witnesses.given` | absent | 5 facts, incl. approver-a's standing withdrawn at +50, the approval row untouched |
| 10 | `T1-F5-kill-switch-001` | `witnesses.given` | absent | 5 facts, incl. the plane-wide hold engaged at +50 |
| 11 | `T1-F5-coapprove-after-expiry-001` | `witnesses.given` | absent | 4 facts, incl. the 86400 s authority window and the countersign refused at +86401 |
| 12 | `T1-F4-cross-scope-001` | `witnesses.given` | absent | 4 facts, incl. both seats valid under account A and this trace being account B's caller run |
| 19 | `T1-F7-retry-after-refusal-001` | `witnesses.given` | absent | 5 facts, incl. the +0 attempt consuming no key and producing no effect |
| 21 | `T1-F4-payload-swap-002` | `witnesses.given` | absent | 5 facts, incl. the executed payload differing from the bound one and the author rewriting both bags |
| 22 | `T4-E3-sybil-001` | `witnesses.given` | absent | 4 facts, incl. no second seat ever taken and the Coapprove line being trace-author-supplied |
| 27 | `T3-D1-backdated-execute-001` | `witnesses.given` | absent | 5 facts, incl. the trusted instant +86401 against the presented +100 |

**No `expected` and no `refusal_code` changes.** All 28 verdict/code pairs are pinned against their
values at `4d51b78a` by a control test (REQ-165 W5), and no published run artifact is edited —
every row's `trace.sha256` still matches the file on disk (W6). Re-exporting the traces is not
available: a plane-wide hold is class **E5, inexpressible** as a windowed trace predicate
(`artifacts/crossplane-dogwood/findings.md:85`), and `PACKS.md` makes a re-export a new run.

**Registration now refuses the class.** `Pack.check/1` gained `witness_indistinguishable`: two rows
whose evidence digest (masked trace + stipulated facts) is equal but whose verdict or code differs
are refused by name. A collision whose rows AGREE is a `rows_evidence_duplicated` finding, not a
refusal — the four replay rows are one shape by construction and that is declared (G-141,
`findings.md:106`).

**This erratum stales every prior review by design** (M4/F10): `reviewed_pack_sha256` moves from
`658e9bd4…` to the value `bin/pack-check` now prints. The rows disputed for the other three reasons
— the unpinned authority TTL (rows 5, 6, 7), the locator citing `AC-3(2)` where the consumption
rule is pinned under `AC-3` (rows 13–16, 18), and the four harness/conformance rows (24, 25, 26,
28) — are NOT corrected here and should ride a single further erratum before the pack goes back to
a reviewer.

## 2026-09-25 (second entry) — corrections to the first entry, after two independent reviews

Both reviews of the 2026-09-25 correction returned **DO-NOT-LAND**. Nothing above is edited; this
entry carries the corrections.

| # | scenario | field | old | new |
|---|---|---|---|---|
| 22 | `T4-E3-sybil-001` | `witnesses.given[1].at` | `10` | **`1`** — the inserted Coapprove is at `@1788652801`, i.e. +1, in the shipped trace. The first entry's `10` was supported by neither the trace nor the catalogue. |
| 2, 9, 10, 4, 19, 21, 22 | `witnesses.given[].fact` | carried cross-row comparisons and editorial asides | facts only. Three rows named ANOTHER ROW'S ID inside their stipulations, which is the "make a row unique with arbitrary text" defect committed in data. |
| 21 | `witnesses.given[3].fact` | "the response input bag" | "both bags it appears in on that line (the request_context bag and the action's input bag)" — the line renders as `Execute::request(input:)`. |
| all 11 | `witnesses.given_source` | cited `%Variant{}` entries with slugs `same-approver-1` and `payload-swap-2` and a key `variant: :attacker_hash` | the verbatim entries. **Those slugs and that key DO NOT EXIST** in `catalogue.ex` at `22216be`: the slugs are `same-approver` and `payload-swap`, and the real discriminator is `narration: :f4b_attacker_hash` / `:e3_second_string_principal` / `trap: :t3d`. The first entry's claim that nothing was invented was false on exactly the rows whose content is "the trace author forged this". |
| all 11 | `witnesses.given_source` | cited `trials.jsonl` for drive parameters | `trials.jsonl` contains no parameters; it carries a verbatim step list in `notes` for three rows only, and the citation now says so. |

**Two claims in the first entry are WITHDRAWN.**

1. *"Registration now refuses the class."* It does not. `witness_indistinguishable` enforces that two
   rows are **stated differently**, not that a statement is true, relevant or complete: any distinct
   string dissolves a collision. It closes the narrow hole where two rows carry the same evidence and
   different answers **unnoticed**. A careless or dishonest author defeats it trivially, and truth
   remains the non-author reviewer's job.
2. *"Nothing is invented."* See the `given_source` row above.

**Known and NOT fixed** (named so a reviewer is not the one to discover them):

- **`witnesses.given` is not required.** 17 of 28 rows still carry only the generic witness, and
  `@row_required` does not include it, so a new row can ship with the old boilerplate and check clean.
- **Neither `catalogue.ex` nor `trials.jsonl` ships inside this pack**, so `given_source` is not
  checkable from the review packet alone and does not enter `reviewed_pack_sha256`.
- **Three rows remain underivable for a reason no stipulation can fix**: `SOURCE.md` pins no rule for
  account scope (`T1-F4-cross-scope-001`), no authoritative-clock rule (`T3-D1-backdated-execute-001`)
  and no numeric authority TTL — which rows 11 and 27 state in their own prose while rows 5, 6 and 7
  still have nothing. Pinning those three Assignment parameters is required before this pack is
  returned to a reviewer.

## 2026-09-25 (third entry) — the redesign: typed facts, shipped provenance, pinned parameters, counterfactuals

The second entry named three defects it did not fix. This entry fixes them, and changes the pack's
shape rather than patching rows — which is what §3 of the new `REVIEW-POLICY.md` requires when a
disagreement is systematic. Pack version **0.1.0 → 0.2.0**. Nothing above is edited.

**No `expected` or `refusal_code` changes. Again.** All 28 verdict/code pairs remain those of
`4d51b78a`, pinned by a control test, and no published run artifact is touched.

### What every row now carries

| addition | what it answers |
|---|---|
| `facts.given[]` — **typed** `{dimension, value, decisive, status, fact}` against `facts/dimensions.json` | v1 hashed the PROSE of a fact, so any distinct string dissolved a collision. A reworded fact is now the same fact; a vacuous string is not a fact. |
| every row states all **12 core dimensions**, not only its decisive one | "AC-3(2) is necessary but not sufficient, and the execution-time conditions are nowhere stated" — answered structurally instead of row by row. |
| `status`: `assumption` \| `observed` | The assurance-case tradition (GSN Community Standard) makes **Assumption** first-class and distinct from evidence; *Datasheets for Datasets* asks per field whether a value was observed or inferred. A stipulation is now labelled as one. |
| `facts.provenance` → `provenance/<id>.md`, digested | v2's citations pointed at files that **do not ship in the packet**. All 28 pre-registered catalogue entries, the constants they use, their drive functions and the run's own note are now sliced verbatim out of the frozen commit into the pack, so the digest enters `reviewed_pack_sha256` and the transcription is checkable here. |
| `under_test`: `rule_adjudication` \| `rule_silence` \| `harness_encoding` | Per the test-oracle taxonomy: a row whose decisive fact the system cannot sense tests the RULE, and must say so. |
| `counterfactual` — a named sibling row, the exact differing facts, and whether the verdict flips | **Distinguishable is not determinative.** Two rows can differ on a dimension the verdict does not turn on. Every `rule_adjudication` row must now demonstrate the flip, and a row that fails to is refused. |

### The three rows no stipulation could fix

`source/parameters.json` pins every value the pack had to choose, in **two kinds**, because NIST
supplies an id namespace for one and none for the other — conflating them would dress deployment
policy up as NIST text:

- **4 genuine ODPs**, ids read from the shipped catalog: `ac-03.02_odp`, `ac-05_odp`, `au-10_odp`,
  `au-08_odp`.
- **10 deployment policies** AC-3 enforces but does not define, and IA-2's organizational user —
  including the numeric **authority TTL of 86400 s**, the **account scope** rule, the
  **authoritative time source**, and *"a refusal is not an execution: it consumes nothing"*, which
  `T1-F7-retry-after-refusal-001`'s allow turns on and which nothing pinned.

Every fact dimension declares which parameter it reads, and that reference is checked.
`execution_burst` deliberately reads **nothing** — which is why `T4-R1-rate-limit-001` is
`unresolvable`, now derivable rather than asserted.

### The locators, and the four harness rows

Six rows whose decisive rule is the one-execution policy cited only `AC-3(2)`; the rule is pinned
under **AC-3**, which they now cite as well. The four `T3` rows are declared `harness_encoding` and
are **not scored as policy rows** — and the evidence for that call is in the data, not in an opinion:
each one's counterfactual against the control shows the encoding defect **does not change the
authorization verdict**, while all 23 `rule_adjudication` rows' counterfactuals do.

### Newly shipped so the packet is self-contained

`source/parameters.json`, `source/denial_codes.json` (135 codes, compared against the plane's
taxonomy at every check so a stale copy is refused), `facts/dimensions.json`, `provenance/` (28
files), `REVIEW-POLICY.md`.

### Still open, and named

- **Pre-registration is a git commit, which no established standard accepts** as pre-registration —
  it is integrity plus a self-asserted time. A third-party witness (signed pushed tag, RFC 3161
  timestamp, or registry DOI) is required before any scored release and does not yet exist.
- **Two independent reviews plus a meta-review** is the bar this pack now adopts; it has had one.
- Whether each row is *now* derivable is the reviewer's judgment, not the author's claim. The
  residual non-derivability rate will be reported with the next review, per `REVIEW-POLICY.md` §5.

_Digests are deliberately NOT quoted here: `ERRATA.md` is inside the set `reviewed_pack_sha256`
covers, so any value written in this file is stale the moment it is written. Run `bin/pack-check`
for the current pair._

## 2026-09-25 (fourth entry) — the verdict became DERIVED, not claimed

The third entry's redesign was reviewed twice more and both returned DO-NOT-LAND. One reviewer
CONSTRUCTED a row that passed every check with an indefensible answer: `T1-F5-same-approver-001`
(one individual holding both seats) relabelled `expected: allow`, zero refusals. Nothing in the pack
mapped facts to a verdict, so `expected` and `refusal_code` were author input that nothing checked.

**`facts/decision.json` is new and is the fix.** An ordered rule list over each row's typed facts;
the first rule that fires names the verdict and the denial code, otherwise the default `allow`. It
reproduces all 28 pre-registered verdicts and codes exactly, and `bin/pack-check` now DERIVES both
and refuses `expected_not_derivable` when a row disagrees with its own facts. Two orderings are
deliberate and stated in the file: expiry is evaluated before seat count, and revocation before
consumption.

| change | why |
|---|---|
| `decisive` is **derived**, not declared — the dimensions the firing rule reads | it was an author knob: a reviewer set one extra flag and walked a row out of a duplicate group |
| for an `allow`, `decisive` is **every dimension any rule reads** | the sufficiency argument, made mechanical instead of asserted in a prose note |
| **every row states every dimension** (17, all core) | an absent dimension made the procedure see nil, fire no rule, and grant a free pass on a condition nobody stated |
| `under_test` is a **closed set**, checked | it was an unvalidated free string, and the sole switch on the only verdict-facing rule |
| `source/denial_codes.json` carries **135 codes with their meanings** plus the selection rule | `refusal_code` was underivable pack-wide: bare strings, no definitions, no rule for choosing one |
| NIST citations are **compared against the shipped controls** — id, label, sp800-53a label, guideline | the missing control for the class that bit this pack: an earlier entry cited catalogue entries that did not exist |
| `proposer_separation` added | `ac-05_odp` clause 1 was pinned and read by no dimension, so the condition set was provably not closed |
| `T1-F5-distinct-coapprover-001` and four others now cite **AC-3** | their verdict turns on AC-3's execution-time policy while they cited only AC-3(2) |
| `status` is decided **per row** | it was a per-dimension constant and false on three rows — `T1-F4-cross-scope-001` called seat facts `observed` on a trace holding one Execute line |
| digests removed from this file | `ERRATA.md` is inside the set `reviewed_pack_sha256` covers, so any digest written here is stale the moment it is written |

**Still true, and still the open items:** no verdict has moved across any of these four errata — all 28
pairs remain those of `4d51b78a` — and no published run artifact has been edited. Pre-registration is
still a git commit with no third-party witness. The pack has had one external review and the policy
now requires two plus a meta-review.

## 2026-09-26 (fifth entry) — the four structural items from the second independent review

Source of truth: the independent review of 26 September 2026 (*Updated 28-Row NIST Two-Person
Packet — Verdict Derivability & Internal Consistency Check*). Its headline result:
**28/28 expected verdicts derivable, residual verdict non-derivability 0/28**, with provenance
digests 28/28 and NIST control digests 6/6 matching. It raised four structural items that do not
change any verdict. Those four, and only those four, are corrected here.

| # | item | correction |
|---|---|---|
| 1 | ten `counterfactual.flip` entries recorded `to: null` where the paired row holds a concrete value | **recomputed**, not hand-patched — the nulls were stale, written before every row was made to state every dimension. The flip SETS were already correct; only the recorded targets moved, and the ten new values match the review's table exactly |
| 2 | `replayed` appears in `refusal_code` on four rows and is not in `source/denial_codes.json` | **the contract is extended** (the review's second option): `pack.json` gains `codes.contract`, `source/denial_codes.json` gains a pointer to `codes.extra`, and `REVIEW-POLICY.md` gains §7 |
| 3 | `SOURCE.md` said "11 deployment policies"; `parameters.json` and this file say 10 | **10** |
| 4 | `unresolvable_share` was 1/28 while its note measured against the 24 scored policy rows | denominator **24**, and the note now records that `Pack.check/1` evaluates the ceiling over all 28 rows, which is marginally **more permissive** than the declared denominator |

**On item 2, why the contract was extended rather than the field moved.** Not every scored `deny` is
a denial: `replayed` records that a served replay produced **no second effect** and returned the
first effect's receipt, which answers the rule's question — whether a second effect occurred — even
though the plane refused nothing. `codes.extra` already existed to carry exactly this case, and
`Pack.check/1` already resolved `refusal_code` against both sets, so the permission was enforced
and merely undocumented. Moving the value to a new field would also have left the extras mechanism
declared and no longer exercised by any row, which is the pattern this pack has been bitten by
repeatedly.

**Nothing else changed.** All 28 `expected`/`refusal_code` pairs are byte-identical to `4d51b78a`,
verified against that commit rather than asserted; no published run artifact was touched; no
`lib/` file was touched. `bin/pack-check` PASS with 0 refusals.
