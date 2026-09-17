# Phase 2 fixture (REQ-093, fix review 2026-09-16): Approve, Coapprove, Revoke, one fresh Approve: revocation is terminal -> deny (under the since-idiom this replayed ALLOW; fix review 3).
[
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K1", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :response,
    action: "Approve",
    request_id: "approval-event:e1",
    t: 1000,
    principal: "Req::User::\"u1\""
  },
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K1", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :response,
    action: "Coapprove",
    request_id: "approval-event:e2",
    t: 1010,
    principal: "Req::User::\"u2\""
  },
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K1", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :response,
    action: "Revoke",
    request_id: "approval-event:e3",
    t: 1050,
    principal: "Req::User::\"u1\""
  },
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K1", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :response,
    action: "Approve",
    request_id: "approval-event:e4",
    t: 1060,
    principal: "Req::User::\"u1\""
  },
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
