# Provenance — `T1-F7-replay-2-001`

Every fact in this scenario's `facts.given` is transcribed from the text below. Nothing here
is written for the pack: each block is sliced verbatim out of a frozen commit, and this file
is inside the pack, so its digest is part of `reviewed_pack_sha256` and you can check the
transcription without leaving the review packet.

| | |
|---|---|
| pre-registration commit | `22216be` (the pack's `catalogue_frozen_at` pin) |
| catalogue | `test/support/campaigns/dogwood/catalogue.ex` lines 243-255 |
| drive | `test/support/campaigns/dogwood/driver.ex` lines 134-155 |
| run record | `artifacts/crossplane-dogwood/2026-09-18-79df522b/trials.jsonl`, this row's `notes` |

## The pre-registered catalogue entry, verbatim

```elixir
      %Variant{
        class: :t1,
        family: "F7",
        slug: "replay-2",
        drive: :f7_replay,
        params: @seats |> Map.put(:executes, 2) |> Map.put(:spacing, 10),
        subject: {:last, "Replay"},
        expected_agreement: :agree,
        expected_requisition: %{outcome: :allowed, denial_code: :replayed},
        expected_dogwood: %{verdict: :deny, determining_rules: [@replay_rule]},
        notes:
          "two executes, same key, 10 s apart (execute_at + spacing): the plane serves the second from the record (tool.replayed, no second effect) — the trace carries ONE Replay event whatever N (G-141); the pack forbids a Replay of an executed key by name. The Oracle's outcome is `allowed` for the run (the first execute's effect); the subject's evidence is `:replayed`."
      },
```

## The module attributes it refers to, verbatim

```elixir
@replay_rule "f7_replay_of_executed_key"
@seats %{approve_at: 0, coapprove_at: 10, execute_at: 100}
```

## The drive `:f7_replay`, verbatim

```elixir
  defp build(:f7_replay, v, %Prepared{} = prepared, account, owner, run, key) do
    {approval, steps, idem, payload} = seats(v.params, account, owner, run, key, :distinct)
    execute_at = offset(v.params.execute_at)
    n = v.params.executes
    spacing = v.params.spacing

    drive = fn ->
      Enum.reduce(1..n, nil, fn i, _ ->
        at(execute_at + (i - 1) * spacing)
        execute(account, run, approval, idem, payload)
      end)
    end

    %Prepared{
      prepared
      | approval_ids: [approval.id],
        idempotency_keys: [idem],
        approved_hash: hash(payload),
        driven_payload: payload,
        steps: steps ++ Enum.map(1..n, &{execute_at + (&1 - 1) * spacing, :execute, :in_drive}),
        context: context(account, run, approval, idem, payload, payload, drive)
    }
```

## The run's own note for this row, verbatim

> two executes, same key, 10 s apart (execute_at + spacing): the plane serves the second from the record (tool.replayed, no second effect) — the trace carries ONE Replay event whatever N (G-141); the pack forbids a Replay of an executed key by name. The Oracle's outcome is `allowed` for the run (the first execute's effect); the subject's evidence is `:replayed`.
