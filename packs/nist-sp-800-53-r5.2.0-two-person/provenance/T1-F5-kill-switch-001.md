# Provenance — `T1-F5-kill-switch-001`

Every fact in this scenario's `facts.given` is transcribed from the text below. Nothing here
is written for the pack: each block is sliced verbatim out of a frozen commit, and this file
is inside the pack, so its digest is part of `reviewed_pack_sha256` and you can check the
transcription without leaving the review packet.

| | |
|---|---|
| pre-registration commit | `22216be` (the pack's `catalogue_frozen_at` pin) |
| catalogue | `test/support/campaigns/dogwood/catalogue.ex` lines 205-216 |
| drive | `test/support/campaigns/dogwood/driver.ex` lines 332-360 |
| run record | `artifacts/crossplane-dogwood/2026-09-18-79df522b/trials.jsonl`, this row's `notes` |

## The pre-registered catalogue entry, verbatim

```elixir
      %Variant{
        class: :t1,
        family: "F5",
        slug: "kill-switch",
        drive: :f5_kill_switch,
        params: Map.put(@seats, :engage_at, 50),
        expected_agreement: :disagree_dogwood_allows,
        expected_requisition: %{outcome: :prevented, denial_code: :authority_hold},
        expected_dogwood: %{verdict: :allow, determining_rules: [@permit]},
        notes:
          "D-12 row 2. Two seats at +0/+10; at +50 the platform kill switch is engaged (the owner's `ENGAGE`, an authority hold over the whole plane); the execute at +100. MEASURED 2026-09-16, verbatim: steps `[..., {50, :engage_kill_switch, :ok}, {100, :execute, :in_drive}]`; Requisition `outcome: :prevented, denial_code: :authority_hold, evidence: :denied, oracle_verdict: :authorized` (the Oracle has no hold: recorded, not scored); Dogwood `verdict: :allow, determining_rules: [\"f5_two_person_execute\"]`. The hold is not an event in the approval's history; a pack whose evidence is the trace cannot see a plane-wide state that no trace line carries (the census's E5 class: a latched state is inexpressible as a windowed predicate). NIST SP 800-207 tenets 4 and 6: the enterprise's current posture is an input to every decision."
      },
```

## The module attributes it refers to, verbatim

```elixir
@permit "f5_two_person_execute"
@seats %{approve_at: 0, coapprove_at: 10, execute_at: 100}
```

## The drive `:f5_kill_switch`, verbatim

```elixir
  defp build(:f5_kill_switch, v, %Prepared{} = prepared, account, owner, run, key) do
    {approval, steps, idem, payload} =
      seats(Map.delete(v.params, :engage_at), account, owner, run, key, :distinct)

    engage_at = v.params.engage_at
    execute_at = offset(v.params.execute_at)

    at(engage_at)
    operator = AutonomousAgency.Access.platform_owner_emails() |> List.first()

    Fixtures.ok!(
      Platform.engage_kill_switch(operator, "ENGAGE", "Dogwood row: the kill switch"),
      "#{key}/engage_kill_switch"
    )

    %Prepared{
      prepared
      | approval_ids: [approval.id],
        idempotency_keys: [idem],
        approved_hash: hash(payload),
        driven_payload: payload,
        steps:
          steps ++ [{engage_at, :engage_kill_switch, :ok}, {execute_at, :execute, :in_drive}],
        context:
          context(account, run, approval, idem, payload, payload, fn ->
            at(execute_at)
            execute(account, run, approval, idem, payload)
          end)
    }
```

## The run's own note for this row, verbatim

> D-12 row 2. Two seats at +0/+10; at +50 the platform kill switch is engaged (the owner's `ENGAGE`, an authority hold over the whole plane); the execute at +100. MEASURED 2026-09-16, verbatim: steps `[..., {50, :engage_kill_switch, :ok}, {100, :execute, :in_drive}]`; Requisition `outcome: :prevented, denial_code: :authority_hold, evidence: :denied, oracle_verdict: :authorized` (the Oracle has no hold: recorded, not scored); Dogwood `verdict: :allow, determining_rules: ["f5_two_person_execute"]`. The hold is not an event in the approval's history; a pack whose evidence is the trace cannot see a plane-wide state that no trace line carries (the census's E5 class: a latched state is inexpressible as a windowed predicate). NIST SP 800-207 tenets 4 and 6: the enterprise's current posture is an input to every decision.
