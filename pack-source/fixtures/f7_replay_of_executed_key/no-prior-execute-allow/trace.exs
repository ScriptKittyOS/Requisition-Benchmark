# Phase 2 fixture (REQ-093): event maps rendered through Exporter.render_line/1.
[
  %{
    fields: %{approval_id: "A1", idempotency_key: "K1", payload_hash: "H1", scope: "S1"},
    resource: "Req::Approval::\"A1\"",
    kind: :request,
    action: "Replay",
    request_id: "audit-event:x1",
    t: 1101,
    principal: "Req::Agent::\"run1\""
  }
]
