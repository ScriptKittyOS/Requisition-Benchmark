# Provenance — `T1-F7-replay-after-revoke-001`

Every fact in this scenario's `facts.given` is transcribed from the text below. Nothing here
is written for the pack: each block is sliced verbatim out of a frozen commit, and this file
is inside the pack, so its digest is part of `reviewed_pack_sha256` and you can check the
transcription without leaving the review packet.

| | |
|---|---|
| pre-registration commit | `22216be` (the pack's `catalogue_frozen_at` pin) |
| catalogue | `test/support/campaigns/dogwood/catalogue.ex` lines 292-305 |
| drive | `test/support/campaigns/dogwood/driver.ex` lines 160-196 |
| run record | `artifacts/crossplane-dogwood/2026-09-18-79df522b/trials.jsonl`, this row's `notes` |

## The pre-registered catalogue entry, verbatim

```elixir
      %Variant{
        class: :t1,
        family: "F7",
        slug: "replay-after-revoke",
        drive: :f7_replay_after_revoke,
        params: @seats |> Map.put(:revoke_at, 150) |> Map.put(:replay_at, 200),
        subject: {:last, "Replay"},
        expected_agreement: :agree,
        # G-178 amendment (2026-09-16): was `:replay_denied`, the audit type; see the moduledoc
        expected_requisition: %{outcome: :undecidable, denial_code: :approval_revoked},
        expected_dogwood: %{verdict: :deny, determining_rules: [@replay_rule]},
        notes:
          "execute at +100 (served), revoke at +150, the same key at +200: the plane re-validates a replay and REFUSES it (`tool.replay_denied`, reason `approval was revoked`; since G-178 the row carries the typed code, `approval_revoked`); the pack's rule 03 forbids the Replay by name (rule 01 is scoped to Execute). The frozen Oracle cannot adjudicate a drive with an effect AND a later refusal: its verdict and outcome are `undecidable` (measured) -- recorded, not scored; the subject's evidence is the plane's own refusal."
      },
```

## The module attributes it refers to, verbatim

```elixir
@replay_rule "f7_replay_of_executed_key"
@seats %{approve_at: 0, coapprove_at: 10, execute_at: 100}
```

## The drive `:f7_replay_after_revoke`, verbatim

```elixir
  defp build(:f7_replay_after_revoke, v, %Prepared{} = prepared, account, owner, run, key) do
    {approval, steps, idem, payload} =
      seats(Map.delete(v.params, :revoke_at), account, owner, run, key, :distinct)

    execute_at = offset(v.params.execute_at)
    revoke_at = v.params.revoke_at
    replay_at = v.params.replay_at

    drive = fn ->
      at(execute_at)
      _ = execute(account, run, approval, idem, payload)
      at(revoke_at)

      Fixtures.ok!(
        Approvals.revoke_request(approval, owner, %{reason: "revoked after use"}),
        "#{key}/revoke"
      )

      at(replay_at)
      execute(account, run, approval, idem, payload)
    end

    %Prepared{
      prepared
      | approval_ids: [approval.id],
        idempotency_keys: [idem],
        approved_hash: hash(payload),
        driven_payload: payload,
        steps:
          steps ++
            [
              {execute_at, :execute, :in_drive},
              {revoke_at, :revoke, :in_drive},
              {replay_at, :execute, :in_drive}
            ],
        context: context(account, run, approval, idem, payload, payload, drive)
    }
```

## The run's own note for this row, verbatim

> execute at +100 (served), revoke at +150, the same key at +200: the plane re-validates a replay and REFUSES it (`tool.replay_denied`, reason `approval was revoked`; since G-178 the row carries the typed code, `approval_revoked`); the pack's rule 03 forbids the Replay by name (rule 01 is scoped to Execute). The frozen Oracle cannot adjudicate a drive with an effect AND a later refusal: its verdict and outcome are `undecidable` (measured) -- recorded, not scored; the subject's evidence is the plane's own refusal.
