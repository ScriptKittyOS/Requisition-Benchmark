# Phase 2 fixture (REQ-093, fix review 2026-09-16): Coapprove older than the window, Approve fresh -> implicit deny: every seat must be within the horizon (fix review 11).
[
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K1", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :response,
    action: "Coapprove",
    request_id: "approval-event:e1",
    t: 1000,
    principal: "Req::User::\"u2\""
  },
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K1", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :response,
    action: "Approve",
    request_id: "approval-event:e2",
    t: 87000,
    principal: "Req::User::\"u1\""
  },
  %{
    fields: %{payload_hash: "H1", idempotency_key: "K1", approval_id: "A1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Execute",
    request_id: "tool-call:c1",
    t: 87500,
    principal: "Req::Agent::\"run1\""
  }
]
