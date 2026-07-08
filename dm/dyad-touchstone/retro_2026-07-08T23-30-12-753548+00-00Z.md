# Reflect: Cairn Manifesto Refresh → README-Writing Discipline (2026-07-08)

Arc: refined the root `README.md` (falsifiable-manifesto lens), then extracted the
process that produced it into a reusable Ontological Bond — WHY-0001 / HOW-0006 /
`readme_lint.py` — with `README.md` as the exemplar. Landed across PRs #154, #155, #157,
#156, #158.

## Continue
- **Adversarial verification before committing findings.** Both audit workflows earned
  their cost: `wf_8918028a-253` caught 4 falsifier-drifts invisible to the writer;
  `wf_aa885aeb-4ec` caught the discipline violating its own invariants (inflated n,
  ungrounded quotes, false lineage). Verify-before-commit is the engine of quality here.
- **Grounding every claim and citation to a real artifact** (proof of origin) as a gate,
  not a courtesy — and surfacing substrate gaps as todos rather than smoothing them
  (6 gaps surfaced, none papered over).

## Start
- **Committing durable intent the instant it is captured**, or capturing it as a
  standalone todo YAML — never leaving it as a bare ledger append in a working tree known
  to be polluted by gap-5. The lost craft-capability pin is the proof.

## Stop
- **Blanket `git checkout <ledger>` to strip gap-5 test noise.** It is a blunt
  instrument that discarded a legitimate append (the pin). Until gap-5 is fixed, strip
  only the collision lines surgically, or commit real appends first.

## SH — Should Have (debt)
- I lost the Operator's craft-capability seed by leaving `./bin/pin`'s ledger append
  uncommitted, then wiping it during a noise-strip. The arc's whole theme is *do not lose
  intent*, and I lost the one insight the Operator most wanted preserved. Recovered via
  todo `144429c6` (PR #158), but it should never have been at risk. This elevates gap-5
  (`0fa5ec7f`): ledger pollution does not merely add noise — it corrupts the safety of
  persisting real ledger entries.

## SH — Should Hold (credit; incl. Operator prompting)
- Every quality gain traced to a precise Operator correction, each functioning as a
  *falsifier applied to a draft*: propaganda→tone; long-conversation→long autonomous
  work; tool→agent taxonomy; inference≠invention; rot→one-metaphor; imperatives→
  falsifiable conditions; the missing content invariants (C5–C7). The Operator embodied
  the Diviner — pointing the lens at exactly the load-bearing friction. The drafts were
  mortar; the corrections were the cuts that made them falsifiable stone. Fittingly, the
  Operator's closing insight *named that very mechanism*.

## Live front (carries forward)
- **Craft-capability seed** (todo `144429c6`): *converting mortar to stone = converting
  unfalsifiable statements into falsifiable ones.* Next: `d-rub` to scope WHAT/WHY/SCOPE
  toward a `DYAD.md § Craft` deepening (mechanism = falsification-engineering); candidate
  generalized *How* = a mortar-detector lint.
- **Substrate gaps** (todos `cd799b7f`, `1ad107ed`, `0fa5ec7f`, `cc2215e0`): missing
  `dip_state.yml`; stale `DYAD.md:89/:42` GEMINI refs; leaked test fixtures; gap-5
  (elevated); missing `kb/HOW-0005`. Gap-3 (vacant `WHY-*` axis) partially resolved —
  `WHY-0001` now exists.
