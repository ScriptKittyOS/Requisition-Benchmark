# REQ-139 (R1, G-191) fixture: account A's two seats spliced onto account B's Execute -- same approval, hash and key, a different scope. ALLOWED under the first pack (pack/census/R1_scope_unbound_first_pack/); the scope pin on both seats denies it (implicit: no seat in B's scope).
[
  %{
    fields: %{approval_id: "A1", idempotency_key: "K1", payload_hash: "H1", scope: "SA"},
    resource: "Req::Approval::\"A1\"",
    kind: :response,
    action: "Approve",
    request_id: "approval-event:e1",
    t: 1000,
    principal: "Req::User::\"u1\""
  },
  %{
    fields: %{approval_id: "A1", idempotency_key: "K1", payload_hash: "H1", scope: "SA"},
    resource: "Req::Approval::\"A1\"",
    kind: :response,
    action: "Coapprove",
    request_id: "approval-event:e2",
    t: 1010,
    principal: "Req::User::\"u2\""
  },
  %{
    fields: %{approval_id: "A1", idempotency_key: "K1", payload_hash: "H1", scope: "SB"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Execute",
    request_id: "tool-call:c-b",
    t: 1100,
    principal: "Req::Agent::\"run-b\""
  }
]
