# Provenance

> v0.1.0 is a single pre-registered run: Requisition and Dogwood were driven through the same 28 scenarios, every prediction held, and the Dogwood half of every claim can be re-derived offline from this package; the Requisition half is the plane's own recorded evidence, inspectable but not re-executable here.
>
> v0.2.0 is the same 28 scenarios run again, with one addition: each scored row ships the receipt chain the plane signed for its verdict under a published key, so the Requisition half of every claim is now checkable for provenance — what the plane signed, hash-chained, under `evaluation_ed25519_v1` — though still not re-executable. Every tally is v0.1.0's.

## v0.2.0 (2026-09-18)

**What this is.** The Dogwood cross-plane campaign run `2026-09-18-79df522b` of Requisition: the same
28 pre-registered scenarios, the same Dogwood commit and policy pack as v0.1.0, a new run of the
plane that ships, per scored row, the receipt chain the plane signed for the row's subject event
and the redacted event it commits to. Assembled by `bin/campaign-package` from the private tree at
`033dd1533ae2f3d7e0dbb87bb3ee5d68ea6c8c32` (the run itself on `79df522bb6125b0a87629f89f50dd9a94b743d96`,
qualified: the full gate, filed-reds, ten name-identical full-suite runs in a detached worktree,
a second run byte-identical on `trials.jsonl` and `t2-provenance.json`) and proved before it left:
the reader ran from inside this repository in an empty environment with the public verifier and
registry supplied from a HolyTrinity-Benchmark checkout at `d19945c5647d8e59b18bc7ec242ca39fbd2162ff`
(`VERIFY.txt`, last line `VERIFY DOGWOOD SIDE: PASS`, 1169 checks, 28 rows verified at step 7;
`VERIFY-v0.1.0.txt`, the v0.1.0 run under the same reader, 317 checks, "no receipts/ in this
run"). `PACKAGE-SHA256SUMS` covers every file here except itself and the two transcripts, taken
over this repository as laid out; each run directory carries its own `SHA256SUMS`.

**The receipts.** `runs/2026-09-18-79df522b/receipts/<trial>.json`: the run's receipt chain in the
public verifier's envelope (`key_id`, `sequence`, `receipt_hash`, `signature`, `signed_payload`,
`subject_id`) and the redacted subject event (`event_type`, `status`, `code`, `proof_hash`,
`occurred_at`, `sequence`, `chain_scope`, `id`; no payload, no prompt text, no detection
internals). All 125 receipts are under `evaluation_ed25519_v1`. `registry-used.json` names the key
id, its public key, and the repository, path, commit and sha256 of the published registry the run
was checked against; step 7 requires the registry you supply to say the same. The verifier and
registry are not in this repository: a registry that arrived with the evidence proves nothing.
A receipt proves that the status and refusal code in `trials.jsonl` are what this plane signed,
hash-chained, under a published key. It does not prove the plane was right. `proof_hash` is
opaque here: its preimage carries the policy snapshot and is not shipped.

**The epoch.** Every instant in a trace is a pinned epoch plus the row's offset. v0.1.0's traces
used `2026-01-01T00:00:00Z`; the plane stamps each receipt's `occurred_at` from that same pinned
clock, and `evaluation_ed25519_v1` is valid from `2026-09-05T00:07:58Z`, so a v0.1.0-epoch receipt
lies outside the key's window and the public verifier refuses it, correctly. v0.2.0's traces use
`2026-09-06T00:00:00Z`, the earliest midnight inside the window. Offsets, windows and verdicts are
unchanged: on every row the agreement, the Dogwood verdict, the plane's status and its refusal code
are identical to v0.1.0's. The registry's window was not moved, no second key was added, and no
receipt is stamped from the wall clock.

**What differs from v0.1.0, file by file.** `trials.jsonl`: the absolute instants, the trace-shape
digests that include them, `tree_sha`, and a `requisition_oracle` field (the Requisition Bench
oracle's verdict beside the frozen oracle's; the oracle itself is still unpublished). `traces/`:
the instants. `run.json`: the run, the qualification, a `receipts` block. New: `receipts/`,
`registry-used.json`. `pack/`: identical. The reader gained step 7; `README-verification.md`
gained the three-way split and the epoch note; `PACKS.md` names `runs/<run id>` rather than one run.

**Status.** Release `v0.2.0` (2026-09-18): this section is frozen at that tag. No DOI yet. The
Requisition Bench's adjudicator, spec and scoring are still not in this release.

## v0.1.0 (2026-09-17)

**What this is.** The Dogwood cross-plane campaign run `2026-09-17-49489219` of Requisition (the authority
control plane), its report, and the reader that re-derives the Dogwood side of every claim offline.
Assembled by `bin/campaign-package` from the private tree at `efdc23f13cd57bad9ec669b0adde78a78769ca3f` on 2026-09-17 and proved
before it left: the reader ran from inside this package in an empty environment (`VERIFY.txt`,
last line `VERIFY DOGWOOD SIDE: PASS`, 317 checks). `PACKAGE-SHA256SUMS` covers every file here
except itself and `VERIFY.txt`; the run directory carries its own `SHA256SUMS`.

**Layout.** `runs/2026-09-17-49489219/` (the run: `run.json`, `trials.jsonl`, `t2-provenance.json`,
`pack/`, `traces/`, `NOTICE`, `SHA256SUMS`), `findings.md` (the report), `verify_dogwood_side.py`
(the reader), `README-verification.md` (how to run it; which citations resolve here and which are
the private tree's), `pack-source/` (the pack's rules, the expressiveness census with the
validator's recorded output on each rejected encoding, the R1 exhibit, the fixture bundles as data).
The reader is run as `./verify_dogwood_side.py runs/2026-09-17-49489219 --dogwood /path/to/dogwood --pack-source pack-source`.

**What is not here.** The authority plane's code and the campaign harness that drove it (the
Requisition side of every row is the plane's recorded measurement: inspectable, not re-executable
from this package); the Requisition Bench's adjudicator, spec and scoring (unpublished; a later
release); the qualification and fresh-clone reproduction records of the private tree that the
report cites by path.

**Status.** Release `v0.1.0` (2026-09-17): this section is frozen at that tag; results cite the tag,
never a moving branch. What the tag contains is exactly the listing above; what it does not
contain is stated above. No DOI yet. The Requisition Bench's adjudicator, spec and scoring are not
in this release -- they join at the first release that includes a run they judged.

**Known at the tag, found 2026-09-18.** `sha256sum -c PACKAGE-SHA256SUMS` fails at `v0.1.0`: the
sums were taken over the package with its run directory at `2026-09-17-49489219/` and published
with it at `runs/2026-09-17-49489219/`, and `README-verification.md` was re-pointed at `runs/` after
the sums. The tag's files are unchanged and are what this section lists; the run directory's own
`SHA256SUMS` verifies; from v0.2.0 the sums are taken over the repository as laid out, and the
v0.1.0 run is covered by them.

**Dogwood.** [github.com/dogwood-policy/dogwood](https://github.com/dogwood-policy/dogwood) at `fa7a32370a642b32b54c73c16fd75bc88c847050`,
built from source (`cargo build --release -p dogwood-cli`). Two builds of that commit gave the same
28 verdicts (workspace `0fb979e9…`, fresh clone `42b4786a…`).
