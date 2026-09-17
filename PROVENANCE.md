# Provenance

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

**Status.** Release `v0.1.0` (2026-09-17): this file is frozen at that tag; results cite the tag,
never a moving branch. What the tag contains is exactly the listing above; what it does not
contain is stated above. No DOI yet. The Requisition Bench's adjudicator, spec and scoring are not
in this release -- they join at the first release that includes a run they judged.

**Dogwood.** [github.com/dogwood-policy/dogwood](https://github.com/dogwood-policy/dogwood) at `fa7a32370a642b32b54c73c16fd75bc88c847050`,
built from source (`cargo build --release -p dogwood-cli`). Two builds of that commit gave the same
28 verdicts (workspace `0fb979e9…`, fresh clone `42b4786a…`).
