# Requisition Bench

> v0.1.0 is a single pre-registered run: Requisition and Dogwood were driven through the same 28 scenarios, every prediction held, and the Dogwood half of every claim can be re-derived offline from this package; the Requisition half is the plane's own recorded evidence, inspectable but not re-executable here.
>
> v0.2.0 is the same 28 scenarios run again, with one addition: each scored row ships the receipt chain the plane signed for its verdict under a published key, so the Requisition half of every claim is now checkable for provenance — what the plane signed, hash-chained, under `evaluation_ed25519_v1` — though still not re-executable. Every tally is v0.1.0's.

Measurements of **Requisition**, an authority control plane for autonomous agents: approvals bound to
frozen payload fingerprints, two-person seats, revocation, expiry, a hold, replay served from the
record. Each release is a run the plane was driven through, the report written from that run, and a
reader that lets you re-derive the checkable half of every claim offline.

**Release v0.1.0 — the Dogwood cross-plane run.** The plane and a reference policy engine,
[Dogwood](https://github.com/dogwood-policy/dogwood), were driven through the same 28 pre-registered
scenarios (two-person approval, expiry, revocation, replay, payload swaps, cross-scope, a burst) and
their verdicts compared row by row. The pre-registration, the agreement table, the disagreements and
what the run cannot show are in [`findings.md`](findings.md).

**Release v0.2.0 — the same run, signed.** The same 28 scenarios, the same Dogwood commit and
policy pack, a new run of the plane (`runs/2026-09-18-79df522b/`). On every row the agreement,
the Dogwood verdict, the plane's status and its refusal code are identical to v0.1.0's. What is
new: `receipts/` (one file per row: the plane's signed receipt chain for the row's subject event,
and the redacted event it commits to) and `registry-used.json` (the key id, its public key and the
commit of the published [HolyTrinity-Benchmark](https://github.com/ScriptKittyOS/HolyTrinity-Benchmark)
registry the run was checked against). The reader's step 7 verifies them with that repository's
public `verify_receipt.py` and registry — obtained from there, never from here — and fails closed.
Section h of [`findings.md`](findings.md) is the v0.2.0 report; sections a–g are v0.1.0's, unchanged.

## What is here

| path | what |
|---|---|
| `runs/2026-09-17-49489219/` | v0.1.0's run: `run.json`, `trials.jsonl` (one record per scenario), `t2-provenance.json`, `pack/` (the Dogwood policy pack, its schemas, rules and manifest), `traces/` (one event trace per scenario), `SHA256SUMS` |
| `runs/2026-09-18-79df522b/` | v0.2.0's run: the same files, plus `receipts/` (one file per scored row: the plane's signed receipt chain and the redacted subject event) and `registry-used.json` (the published key and registry commit it was checked against) |
| `findings.md` | the report; every claim is followed by its source in brackets |
| `verify_dogwood_side.py` | the reader (Python 3, standard library, no network) |
| `README-verification.md` | how to run the reader, and which citations resolve in this repository |
| `pack-source/` | the pack's source: the rules, the expressiveness census (each rejected encoding with the validator's recorded output), the R1 exhibit, the fixture bundles as data |
| `PACKS.md` | the contract a pack author writes against (schema, events, horizon, traces, rule files), how to compare a pack with the plane offline, and why a foreign pack is a new pre-registration and a new run |
| `PROVENANCE.md` | what this release is, what it is not, and the Dogwood commit it was measured against |
| `PACKAGE-SHA256SUMS`, `VERIFY.txt`, `VERIFY-v0.1.0.txt` | the sums over every file (except themselves and the transcripts), and the reader's transcripts from inside this repository: v0.2.0's run with step 7, v0.1.0's run read by steps 1–6 |

## Verify it yourself

Build [Dogwood](https://github.com/dogwood-policy/dogwood) at the pinned commit (`fa7a32370a642b32b54c73c16fd75bc88c847050`):

    git clone https://github.com/dogwood-policy/dogwood && cd dogwood && git checkout fa7a3237 && cargo build --release -p dogwood-cli

Clone [HolyTrinity-Benchmark](https://github.com/ScriptKittyOS/HolyTrinity-Benchmark) for the public receipt
verifier and the evaluation key registry (`receipt-verification/verifier/verify_receipt.py`,
`receipt-verification/keys/evaluation-registry.json`) — from that repository, never from a copy that
arrived with the evidence. Then, from this repository:

    sha256sum -c PACKAGE-SHA256SUMS
    ./verify_dogwood_side.py runs/2026-09-18-79df522b --dogwood /path/to/dogwood/target/release/dogwood --pack-source pack-source \
        --verifier /path/to/HolyTrinity-Benchmark/receipt-verification/verifier/verify_receipt.py \
        --registry /path/to/HolyTrinity-Benchmark/receipt-verification/keys/evaluation-registry.json

The last line is `VERIFY DOGWOOD SIDE: PASS` (1169 checks): every trace replayed through Dogwood must give
the verdicts the record carries; the digests, the deny-provenance classes and the counts are
recomputed; every rejected encoding in the census must fail the validator with the recorded words;
and every row's receipts verify under the registry you supplied — signature, chain, the signed
status and refusal code against the row in `trials.jsonl`. `registry-used.json` must name the
registry you supplied. For v0.1.0's run, `runs/2026-09-17-49489219`, the same command reads
"no receipts/ in this run" at step 7 and passes on steps 1–6 (317 checks).
Four independent builds of the pinned commit have given the same 28 verdicts.

**The epoch.** The campaign pins its clock: every instant in a trace is an epoch plus the row's
offset, which is what makes two runs byte-identical. v0.1.0's traces use epoch `2026-01-01T00:00:00Z`.
v0.2.0's use `2026-09-06T00:00:00Z`, the earliest midnight inside the evaluation key's signing
window (`evaluation_ed25519_v1` is valid from `2026-09-05T00:07:58Z`), so the receipts fall inside
it and the public verifier can judge them; offsets, windows and verdicts are unchanged, and the
row-by-row identity of the two runs' verdicts is the measurement of that.

## What you cannot re-run from here, stated

The Requisition side of every scenario — whether the plane refused, and with which code — is the
plane's own recorded measurement. It is in `trials.jsonl` for inspection, and from v0.2.0 each row's
receipts show that the status and code there are what the plane signed, under a published key,
hash-chained. That is provenance, not correctness: the plane's code and the harness that drove it
are not in this repository, so whether it *should* have refused is the pre-registration's and the
report's argument, not something you can run. The bench's own adjudicator (the "Requisition oracle"), its scenario spec and its
scoring are not in v0.1.0; they join at the first release that includes a run they judged.

## Citing

Cite a tag (`v0.1.0`, `v0.2.0`), never the branch. `PROVENANCE.md` is frozen at each tag.

**A note on v0.1.0's checksums.** At the `v0.1.0` tag, `sha256sum -c PACKAGE-SHA256SUMS` fails: the
sums were taken over the package before its run directory was laid under `runs/`, and
`README-verification.md` was edited after the sums. The files themselves are what the tag says; the
run directory's own `SHA256SUMS` verifies, and `VERIFY.txt` at the tag is the reader's transcript
from this layout. From v0.2.0 the sums are taken over the repository as laid out.
