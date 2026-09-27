# Provenance — `T1-F5-approver-revoked-001`

Every fact in this scenario's `facts.given` is transcribed from the text below. Nothing here
is written for the pack: each block is sliced verbatim out of a frozen commit, and this file
is inside the pack, so its digest is part of `reviewed_pack_sha256` and you can check the
transcription without leaving the review packet.

| | |
|---|---|
| pre-registration commit | `22216be` (the pack's `catalogue_frozen_at` pin) |
| catalogue | `test/support/campaigns/dogwood/catalogue.ex` lines 193-204 |
| drive | `test/support/campaigns/dogwood/driver.ex` lines 272-327 |
| run record | `artifacts/crossplane-dogwood/2026-09-18-79df522b/trials.jsonl`, this row's `notes` |

## The pre-registered catalogue entry, verbatim

```elixir
      %Variant{
        class: :t1,
        family: "F5",
        slug: "approver-revoked",
        drive: :f5_approver_revoked,
        params: Map.put(@seats, :revoke_standing_at, 50),
        expected_agreement: :disagree_dogwood_allows,
        expected_requisition: %{outcome: :prevented, denial_code: :approver_authority_changed},
        expected_dogwood: %{verdict: :allow, determining_rules: [@permit]},
        notes:
          "THE HEADLINE ROW (D-12 row 1). Two seats at +0/+10; at +50 the APPROVER's standing is revoked (membership removed -- the approval row is untouched, its status still approved); the execute at +100. MEASURED 2026-09-16, verbatim: steps `[{0, :create, {:ok, _}}, {0, :approve, :ok}, {10, :coapprove, :ok}, {50, :revoke_standing, :ok}, {100, :execute, :in_drive}]`; Requisition `outcome: :prevented, denial_code: :approver_authority_changed, evidence: :denied, oracle_verdict: :authorized` (the frozen Oracle has no standing check: recorded, not scored); Dogwood `verdict: :allow, determining_rules: [\"f5_two_person_execute\"]`. The seats are in the trace and nothing in it says the approver no longer stands: the pack reads the history of ACTS, ours re-reads the AUTHORITY behind each act at execution (`check_approver_authority/2`, W6 -- the current envelope, measured at A5's hand-back: no catch-all). NIST SP 800-207 tenet 4 (access determined by dynamic policy over the observable state of the requesting asset and the requester) and tenet 6 (authorization strictly enforced before access, re-evaluated as it is granted): a standing revoked after consent is a change of state the decision must see."
      },
```

## The module attributes it refers to, verbatim

```elixir
@permit "f5_two_person_execute"
@seats %{approve_at: 0, coapprove_at: 10, execute_at: 100}
```

## The drive `:f5_approver_revoked`, verbatim

```elixir
  defp build(:f5_approver_revoked, v, %Prepared{} = prepared, account, owner, run, key) do
    approve_at = Map.get(v.params, :approve_at, 0)
    coapprove_at = v.params.coapprove_at
    revoke_standing_at = v.params.revoke_standing_at
    execute_at = offset(v.params.execute_at)

    approver = Fixtures.coapprover(account, owner, key <> "-a")
    coapprover = Fixtures.coapprover(account, owner, key <> "-b")
    {request, idem, payload} = pending(account, run, key)

    at(approve_at)

    approved =
      Fixtures.ok!(
        Approvals.approve_request(request, approver, %{reason: "Primary"}),
        "#{key}/approve"
      )

    at(coapprove_at)

    Fixtures.ok!(
      Approvals.coapprove_request(approved, coapprover, %{reason: "Second"}),
      "#{key}/coapprove"
    )

    at(revoke_standing_at)

    membership =
      account.id
      |> Accounts.list_account_memberships()
      |> Enum.find(&(&1.user_id == approver.id))

    Fixtures.ok!(
      Accounts.remove_member(account, owner, membership.id),
      "#{key}/remove_member"
    )

    %Prepared{
      prepared
      | approval_ids: [approved.id],
        idempotency_keys: [idem],
        approved_hash: hash(payload),
        driven_payload: payload,
        steps: [
          {approve_at, :create, {:ok, request.id}},
          {approve_at, :approve, :ok},
          {coapprove_at, :coapprove, :ok},
          {revoke_standing_at, :revoke_standing, :ok},
          {execute_at, :execute, :in_drive}
        ],
        context:
          context(account, run, approved, idem, payload, payload, fn ->
            at(execute_at)
            execute(account, run, approved, idem, payload)
          end)
    }
```

## The run's own note for this row, verbatim

> THE HEADLINE ROW (D-12 row 1). Two seats at +0/+10; at +50 the APPROVER's standing is revoked (membership removed -- the approval row is untouched, its status still approved); the execute at +100. MEASURED 2026-09-16, verbatim: steps `[{0, :create, {:ok, _}}, {0, :approve, :ok}, {10, :coapprove, :ok}, {50, :revoke_standing, :ok}, {100, :execute, :in_drive}]`; Requisition `outcome: :prevented, denial_code: :approver_authority_changed, evidence: :denied, oracle_verdict: :authorized` (the frozen Oracle has no standing check: recorded, not scored); Dogwood `verdict: :allow, determining_rules: ["f5_two_person_execute"]`. The seats are in the trace and nothing in it says the approver no longer stands: the pack reads the history of ACTS, ours re-reads the AUTHORITY behind each act at execution (`check_approver_authority/2`, W6 -- the current envelope, measured at A5's hand-back: no catch-all). NIST SP 800-207 tenet 4 (access determined by dynamic policy over the observable state of the requesting asset and the requester) and tenet 6 (authorization strictly enforced before access, re-evaluated as it is granted): a standing revoked after consent is a change of state the decision must see.
