# Provenance — `T1-F4-cross-scope-001`

Every fact in this scenario's `facts.given` is transcribed from the text below. Nothing here
is written for the pack: each block is sliced verbatim out of a frozen commit, and this file
is inside the pack, so its digest is part of `reviewed_pack_sha256` and you can check the
transcription without leaving the review packet.

| | |
|---|---|
| pre-registration commit | `22216be` (the pack's `catalogue_frozen_at` pin) |
| catalogue | `test/support/campaigns/dogwood/catalogue.ex` lines 230-241 |
| drive | `test/support/campaigns/dogwood/driver.ex` lines 394-417 |
| run record | `artifacts/crossplane-dogwood/2026-09-18-79df522b/trials.jsonl`, this row's `notes` |

## The pre-registered catalogue entry, verbatim

```elixir
      %Variant{
        class: :t1,
        family: "F4",
        slug: "cross-scope",
        drive: :f4_cross_scope,
        params: @seats,
        expected_agreement: :agree,
        expected_requisition: %{outcome: :prevented, denial_code: :account_scope_mismatch},
        expected_dogwood: %{verdict: :deny, determining_rules: []},
        notes:
          "D-12 row 4. Both seats under account A; the execute under account B's run carrying A's approval id, key and payload. MEASURED 2026-09-16 (twice). BEFORE G-187 (`df900b5`): the plane refused RAW -- `{:error, :account_scope_mismatch}` from `resolve_tool_scope/6` before the door, NO tool_calls row, NO audit event; `RequisitionSide` read `outcome: :prevented, denial_code: nil, evidence: :absent, oracle_verdict: :unauthorized`; the exported trace of EITHER run had no Execute line and Dogwood `verdicts: []` -- the unreceipted-refusal class (G-089's family) on the one row whose subject is the refusal; G-187 filed and fixed first. AFTER G-187: the refusal is typed and recorded under the CALLER's run and account (the subject's chain is B's -- `Prepared.agent_run_id` is B's run): B's evidence `{:denied, :account_scope_mismatch}`, the row's `request` the disagreement (`run_account_id` = B, `payload_account_id` = A), its `policy_result` bound to A's approval id and hash; B's trace `[Execute +100]`, Dogwood `verdict: :deny, determining_rules: []`; A's trace `[Approve +0, Coapprove +10]`, no Execute, `verdicts: []`. THE FINDING: Dogwood's deny is IMPLICIT and for the wrong reason -- B's chain has no seats, so rule 00 cannot permit; the exported bag carries NO scope (`scope(principal, resource: Req::Approval::id)`, no account on any line), so the pack CANNOT bind an Execute to the account its seats were given under. Probed (not evidence, attacker-authored): A's seats and B's Execute spliced into ONE trace -> `verdict: :allow, determining_rules: [\"f5_two_person_execute\"]`. The pack as written did not bind scope; whether it gains a scope pin (an account rendered on every line by the exporter, a rule pinning the Execute's account to the seats') is the OWNER's decision, held open at the pre-registration hand-back. Ours: the run's, the caller's and the payload's account must agree before anything else runs. NIST SP 800-207 tenet 4 (the requesting asset's identity and scope are inputs) and tenet 6 (enforced before access)."
      },
```

## The module attributes it refers to, verbatim

```elixir
@seats %{approve_at: 0, coapprove_at: 10, execute_at: 100}
```

## The drive `:f4_cross_scope`, verbatim

```elixir
  defp build(:f4_cross_scope, v, %Prepared{} = prepared, account, owner, run, key) do
    {approval, steps, idem, payload} = seats(v.params, account, owner, run, key, :distinct)
    execute_at = offset(v.params.execute_at)
    %{account: other} = Fixtures.account(key <> "-b")
    other_run = Fixtures.agent_run(other)

    # the subject's chain is the CALLER's (run B under account B): since G-187 the plane records
    # the scope refusal there, under the account it can be held to; the seats stay in A's chain
    # and A's chain never sees the attempt (measured 2026-09-16, before and after G-187)
    %Prepared{
      prepared
      | agent_run_id: other_run.id,
        account_id: other.id,
        approval_ids: [approval.id],
        idempotency_keys: [idem],
        approved_hash: hash(payload),
        driven_payload: payload,
        steps: steps ++ [{execute_at, :execute_cross_scope, :in_drive}],
        context:
          context(other, other_run, approval, idem, payload, payload, fn ->
            at(execute_at)
            execute(other, other_run, approval, idem, payload)
          end)
    }
```

## The run's own note for this row, verbatim

> D-12 row 4. Both seats under account A; the execute under account B's run carrying A's approval id, key and payload. MEASURED 2026-09-16 (twice). BEFORE G-187 (`df900b5`): the plane refused RAW -- `{:error, :account_scope_mismatch}` from `resolve_tool_scope/6` before the door, NO tool_calls row, NO audit event; `RequisitionSide` read `outcome: :prevented, denial_code: nil, evidence: :absent, oracle_verdict: :unauthorized`; the exported trace of EITHER run had no Execute line and Dogwood `verdicts: []` -- the unreceipted-refusal class (G-089's family) on the one row whose subject is the refusal; G-187 filed and fixed first. AFTER G-187: the refusal is typed and recorded under the CALLER's run and account (the subject's chain is B's -- `Prepared.agent_run_id` is B's run): B's evidence `{:denied, :account_scope_mismatch}`, the row's `request` the disagreement (`run_account_id` = B, `payload_account_id` = A), its `policy_result` bound to A's approval id and hash; B's trace `[Execute +100]`, Dogwood `verdict: :deny, determining_rules: []`; A's trace `[Approve +0, Coapprove +10]`, no Execute, `verdicts: []`. THE FINDING: Dogwood's deny is IMPLICIT and for the wrong reason -- B's chain has no seats, so rule 00 cannot permit; the exported bag carries NO scope (`scope(principal, resource: Req::Approval::id)`, no account on any line), so the pack CANNOT bind an Execute to the account its seats were given under. Probed (not evidence, attacker-authored): A's seats and B's Execute spliced into ONE trace -> `verdict: :allow, determining_rules: ["f5_two_person_execute"]`. The pack as written did not bind scope; whether it gains a scope pin (an account rendered on every line by the exporter, a rule pinning the Execute's account to the seats') is the OWNER's decision, held open at the pre-registration hand-back. Ours: the run's, the caller's and the payload's account must agree before anything else runs. NIST SP 800-207 tenet 4 (the requesting asset's identity and scope are inputs) and tenet 6 (enforced before access). AMENDED 2026-09-17 (D-18, R1; the moduledoc): the bag now carries `scope` and rule 00 pins it on both seats -- re-pre-registered `agree`, both deny, the same cell; the splice denies under the amended pack (`_pack/spliced-seats-other-scope-deny`), and the first pack's allow is the exhibit `pack/census/R1_scope_unbound_first_pack/` (G-191).
