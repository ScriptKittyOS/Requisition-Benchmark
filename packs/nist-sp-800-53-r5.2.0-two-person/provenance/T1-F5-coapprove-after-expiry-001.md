# Provenance — `T1-F5-coapprove-after-expiry-001`

Every fact in this scenario's `facts.given` is transcribed from the text below. Nothing here
is written for the pack: each block is sliced verbatim out of a frozen commit, and this file
is inside the pack, so its digest is part of `reviewed_pack_sha256` and you can check the
transcription without leaving the review packet.

| | |
|---|---|
| pre-registration commit | `22216be` (the pack's `catalogue_frozen_at` pin) |
| catalogue | `test/support/campaigns/dogwood/catalogue.ex` lines 217-228 |
| drive | `test/support/campaigns/dogwood/driver.ex` lines 365-389 |
| run record | `artifacts/crossplane-dogwood/2026-09-18-79df522b/trials.jsonl`, this row's `notes` |

## The pre-registered catalogue entry, verbatim

```elixir
      %Variant{
        class: :t1,
        family: "F5",
        slug: "coapprove-after-expiry",
        drive: :f5_coapprove_after_expiry,
        params: %{approve_at: 0, coapprove_at: :ttl_plus_one, execute_at: :ttl_plus_one},
        expected_agreement: :agree,
        expected_requisition: %{outcome: :prevented, denial_code: :approval_expired_at_execution},
        expected_dogwood: %{verdict: :deny, determining_rules: []},
        notes:
          "D-12 row 3 (pins G-177, after W6). The first seat at +0; the SECOND seat attempted at +TTL+1, past the first seat's authority window; the execute at +TTL+1. MEASURED 2026-09-16, verbatim: steps `[{0, :create, {:ok, _}}, {0, :approve, :ok}, {86401, :coapprove, {:error, :approval_expired}}, {86401, :execute, :in_drive}]` -- the countersign is REFUSED at the API (G-177's lift: `coapprove_request/3` refuses `:approval_expired` before the seat checks) so the trace carries ONE Approve and the Execute; Requisition `outcome: :prevented, denial_code: :approval_expired_at_execution, evidence: :denied, oracle_verdict: :unauthorized`; Dogwood `verdict: :deny, determining_rules: []` -- implicit: rule 00 finds one seat, and the window has closed on it. Both deny; the pack's reason is the missing second seat and the closed window, ours is the expiry named. NIST SP 800-207 tenet 6: a consent past its window is not consent."
      },
```

## The drive `:f5_coapprove_after_expiry`, verbatim

```elixir
  defp build(:f5_coapprove_after_expiry, v, %Prepared{} = prepared, account, owner, run, key) do
    {approved, steps, idem, payload, _key} =
      primary(Map.delete(v.params, :coapprove_at), account, owner, run, key)

    coapprove_at = offset(v.params.coapprove_at)
    execute_at = offset(v.params.execute_at)

    at(coapprove_at)
    co = Fixtures.coapprover(account, owner, key)
    coapproval = Approvals.coapprove_request(approved, co, %{reason: "Second, late"})

    %Prepared{
      prepared
      | approval_ids: [approved.id],
        idempotency_keys: [idem],
        approved_hash: hash(payload),
        driven_payload: payload,
        steps:
          steps ++ [{coapprove_at, :coapprove, coapproval}, {execute_at, :execute, :in_drive}],
        context:
          context(account, run, approved, idem, payload, payload, fn ->
            at(execute_at)
            execute(account, run, approved, idem, payload)
          end)
    }
```

## The run's own note for this row, verbatim

> D-12 row 3 (pins G-177, after W6). The first seat at +0; the SECOND seat attempted at +TTL+1, past the first seat's authority window; the execute at +TTL+1. MEASURED 2026-09-16, verbatim: steps `[{0, :create, {:ok, _}}, {0, :approve, :ok}, {86401, :coapprove, {:error, :approval_expired}}, {86401, :execute, :in_drive}]` -- the countersign is REFUSED at the API (G-177's lift: `coapprove_request/3` refuses `:approval_expired` before the seat checks) so the trace carries ONE Approve and the Execute; Requisition `outcome: :prevented, denial_code: :approval_expired_at_execution, evidence: :denied, oracle_verdict: :unauthorized`; Dogwood `verdict: :deny, determining_rules: []` -- implicit: rule 00 finds one seat, and the window has closed on it. Both deny; the pack's reason is the missing second seat and the closed window, ours is the expiry named. NIST SP 800-207 tenet 6: a consent past its window is not consent.
