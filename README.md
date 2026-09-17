# Requisition Bench

> v0.1.0 is a single pre-registered run: Requisition and Dogwood were driven through the same 28 scenarios, every prediction held, and the Dogwood half of every claim can be re-derived offline from this package; the Requisition half is the plane's own recorded evidence, inspectable but not re-executable here.

Measurements of **Requisition**, an authority control plane for autonomous agents: approvals bound to
frozen payload fingerprints, two-person seats, revocation, expiry, a hold, replay served from the
record. Each release is a run the plane was driven through, the report written from that run, and a
reader that lets you re-derive the checkable half of every claim offline.

**Release v0.1.0 — the Dogwood cross-plane run.** The plane and a reference policy engine,
[Dogwood](https://github.com/dogwood-policy/dogwood), were driven through the same 28 pre-registered
scenarios (two-person approval, expiry, revocation, replay, payload swaps, cross-scope, a burst) and
their verdicts compared row by row. The pre-registration, the agreement table, the disagreements and
what the run cannot show are in [`findings.md`](findings.md).

## What is here

| path | what |
|---|---|
| `runs/2026-09-17-49489219/` | the run: `run.json`, `trials.jsonl` (one record per scenario), `t2-provenance.json`, `pack/` (the Dogwood policy pack, its schemas, rules and manifest), `traces/` (one event trace per scenario), `SHA256SUMS` |
| `findings.md` | the report; every claim is followed by its source in brackets |
| `verify_dogwood_side.py` | the reader (Python 3, standard library, no network) |
| `README-verification.md` | how to run the reader, and which citations resolve in this repository |
| `pack-source/` | the pack's source: the rules, the expressiveness census (each rejected encoding with the validator's recorded output), the R1 exhibit, the fixture bundles as data |
| `PROVENANCE.md` | what this release is, what it is not, and the Dogwood commit it was measured against |
| `PACKAGE-SHA256SUMS`, `VERIFY.txt` | the sums over every file, and the reader's transcript from inside this package |

## Verify it yourself

Build [Dogwood](https://github.com/dogwood-policy/dogwood) at the pinned commit (`fa7a32370a642b32b54c73c16fd75bc88c847050`):

    git clone https://github.com/dogwood-policy/dogwood && cd dogwood && git checkout fa7a3237 && cargo build --release -p dogwood-cli

Then, from this repository:

    sha256sum -c PACKAGE-SHA256SUMS
    ./verify_dogwood_side.py runs/2026-09-17-49489219 --dogwood /path/to/dogwood/target/release/dogwood --pack-source pack-source

The last line is `VERIFY DOGWOOD SIDE: PASS` (317 checks): every trace replayed through Dogwood must give
the verdicts the record carries; the digests, the deny-provenance classes and the counts are
recomputed; every rejected encoding in the census must fail the validator with the recorded words.
Four independent builds of the pinned commit have given the same 28 verdicts.

## What you cannot re-run from here, stated

The Requisition side of every scenario — whether the plane refused, with which code, and the receipt
it wrote — is the plane's own recorded measurement. It is in `trials.jsonl` for inspection, and the
report says where each claim rests on it, but the plane's code and the harness that drove it are not
in this repository. The bench's own adjudicator (the "Requisition oracle"), its scenario spec and its
scoring are not in v0.1.0; they join at the first release that includes a run they judged.

## Citing

Cite the tag (`v0.1.0`), never the branch. `PROVENANCE.md` is frozen at each tag.
