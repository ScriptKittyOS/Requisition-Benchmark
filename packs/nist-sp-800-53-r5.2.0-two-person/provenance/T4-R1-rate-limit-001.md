# Provenance — `T4-R1-rate-limit-001`

Every fact in this scenario's `facts.given` is transcribed from the text below. Nothing here
is written for the pack: each block is sliced verbatim out of a frozen commit, and this file
is inside the pack, so its digest is part of `reviewed_pack_sha256` and you can check the
transcription without leaving the review packet.

| | |
|---|---|
| pre-registration commit | `22216be` (the pack's `catalogue_frozen_at` pin) |
| catalogue | `test/support/campaigns/dogwood/catalogue.ex` lines 372-383 |
| drive | `test/support/campaigns/dogwood/driver.ex` lines 469-506 |
| run record | `artifacts/crossplane-dogwood/2026-09-18-79df522b/trials.jsonl`, this row's `notes` |

## The pre-registered catalogue entry, verbatim

```elixir
      %Variant{
        class: :t4,
        family: "R1",
        slug: "rate-limit",
        drive: :r1_burst,
        params: @seats |> Map.put(:executes, 4) |> Map.put(:spacing, 60),
        expected_agreement: :disagree_dogwood_denies,
        expected_requisition: %{outcome: :allowed, denial_code: nil},
        expected_dogwood: %{verdict: :deny, determining_rules: [@burst]},
        notes:
          "four two-person-approved executes (four approvals, four keys — every seat at +0/+10, before any execute, so t is monotone) by one run agent at +100/+160/+220/+280, inside 10 m; subject the fourth: `rl_execute_burst` denies by name, our plane has no rate limit on the execute path (W3 has cooldown only) — the reverse-direction demo, by design."
      },
```

## The module attributes it refers to, verbatim

```elixir
@burst "rl_execute_burst"
@seats %{approve_at: 0, coapprove_at: 10, execute_at: 100}
```

## The drive `:r1_burst`, verbatim

```elixir
  defp build(:r1_burst, v, %Prepared{} = prepared, account, owner, run, key) do
    n = v.params.executes
    spacing = v.params.spacing
    execute_at = offset(v.params.execute_at)
    seat_params = Map.take(v.params, [:approve_at, :coapprove_at])

    # every primary seat at approve_at, THEN every second seat at coapprove_at, then the
    # executes: the trace stays monotone in t, which Dogwood reads by position (reds review, F4)
    primaries = Enum.map(1..n, &primary(seat_params, account, owner, run, "#{key}-#{&1}"))

    approvals =
      Enum.map(primaries, fn {approved, steps, idem, payload, k} ->
        {approved, steps ++ second(seat_params, approved, account, owner, k, :distinct), idem,
         payload}
      end)

    [{first, _, first_idem, first_payload} | _] = approvals

    drive = fn ->
      approvals
      |> Enum.with_index()
      |> Enum.reduce(nil, fn {{approval, _, idem, payload}, i}, _ ->
        at(execute_at + i * spacing)
        execute(account, run, approval, idem, payload)
      end)
    end

    %Prepared{
      prepared
      | approval_ids: Enum.map(approvals, fn {a, _, _, _} -> a.id end),
        idempotency_keys: Enum.map(approvals, fn {_, _, k, _} -> k end),
        approved_hash: hash(first_payload),
        driven_payload: first_payload,
        steps:
          Enum.flat_map(approvals, fn {_, s, _, _} -> s end) ++
            Enum.map(0..(n - 1), &{execute_at + &1 * spacing, :execute, :in_drive}),
        context: context(account, run, first, first_idem, first_payload, first_payload, drive)
    }
```

## The run's own note for this row, verbatim

> four two-person-approved executes (four approvals, four keys — every seat at +0/+10, before any execute, so t is monotone) by one run agent at +100/+160/+220/+280, inside 10 m; subject the fourth: `rl_execute_burst` denies by name, our plane has no rate limit on the execute path (W3 has cooldown only) — the reverse-direction demo, by design.
