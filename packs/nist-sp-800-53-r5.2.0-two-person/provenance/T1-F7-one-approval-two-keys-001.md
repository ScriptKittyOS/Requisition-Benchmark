# Provenance — `T1-F7-one-approval-two-keys-001`

Every fact in this scenario's `facts.given` is transcribed from the text below. Nothing here
is written for the pack: each block is sliced verbatim out of a frozen commit, and this file
is inside the pack, so its digest is part of `reviewed_pack_sha256` and you can check the
transcription without leaving the review packet.

| | |
|---|---|
| pre-registration commit | `22216be` (the pack's `catalogue_frozen_at` pin) |
| catalogue | `test/support/campaigns/dogwood/catalogue.ex` lines 306-318 |
| drive | `test/support/campaigns/dogwood/driver.ex` lines 421-444 |
| run record | `artifacts/crossplane-dogwood/2026-09-18-79df522b/trials.jsonl`, this row's `notes` |

## The pre-registered catalogue entry, verbatim

```elixir
      %Variant{
        class: :t1,
        family: "F7",
        slug: "one-approval-two-keys",
        drive: :f7_two_keys,
        params: @seats |> Map.put(:spacing, 10),
        subject: {:last, "Execute"},
        expected_agreement: :disagree_dogwood_allows,
        expected_requisition: %{outcome: :undecidable, denial_code: :idempotency_key_mismatch},
        expected_dogwood: %{verdict: :allow, determining_rules: [@permit]},
        notes:
          "D-12 row 5 (measured first as a single-trial rehearsal, as ruled). One approval, two seats; the execute at +100 under the approved key (served), then the IDENTICAL payload at +110 under a SECOND key. MEASURED 2026-09-16, verbatim: steps `[..., {100, :execute, :in_drive}, {110, :execute_second_key, :in_drive}]`; Requisition `outcome: :undecidable, denial_code: :idempotency_key_mismatch, evidence: :denied, oracle_verdict: :undecidable` (the frozen Oracle cannot adjudicate a drive with an effect AND a later refusal, as on `replay-after-revoke`: recorded, not scored; the subject's evidence is the plane's own refusal of the second key -- the approval binds ONE key, no new G-id); Dogwood index 0 `allow [\"f5_two_person_execute\"]`, index 1 (the subject) `allow [\"f5_two_person_execute\"]` -- rule 00 pins approval id and payload hash, both unchanged; rule 02 counts PER KEY and the second key's count is 1. THE FINDING: the pack allows N effects under one approval as long as each carries a fresh key; a per-key count is not a per-approval count. NIST SP 800-207 tenet 6 (per-request authorization) and tenet 4: one consent, one effect."
      },
```

## The module attributes it refers to, verbatim

```elixir
@permit "f5_two_person_execute"
@seats %{approve_at: 0, coapprove_at: 10, execute_at: 100}
```

## The drive `:f7_two_keys`, verbatim

```elixir
  defp build(:f7_two_keys, v, %Prepared{} = prepared, account, owner, run, key) do
    {approval, steps, idem, payload} = seats(v.params, account, owner, run, key, :distinct)
    execute_at = offset(v.params.execute_at)
    second_at = execute_at + v.params.spacing
    second_key = idem <> "-2"

    drive = fn ->
      at(execute_at)
      _ = execute(account, run, approval, idem, payload)
      at(second_at)
      execute(account, run, approval, second_key, payload)
    end

    %Prepared{
      prepared
      | approval_ids: [approval.id],
        idempotency_keys: [idem, second_key],
        approved_hash: hash(payload),
        driven_payload: payload,
        steps:
          steps ++
            [{execute_at, :execute, :in_drive}, {second_at, :execute_second_key, :in_drive}],
        context: context(account, run, approval, second_key, payload, payload, drive)
    }
```

## The run's own note for this row, verbatim

> D-12 row 5 (measured first as a single-trial rehearsal, as ruled). One approval, two seats; the execute at +100 under the approved key (served), then the IDENTICAL payload at +110 under a SECOND key. MEASURED 2026-09-16, verbatim: steps `[..., {100, :execute, :in_drive}, {110, :execute_second_key, :in_drive}]`; Requisition `outcome: :undecidable, denial_code: :idempotency_key_mismatch, evidence: :denied, oracle_verdict: :undecidable` (the frozen Oracle cannot adjudicate a drive with an effect AND a later refusal, as on `replay-after-revoke`: recorded, not scored; the subject's evidence is the plane's own refusal of the second key -- the approval binds ONE key, no new G-id); Dogwood index 0 `allow ["f5_two_person_execute"]`, index 1 (the subject) `allow ["f5_two_person_execute"]` -- rule 00 pins approval id and payload hash, both unchanged; rule 02 counts PER KEY and the second key's count is 1. THE FINDING: the pack allows N effects under one approval as long as each carries a fresh key; a per-key count is not a per-approval count. NIST SP 800-207 tenet 6 (per-request authorization) and tenet 4: one consent, one effect.
