# Provenance — `T1-F7-retry-after-refusal-001`

Every fact in this scenario's `facts.given` is transcribed from the text below. Nothing here
is written for the pack: each block is sliced verbatim out of a frozen commit, and this file
is inside the pack, so its digest is part of `reviewed_pack_sha256` and you can check the
transcription without leaving the review packet.

| | |
|---|---|
| pre-registration commit | `22216be` (the pack's `catalogue_frozen_at` pin) |
| catalogue | `test/support/campaigns/dogwood/catalogue.ex` lines 319-331 |
| drive | `test/support/campaigns/dogwood/driver.ex` lines 203-266 |
| run record | `artifacts/crossplane-dogwood/2026-09-18-79df522b/trials.jsonl`, this row's `notes` |

## The pre-registered catalogue entry, verbatim

```elixir
      %Variant{
        class: :t1,
        family: "F7",
        slug: "retry-after-refusal",
        drive: :f7_retry_after_refusal,
        params: %{attempt_at: 0, approve_at: 10, coapprove_at: 20, execute_at: 100},
        subject: {:last, "Execute"},
        expected_agreement: :disagree_dogwood_denies,
        expected_requisition: %{outcome: :allowed, denial_code: nil},
        expected_dogwood: %{verdict: :deny, determining_rules: [@once_per_key]},
        notes:
          "PRE-REGISTERED FROM THE MEASUREMENT (2026-09-16, D-17 item 4, after G-185 lifted; the sixth added row). The agent attempts at +0 BEFORE any seat (refused by the plane: `witness_unsatisfied`, recorded under the action's key and not consuming it -- REQ-135), the two seats are taken at +10/+20, the same key executes at +100. MEASURED, verbatim: Requisition `outcome: :allowed, denial_code: nil, oracle_verdict: :authorized, evidence: :succeeded` (the Oracle: \"1 matching effect(s); effect observed; a valid in-scope unexpired approval bound to payload_hash ... matched\"; the run's `proof_state` reads `manual_review_required` from the refused attempt's invariant records -- recorded, not scored); Dogwood: index 0 (the refused attempt, +0) `deny []`, index 1 (the retry, +100) `deny` with determining_rules `[\"f7_execute_once_per_key\"]` -- rule 02's self-inclusive per-key count reached 2 at the retry because the REFUSED Execute::request at +0 is in the count. THE FINDING: a per-key attempt count cannot distinguish a served effect from a refused attempt; the plane distinguishes them (a refusal never consumes the key), the pack cannot express the distinction (its bag carries no outcome). NIST SP 800-207 tenet 4 (access determined by dynamic policy, including the observable state of the requesting asset) and tenet 6 (authorization strictly enforced before access, and re-evaluated) -- the retry is a fresh evaluation under fresh authority."
      },
```

## The module attributes it refers to, verbatim

```elixir
@once_per_key "f7_execute_once_per_key"
```

## The drive `:f7_retry_after_refusal`, verbatim

```elixir
  defp build(:f7_retry_after_refusal, v, %Prepared{} = prepared, account, owner, run, key) do
    attempt_at = Map.get(v.params, :attempt_at, 0)
    approve_at = v.params.approve_at
    coapprove_at = v.params.coapprove_at
    execute_at = offset(v.params.execute_at)

    idem = "dogwood-#{key}"
    payload = %{account_id: account.id, credential: "rotate", email: "dogwood-#{key}@example.com"}
    at(attempt_at)

    request =
      Fixtures.ok!(
        Approvals.create_request(%{
          account_id: account.id,
          agent_run_id: run.id,
          approval_type: "credential_change",
          action_provider: Atom.to_string(@provider),
          action_operation: Atom.to_string(@operation),
          action_idempotency_key: idem,
          subject: "Rotate credential",
          reason: "Dogwood #{key}",
          metadata: %{"payload_hash" => hash(payload)}
        }),
        "#{key}/create_request"
      )

    # the premature attempt: refused by the plane, recorded verbatim (never unwrapped)
    attempt = execute(account, run, request, idem, payload)

    at(approve_at)

    approved =
      Fixtures.ok!(
        Approvals.approve_request(request, owner, %{reason: "Primary"}),
        "#{key}/approve"
      )

    at(coapprove_at)
    co = Fixtures.coapprover(account, owner, key)

    Fixtures.ok!(
      Approvals.coapprove_request(approved, co, %{reason: "Second"}),
      "#{key}/coapprove"
    )

    %Prepared{
      prepared
      | approval_ids: [approved.id],
        idempotency_keys: [idem],
        approved_hash: hash(payload),
        driven_payload: payload,
        steps: [
          {attempt_at, :create, {:ok, request.id}},
          {attempt_at, :execute_refused, attempt},
          {approve_at, :approve, :ok},
          {coapprove_at, :coapprove, :ok},
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

> PRE-REGISTERED FROM THE MEASUREMENT (2026-09-16, D-17 item 4, after G-185 lifted; the sixth added row). The agent attempts at +0 BEFORE any seat (refused by the plane: `witness_unsatisfied`, recorded under the action's key and not consuming it -- REQ-135), the two seats are taken at +10/+20, the same key executes at +100. MEASURED, verbatim: Requisition `outcome: :allowed, denial_code: nil, oracle_verdict: :authorized, evidence: :succeeded` (the Oracle: "1 matching effect(s); effect observed; a valid in-scope unexpired approval bound to payload_hash ... matched"; the run's `proof_state` reads `manual_review_required` from the refused attempt's invariant records -- recorded, not scored); Dogwood: index 0 (the refused attempt, +0) `deny []`, index 1 (the retry, +100) `deny` with determining_rules `["f7_execute_once_per_key"]` -- rule 02's self-inclusive per-key count reached 2 at the retry because the REFUSED Execute::request at +0 is in the count. THE FINDING: a per-key attempt count cannot distinguish a served effect from a refused attempt; the plane distinguishes them (a refusal never consumes the key), the pack cannot express the distinction (its bag carries no outcome). NIST SP 800-207 tenet 4 (access determined by dynamic policy, including the observable state of the requesting asset) and tenet 6 (authorization strictly enforced before access, and re-evaluated) -- the retry is a fresh evaluation under fresh authority.
