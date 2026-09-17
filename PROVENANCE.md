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

**Status.** Private, for the owner's review. Not yet a release: no tag, no DOI. When released, the
release is a tag with this file frozen at it; results cite the tag, never a moving branch.

**Dogwood.** github.com/dogwood-policy/dogwood at `fa7a32370a642b32b54c73c16fd75bc88c847050`,
built from source (`cargo build --release -p dogwood-cli`). Two builds of that commit gave the same
28 verdicts (workspace `0fb979e9…`, fresh clone `42b4786a…`).
