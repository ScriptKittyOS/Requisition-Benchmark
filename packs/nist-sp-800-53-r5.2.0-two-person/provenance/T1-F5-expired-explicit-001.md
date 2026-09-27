# Provenance — `T1-F5-expired-explicit-001`

Every fact in this scenario's `facts.given` is transcribed from the text below. Nothing here
is written for the pack: each block is sliced verbatim out of a frozen commit, and this file
is inside the pack, so its digest is part of `reviewed_pack_sha256` and you can check the
transcription without leaving the review packet.

| | |
|---|---|
| pre-registration commit | `22216be` (the pack's `catalogue_frozen_at` pin) |
| catalogue | `test/support/campaigns/dogwood/catalogue.ex` lines 155-166 |
| drive | `test/support/campaigns/dogwood/driver.ex` lines 94-110 |
| run record | `artifacts/crossplane-dogwood/2026-09-18-79df522b/trials.jsonl`, this row's `notes` |

## The pre-registered catalogue entry, verbatim

```elixir
      %Variant{
        class: :t1,
        family: "F5",
        slug: "expired-explicit",
        drive: :f5_seats,
        params: %{@seats | execute_at: 31} |> Map.put(:expires_at, 30),
        expected_agreement: :disagree_dogwood_allows,
        expected_requisition: %{outcome: :prevented, denial_code: :approval_expired_at_execution},
        expected_dogwood: %{verdict: :allow, determining_rules: [@permit]},
        notes:
          "an explicit per-approval `expires_at` (+30 s) is invisible to the pack (its horizon is the constant TTL, G-174): Dogwood allows at +31, ours denies. The frozen Oracle's `expired?/1` reads the WALL clock, so its verdict here (`unauthorized`) is an artifact of the run date, not of +31 > +30 — recorded, not scored (Q5). The Coapprove is at +10, before the expiry (G-177 is not what this row measures)."
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

> an explicit per-approval `expires_at` (+30 s) is invisible to the pack (its horizon is the constant TTL, G-174): Dogwood allows at +31, ours denies. The frozen Oracle's `expired?/1` reads the WALL clock, so its verdict here (`unauthorized`) is an artifact of the run date, not of +31 > +30 — recorded, not scored (Q5). The Coapprove is at +10, before the expiry (G-177 is not what this row measures).
