# Authoring a pack against these traces

A **pack** is a set of Dogwood rules that judge the same traces the plane was driven through. The
pack in `runs/<run id>/pack/` is ours. Anyone can write another against the same contract and
compare its verdicts with the plane's evidence, offline, with nothing but this package and a Dogwood
binary built at the pinned commit.

## The contract (what a rule may name)

Everything below is read off the files in `pack-source/` and `runs/<run id>/pack/`; those files
are the contract, this page only points at them.

- **The schema**: `pack/schema.cedarschema` — namespace `Req`; entities `User`, `Agent`, `System`,
  `Approval`, `Run`; five actions, each with its principal and resource types and one input bag:
  `Approve`, `Coapprove`, `Revoke` (principal `User` or `System`) and `Execute`, `Replay`
  (principal `Agent`), on `Approval` or `Run`. Every input bag carries `approval_id`,
  `idempotency_key`, `payload_hash` and `scope` (strings). A rule reads them as
  `context.input.<field>`.
- **The events**: `pack/events.dwschema` — every action has a `<A>::request` (the decision event)
  and an `<A>::response` (the recorded outcome), each carrying the input bag, the caller's
  principal and resource, and a `requestId`. Decision lines in a trace are `::request`; history
  lines the plane recorded are `::response`. The schema is unpinned on purpose: a rule may read
  another principal's history (two-person patterns).
- **The horizon**: every window in our rules is `within 24h`, the plane's authority TTL; the event
  schema's `max_window` bounds what a rule may ask for (the census entry
  `pack-source/census/E6_standing_authority_365d.*` shows the validator refusing `365d`).
- **The traces**: `runs/<run id>/traces/<trial>.log`, one per scenario, exactly what the plane
  exported; a line is `@<unix seconds> scope(principal: …, resource: …) request_context(input: {…})`
  followed by the event. The instants are the campaign's pinned clock, not wall time.
- **The rule files**: one statement per file, one `@id("…")` matching the filename's `<id>`, in
  `NN_<id>.dw` order (the index is the filename order); one `permit` per decision action across
  the pack; `forbid`s beside it. `pack-source/rules/` is the worked example; the assembler refuses
  a second permit for a decision action, a file with two statements or two ids, and a rule that
  does not validate alone.

## Compare a pack with the plane, offline

    dogwood replay <your-pack>.dw --policy-schema pack/schema.cedarschema \
        --event-schema pack/events.dwschema --trace runs/<run id>/traces/<trial>.log --format json

For each trial, the plane's side is `requisition.evidence` and `requisition.denial_code` in
`runs/<run id>/trials.jsonl`; the subject event is the last decision line of the trace.
`verify_dogwood_side.py` shows the exact command line and the verdict-vector shape it compares.

## Running a foreign pack as a campaign run

The campaign's own runner takes a pack directory: `bin/campaign-run --pack-rules-dir DIR` (in the
private tree) assembles DIR as the run's pack and records its digest as `pack_sha256`. **A foreign
pack is a new pre-registration and a new run, never a swap under a published run's numbers**: each
scenario's expected verdict under the new pack is written down first, the run is qualified and
delivered through the same pipeline, and it ships as its own release with its own tag. The
option is refused with `--qualified` for exactly that reason. `v0.1.0`'s numbers are ours, under
our pack, and stay so.
