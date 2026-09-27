# generators/ — none (a stated absence)

The contract asks for "the per-family generators and the seed of the registered draw". This pack has
no generators: its registered draw is the fixed catalogue v0.2.0 ran, one instance per family, frozen
at `22216be` before that run (`pack.json` → `draw`). The confirmation draw the specification describes
(§Scoring: a re-draw under a seed the plane's author did not choose) therefore cannot be made against
this pack, and a run against it is reported as *registered draw only*.

Generators that vary names, instants and structure per family, with the expected verdict derived from
`rule_predicate` where the paragraph is a predicate, are a standing obligation named in the
specification's §Third-party runnability. When they exist they land here with the seed, and the pack
re-registers under a new version.
