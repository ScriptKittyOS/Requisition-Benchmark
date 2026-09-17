# Phase 2 fixture (REQ-093, fix review 2026-09-16): three Executes by run1 then one by run2 inside 10m: the count is per callerPrincipal, so the fourth is allowed (fix review 11).
[
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K1", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Execute",
    request_id: "tool-call:c1",
    t: 1000,
    principal: "Req::Agent::\"run1\""
  },
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K2", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Execute",
    request_id: "tool-call:c2",
    t: 1010,
    principal: "Req::Agent::\"run1\""
  },
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K3", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Execute",
    request_id: "tool-call:c3",
    t: 1020,
    principal: "Req::Agent::\"run1\""
  },
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K4", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Execute",
    request_id: "tool-call:c4",
    t: 1030,
    principal: "Req::Agent::\"run2\""
  }
]
