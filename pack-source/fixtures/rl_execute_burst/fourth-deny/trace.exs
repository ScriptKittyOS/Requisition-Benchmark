# Phase 2 fixture (REQ-093): event maps rendered through Exporter.render_line/1.
[
  %{
    fields: %{approval_id: "A1", idempotency_key: "K1", payload_hash: "H1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Execute",
    request_id: "tool-call:c1",
    t: 1101,
    principal: "Req::Agent::\"run1\""
  },
  %{
    fields: %{approval_id: "A1", idempotency_key: "K2", payload_hash: "H1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Execute",
    request_id: "tool-call:c2",
    t: 1102,
    principal: "Req::Agent::\"run1\""
  },
  %{
    fields: %{approval_id: "A1", idempotency_key: "K3", payload_hash: "H1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Execute",
    request_id: "tool-call:c3",
    t: 1103,
    principal: "Req::Agent::\"run1\""
  },
  %{
    fields: %{approval_id: "A1", idempotency_key: "K4", payload_hash: "H1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Execute",
    request_id: "tool-call:c4",
    t: 1104,
    principal: "Req::Agent::\"run1\""
  }
]
