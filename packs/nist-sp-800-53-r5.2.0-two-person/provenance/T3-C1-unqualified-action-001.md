# Provenance — `T3-C1-unqualified-action-001`

Every fact in this scenario's `facts.given` is transcribed from the text below. Nothing here
is written for the pack: each block is sliced verbatim out of a frozen commit, and this file
is inside the pack, so its digest is part of `reviewed_pack_sha256` and you can check the
transcription without leaving the review packet.

| | |
|---|---|
| pre-registration commit | `22216be` (the pack's `catalogue_frozen_at` pin) |
| catalogue | `test/support/campaigns/dogwood/catalogue.ex` lines 425-441 |
| drive | `test/support/campaigns/dogwood/driver.ex` lines 94-110 |
| run record | `artifacts/crossplane-dogwood/2026-09-18-79df522b/trials.jsonl`, this row's `notes` |

## The pre-registered catalogue entry, verbatim

```elixir
      %Variant{
        class: :t3,
        family: "C1",
        slug: "unqualified-action",
        drive: :f5_seats,
        params: @seats,
        trap: :t3c,
        expected_agreement: :disagree_dogwood_denies,
        expected_requisition: %{outcome: :allowed, denial_code: nil},
        expected_dogwood: %{
          verdict: :deny,
          determining_rules: [],
          deny_provenance: :undeclared_deny
        },
        notes:
          "T3c: the decision line's action rendered unqualified (`Action::\"Execute\"`): exact structural matching, no rule matches. MEASURED: deny [] and the binary is silent; the replayer names the unqualified line (`undeclared`). Ours: W5 -- an operation that is not the canonical identity is a LOUD `:operation_near_miss` (`traps_test` T3's equivalent), never a silent non-match."
      },
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

> T3c: the decision line's action rendered unqualified (`Action::"Execute"`): exact structural matching, no rule matches. MEASURED: deny [] and the binary is silent; the replayer names the unqualified line (`undeclared`). Ours: W5 -- an operation that is not the canonical identity is a LOUD `:operation_near_miss` (`traps_test` T3's equivalent), never a silent non-match.
