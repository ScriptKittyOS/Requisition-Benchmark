# Phase 2 fixture (REQ-093): two forbids fire on one deny, so determining_rules carries two ids (sorted).
[
  %{
    fields: %{approval_id: "A1", idempotency_key: "K1", payload_hash: "H1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :response,
    action: "Approve",
    request_id: "approval-event:e1",
    t: 1000,
    principal: "Req::User::\"u1\""
  },
  %{
    fields: %{approval_id: "A1", idempotency_key: "K1", payload_hash: "H1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :response,
    action: "Coapprove",
    request_id: "approval-event:e2",
    t: 1010,
    principal: "Req::User::\"u2\""
  },
  %{
    fields: %{approval_id: "A1", idempotency_key: "K1", payload_hash: "H1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Execute",
    request_id: "tool-call:c1",
    t: 1100,
    principal: "Req::Agent::\"run1\""
  },
  %{
    fields: %{approval_id: "A1", idempotency_key: "K1", payload_hash: "H1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :response,
    action: "Revoke",
    request_id: "approval-event:e3",
    t: 1150,
    principal: "Req::User::\"u1\""
  },
  %{
    fields: %{approval_id: "A1", idempotency_key: "K1", payload_hash: "H1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Execute",
    request_id: "tool-call:c2",
    t: 1200,
    principal: "Req::Agent::\"run1\""
  }
]
