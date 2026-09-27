# Provenance — `T3-E1-undeclared-action-001`

Every fact in this scenario's `facts.given` is transcribed from the text below. Nothing here
is written for the pack: each block is sliced verbatim out of a frozen commit, and this file
is inside the pack, so its digest is part of `reviewed_pack_sha256` and you can check the
transcription without leaving the review packet.

| | |
|---|---|
| pre-registration commit | `22216be` (the pack's `catalogue_frozen_at` pin) |
| catalogue | `test/support/campaigns/dogwood/catalogue.ex` lines 459-475 |
| drive | `test/support/campaigns/dogwood/driver.ex` lines 94-110 |
| run record | `artifacts/crossplane-dogwood/2026-09-18-79df522b/trials.jsonl`, this row's `notes` |

## The pre-registered catalogue entry, verbatim

```elixir
      %Variant{
        class: :t3,
        family: "E1",
        slug: "undeclared-action",
        drive: :f5_seats,
        params: @seats,
        trap: :t3e,
        expected_agreement: :disagree_dogwood_denies,
        expected_requisition: %{outcome: :allowed, denial_code: nil},
        expected_dogwood: %{
          verdict: :deny,
          determining_rules: [],
          deny_provenance: :undeclared_deny
        },
        notes:
          "T3e: the decision line's action renamed to one the schema does not declare (`Req::Action::\"Transfer\"`, qualified). MEASURED: deny [], `errors: []`, exit 0 -- the binary is SILENT about a line it does not know; a misconfiguration reads as a deny. The replayer names the undeclared line. The rendered action is on the record. Ours: W5's registry refuses by name."
      }
```

## The module attributes it refers to, verbatim

```elixir
@seats %{approve_at: 0, coapprove_at: 10, execute_at: 100}
```

## The drive `:f5_seats`, verbatim

```elixir
  defp build(:f5_seats, v, %Prepared{} = prepared, account, owner, run, key) do
    {approval, steps, idem, payload} = seats(v.params, account, owner, run, key, :distinct)
    execute_at = offset(v.params.execute_at)

    %Prepared{
      prepared
      | approval_ids: [approval.id],
        idempotency_keys: [idem],
        approved_hash: hash(payload),
        driven_payload: payload,
        steps: steps,
        context:
          context(account, run, approval, idem, payload, payload, fn ->
            at(execute_at)
            execute(account, run, approval, idem, payload)
          end)
    }
```

## The run's own note for this row, verbatim

> T3e: the decision line's action renamed to one the schema does not declare (`Req::Action::"Transfer"`, qualified). MEASURED: deny [], `errors: []`, exit 0 -- the binary is SILENT about a line it does not know; a misconfiguration reads as a deny. The replayer names the undeclared line. The rendered action is on the record. Ours: W5's registry refuses by name.
