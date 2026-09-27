# SOURCE — NIST SP 800-53, Release 5.2.0

| | |
|---|---|
| identifier | NIST Special Publication 800-53, *Security and Privacy Controls for Information Systems and Organizations* |
| edition | **Release 5.2.0** (the catalog's `metadata.version`; `last-modified` 2026-05-11) — see the note on the draft's edition line below |
| effective window | from 2026-05-11, open — until NIST supersedes 5.2.0; the pack then re-registers under the new edition and this one stays runnable, labelled by its window |
| obtained | the NIST OSCAL catalog, `usnistgov/oscal-content` tag `v1.5.0` (commit `78650f02ad9321bb7b817846f8fbd4f2bcd620de`, 2026-05-13), path `nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json`, sha256 `01f37cf90ea99d92242c936cbfbdebcc338eef1f71454e2acac36cc56e9bc062`, 10,442,037 bytes, fetched 2026-09-21 |
| shipped | `source/controls/` — the six relied-on controls, each the catalog's own JSON subtree (re-serialised with sorted keys; the one transformation), digests in `source/index.json`; the whole catalog is NOT shipped (10 MB) — a reviewer re-fetches it at the tag, checks the sha256, and re-runs `docs/slices/requisition/REQ-155-pack-registration-shape/extract_source.py` to get byte-identical control files |
| relied-on controls | AC-3 Access Enforcement; AC-3(2) Dual Authorization; AC-5 Separation of Duties; IA-2 Identification and Authentication (Organizational Users); AU-8 Time Stamps; AU-10 Non-repudiation |

**The reviewer's first check.** Every `rule_text` in `scenarios.jsonl` is verified by `bin/pack-check` against
the shipped control's statement or discussion (whitespace-normalised). The reviewer's own first check is the
shipped controls against the copy they hold — the NIST PDF of 5.2.0 or their own OSCAL fetch at the tag.

**Why 5.2.0 and not "Rev. 5 + the December 2020 errata".** The author's draft of 2026-09-21 pinned the 2020
edition from memory and a mirror labelled 5.2.0. Measured at assembly: NIST's current catalog is Release 5.2.0,
and the six controls' operative statements and the AC-3(2) discussion sentence relied on are the draft's quotes
verbatim. The pack pins the edition an assessor holds today. If the review wants the 2020 text instead, that is
a re-registration under that edition, not an edit here.

**The values this pack pins live in `source/parameters.json`, in TWO KINDS.** They are not listed
here in prose, because a prose list next to a machine-readable one drifts, and because listing them
together blurs a distinction that matters:

- **4 organization-defined parameters (ODPs)** — genuine NIST Assignment operations, with the ids and
  labels the shipped catalog gives them: `ac-03.02_odp`, `ac-05_odp`, `au-10_odp`, `au-08_odp`.
  `bin/pack-check` compares each declared id, label and guideline against `source/controls/`, so a
  citation this pack cannot verify against its own shipped source is refused.
- **10 deployment policies** — **NOT NIST text.** AC-3 enforces "approved authorizations ... in
  accordance with applicable access control policies" but does not define those policies, and IA-2
  does not define who an organizational user is. **AC-3 and IA-2 have no ODP at all** (`params: []`
  in the shipped subtrees). These are this deployment's rules, which AC-3 and IA-2 then enforce:
  the canonical-action binding, the **86400 s** authority TTL, expiry precedence, revocation,
  approver standing, organizational hold, **one execution — and that a REFUSAL IS NOT AN EXECUTION
  and consumes nothing**, account scope, the authoritative time source, and the organizational user.

**Why they are pinned at all.** The first independent review (2026-09-25) refused rows whose verdict
turns on a numeric deadline, on account scope, on which clock is authoritative, on whether a named
principal is a real user, or on whether a refused attempt consumed the authorization — none of which
this pack pinned, so no reviewer could derive them however the scenario was written.

**How a verdict follows from them.** `facts/decision.json` is an ordered rule list over each row's
typed facts; the first rule that fires names the verdict and the denial code. `bin/pack-check`
DERIVES every row's verdict and refuses the row if it claims otherwise — so `expected` is not
author input.

