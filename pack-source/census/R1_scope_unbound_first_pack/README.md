# R1 exhibit — the first pack did not bind scope (G-191)

**What this is.** The Dogwood pack as it stood at the pre-registration commit `22216be` (the
rehearsal on `c24c366` ran it; `pack.dw` here is byte-identical to
`artifacts/crossplane-dogwood/rehearsals/2026-09-16-c24c366/pack/pack.dw`, sha256
`7c34dd5c9f96f320ccfe11ad1821dd74d6313e71cc8a1980bc3872a52cb1616d`), its two schema files as
generated then (no `scope` field), and an ATTACKER-AUTHORED trace: account A's two seats
(`u1`, `u2`) spliced onto account B's Execute (`run-b`), same approval id, payload hash and
key. Nothing in the trace names an account, because the exporter of that day exported none.

**What it shows.** `replay.json` is the binary's own output (`fa7a323`), recorded 2026-09-17:
`allow`, `determining_rules: [0]` (`f5_two_person_execute`). The pack permitted an Execute
under one account on the strength of seats given under another. Our plane refuses the same
attempt before the door (`:account_scope_mismatch`, REQ-138); the campaign's row
`T1-F4-cross-scope-001` recorded `agree` (both deny) only because the caller's OWN trace has
no seats -- the implicit deny was for the wrong reason (REQ-095's measurement).

**Why it is preserved.** The finding is about authoring burden, not expressiveness: Dogwood
CAN bind a scope (the amended rule 00 does: `input.scope: context.input.scope` on both seats)
but nothing in the language requires an author to, and the first pack -- validated, exercised
against 43 bundles, rehearsed with every cell holding -- did not. G-191.

**Reproduce.**

    dogwood replay pack.dw --policy-schema schema.cedarschema --event-schema events.dwschema \
      --trace spliced.log --format json

`ScopePinTest` SP7 runs exactly that and compares the output with `replay.json` byte for byte
(after the campaign's canonicalisation), and checks `pack.dw`'s digest against the rehearsal
manifest's `pack_sha256`. The live pack (`pack/rules/00_f5_two_person_execute.dw`) denies the
same trace once it carries the scope field: bundle `_pack/spliced-seats-other-scope-deny`.
