# Phase 2 fixture (REQ-093, fix review 2026-09-16): a Revoke older than the horizon is not seen: fresh seats after it allow. Unreachable in our plane (terminal); the constant-horizon limit, G-174.
[
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K1", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :response,
    action: "Revoke",
    request_id: "approval-event:e0",
    t: 1000,
    principal: "Req::User::\"u1\""
  },
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K1", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :response,
    action: "Approve",
    request_id: "approval-event:e1",
    t: 90000,
    principal: "Req::User::\"u1\""
  },
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K1", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :response,
    action: "Coapprove",
    request_id: "approval-event:e2",
    t: 90010,
    principal: "Req::User::\"u2\""
  },
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K1", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Execute",
    request_id: "tool-call:c1",
    t: 90100,
    principal: "Req::Agent::\"run1\""
  }
]
