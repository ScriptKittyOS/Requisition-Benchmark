# Provenance — `T3-D1-backdated-execute-001`

Every fact in this scenario's `facts.given` is transcribed from the text below. Nothing here
is written for the pack: each block is sliced verbatim out of a frozen commit, and this file
is inside the pack, so its digest is part of `reviewed_pack_sha256` and you can check the
transcription without leaving the review packet.

| | |
|---|---|
| pre-registration commit | `22216be` (the pack's `catalogue_frozen_at` pin) |
| catalogue | `test/support/campaigns/dogwood/catalogue.ex` lines 442-458 |
| drive | `test/support/campaigns/dogwood/driver.ex` lines 94-110 |
| run record | `artifacts/crossplane-dogwood/2026-09-18-79df522b/trials.jsonl`, this row's `notes` |

## The pre-registered catalogue entry, verbatim

```elixir
      %Variant{
        class: :t3,
        family: "D1",
        slug: "backdated-execute",
        drive: :f5_seats,
        params: %{@seats | execute_at: :ttl_plus_one} |> Map.put(:trap_at, 100),
        trap: :t3d,
        expected_agreement: :disagree_dogwood_allows,
        expected_requisition: %{outcome: :prevented, denial_code: :approval_expired_at_execution},
        expected_dogwood: %{
          verdict: :allow,
          determining_rules: [@permit],
          deny_provenance: nil
        },
        notes:
          "T3d: the subject executed at +TTL+1 -- ours refused it (`approval_expired_at_execution`; the deadline is `Clock`'s, W1) -- and the trace author backdates its `@t` to +100. MEASURED: Dogwood ALLOWS (`f5_two_person_execute`): the window holds a resurrected event; the trust root is the trace author. Both instants are on the record (`trap_record`). Ours: no caller supplies an instant; every stamp is `Clock`'s (W1, REQ-136) and the receipts are signed (W3)."
      },
```

## The module attributes it refers to, verbatim

```elixir
@permit "f5_two_person_execute"
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

> T3d: the subject executed at +TTL+1 -- ours refused it (`approval_expired_at_execution`; the deadline is `Clock`'s, W1) -- and the trace author backdates its `@t` to +100. MEASURED: Dogwood ALLOWS (`f5_two_person_execute`): the window holds a resurrected event; the trust root is the trace author. Both instants are on the record (`trap_record`). Ours: no caller supplies an instant; every stamp is `Clock`'s (W1, REQ-136) and the receipts are signed (W3).
