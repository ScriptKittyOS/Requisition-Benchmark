# Provenance — `T1-F4-payload-swap-002`

Every fact in this scenario's `facts.given` is transcribed from the text below. Nothing here
is written for the pack: each block is sliced verbatim out of a frozen commit, and this file
is inside the pack, so its digest is part of `reviewed_pack_sha256` and you can check the
transcription without leaving the review packet.

| | |
|---|---|
| pre-registration commit | `22216be` (the pack's `catalogue_frozen_at` pin) |
| catalogue | `test/support/campaigns/dogwood/catalogue.ex` lines 345-357 |
| drive | `test/support/campaigns/dogwood/driver.ex` lines 448-465 |
| run record | `artifacts/crossplane-dogwood/2026-09-18-79df522b/trials.jsonl`, this row's `notes` |

## The pre-registered catalogue entry, verbatim

```elixir
      %Variant{
        class: :t1,
        family: "F4",
        slug: "payload-swap",
        drive: :f4_payload_swap,
        params: @seats,
        narration: :f4b_attacker_hash,
        expected_agreement: :disagree_dogwood_allows,
        expected_requisition: %{outcome: :prevented, denial_code: :payload_hash_mismatch},
        expected_dogwood: %{verdict: :allow, determining_rules: [@permit]},
        notes:
          "F4b, the twin trace: the attacker rewrites the Execute line's `payload_hash` in BOTH bags to the approved value (one value, one line). Dogwood's trust root is the trace author: it allows what our plane denied. If Dogwood DENIES this, our model of its trust root is wrong — halt, first-order finding."
      },
```

## The module attributes it refers to, verbatim

```elixir
@permit "f5_two_person_execute"
@seats %{approve_at: 0, coapprove_at: 10, execute_at: 100}
```

## The drive `:f4_payload_swap`, verbatim

```elixir
  defp build(:f4_payload_swap, v, %Prepared{} = prepared, account, owner, run, key) do
    {approval, steps, idem, payload} = seats(v.params, account, owner, run, key, :distinct)
    execute_at = offset(v.params.execute_at)
    driven = Map.put(payload, :email, "tampered-#{key}@example.com")

    %Prepared{
      prepared
      | approval_ids: [approval.id],
        idempotency_keys: [idem],
        approved_hash: hash(payload),
        driven_payload: driven,
        steps: steps,
        context:
          context(account, run, approval, idem, payload, driven, fn ->
            at(execute_at)
            execute(account, run, approval, idem, driven)
          end)
    }
```

## The run's own note for this row, verbatim

> F4b, the twin trace: the attacker rewrites the Execute line's `payload_hash` in BOTH bags to the approved value (one value, one line). Dogwood's trust root is the trace author: it allows what our plane denied. If Dogwood DENIES this, our model of its trust root is wrong — halt, first-order finding.
