# Phase 2 fixture (REQ-093, fix review 2026-09-16): no seat at all: this rule is about revocation only; the seats are rule 00's (with the scaffold, allow).
[
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K1", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Execute",
    request_id: "tool-call:c1",
    t: 1100,
    principal: "Req::Agent::\"run1\""
  }
]
