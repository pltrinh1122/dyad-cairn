# HOW-0006: The README-Writing Discipline

> Procedural *When* of the Ontological Bond: *Why* in `kb/WHY-0001-readme-writing-discipline.md`,
> deterministic *How* in `skills/readme_lint.py` (+ `tests/test_readme_lint.py`).
>
> **Grade: `survives — intra-dyad`, CANDIDATE for cross-dyad use.** No dyad other than
> `dyad-cairn` has run this playbook yet. Per the no-dogma rule this document is
> true-for-now, re-rubbable. Component survival differs and is graded honestly, not
> uniformly:
> - **Phase 1 (inherit form) and Phase 2 (spine before form): n=1** — the 2026-07-08
>   materialization arc (`DYAD_LEDGER.md` REFLECT `2026-07-08 21:07:16`).
> - **The metaphor invariant (Phase 3, pass 6): n=2** — the materialization arc
>   (`DYAD_LEDGER.md` REFLECT `2026-07-08 21:07:16`, SH) **and** the refinement arc's
>   metaphor-coherence pass (PR #154, commit `313a317`).
> - **Phase 4 (Grounding Audit): n=1** — the refinement arc (audit `wf_8918028a-253`, PR #154).
> - **The spine→draft bridge and the first-authorship branch: n=0** — stated
>   prescriptively; both lived arcs ran them implicitly. Re-rub if they do not survive.

## What this produces

A root `README.md` in the **falsifiable-manifesto** form: a `derived-view` lens that
states one belief with conviction, decomposes it into numbered attackable claims, pairs
every claim with an explicit falsifier, and carries machine-readable honesty fields
(`status` / `grade` / `coverage` / `dogma`) that never overstate the evidence.

**Exemplar:** `dyad-cairn/README.md` (this repo — the reference output of this playbook).
**Form ancestor:** `dyad-bond/README.md` ("The Covalent Bond", `github.com/pltrinh1122/dyad-bond`,
`updated: 2026-06-25`). Its derived-view frontmatter keys are bond's own prior art —
bond's `dialectic/loaded-status-frontmatter.md` repo scan (2026-07-04) records them as
one of the only pre-existing front-matter schemes in that repo (alongside the `locus:`
provenance key and `dm/` message headers), independent of that file's still-CANDIDATE
`loaded:` proposal. Inherit the *form* from the exemplars; never inherit a claim, a
metaphor, or a word of body content (per `cairn:never-guess`, assert no deeper lineage
than the artifacts show).

## Glossary (terms this playbook uses normatively)

- **`craft_telos`** — a dyad's charter metric. `dyad-cairn`'s (`DYAD.md § Craft`):
  *minimize the discovery + structuring turns it takes to turn a messy challenge into a
  proven skill.* Adopting dyads substitute their own telos.
- **surface a gap as a todo, never smooth it** — record a discovered substrate gap in
  your dyad's task tracker rather than silently rewording a claim so it stops
  presupposing the missing artifact. "Smoothing the mortar" (`DYAD.md § The Abstraction
  Boundary`) is the banned move; the only legitimate reword is a consensus change in the
  canonical home, followed by re-projection.
- **No-Pure-G invariant** (`DYAD.md § NON-NEGOTIABLE`) — no pure Generative execution;
  every generated script or logic block is immediately paired with a deterministic
  automated test suite.

## Preconditions

- The claims already live in a canonical home (`DYAD.md` or your dyad's equivalent).
  The README is `kind: derived-view` — a projection, **never** a content-home. If a
  claim has no canonical home yet, stop: author it there first, by consensus.
- An Operator is available. **Phase 2 is Operator-answered, Phase 3 is Operator-steered,
  and Phase 5 lands only on an Operator merge** — a pure-Agent run of this playbook is a
  category error (and, per the exemplar's own Claim 3, a falsifier candidate).

## Phase 1 — Inherit the form, not the content

Copy the frontmatter **schema** from the exemplar. Its explanatory inline comments
travel with the schema as form — **except** any comment carrying a metaphor, which is
subject to the same translate-never-carry rule as body prose (see Phase 3, pass 6; e.g.
bond's `genre` comment "hands you the knife" is a knife metaphor and must be re-voiced
into your dyad's ontology, as cairn's exemplar does).

The schema's fields split into two kinds, and the split decides copy-vs-re-derive:

**(a) Fixed-value fields — copy verbatim** (constants of the form):
- `kind: derived-view` — always.
- `dogma: false` — always; no-dogma is permanent.
- `rule: "cite the source, never this lens"`.

**(b) Dyad-derived-value fields — re-derive from YOUR OWN ledger**, never copy the
exemplar's string (they are evidence claims, and copying one overstates your evidence
even when the correct value happens to match):
- `belief{statement, foundation, stance, status}` — `foundation` is the epistemic
  ground (`belief` = chosen and held, not a brute axiom); `stance` is `thesis`
  (advanced to be falsified); `status` is `hypothesis` (survival corroborates → Theory)
  or `theory`, **never** `conjecture` (imports a proof not coming) and **never**
  `settled`.
- `grade` — caps at `survives`, **never** `settled`. A first, unexercised README says
  so honestly (e.g. `"unexercised — no arc survived yet"`); `"survives — intra-dyad"`
  is earned only after an arc survives inside your dyad.
- `coverage` — the **E-scale**: `E0` = no outside attack yet; `En` increments per
  independent outside attack survived. Outside engagement raises *confidence* (E0→E1),
  not *status*.
- `caution`, `cta`, `canonical_home`, `updated`.

`canonical_home` is the **machine-checked anchor set**: it must enumerate *every*
section where the belief and its claims canonically live — i.e. the exact set Phase 4
audits and `readme_lint.py` resolves (see the Proof-of-origin invariant). The body's
closing note may cite a *superset* of governing sections as human-facing prose (a
pattern inherited from bond's "Where it actually lives"); every `FILE § Heading`
citation must still resolve.

*Origin (n=1):* the materialization arc recorded the anti-pattern verbatim —
*"Accidentally carrying over upstream mixed metaphors ('pipeline', 'engine', 'at your
tier') from exemplars like `dyad-bond` without translating them into the current dyad's
strict ontological domain"* (`DYAD_LEDGER.md`, REFLECT `2026-07-08 21:07:16`, Stop).

## Phase 2 — Spine before form (the Elicitation Gate)

**Before generating any large draft**, put the four Elicitation Questions to the
Operator and get answers:

1. **Falsifier** — what concrete artifact or event would refute the belief?
2. **Target** — who is the reader, and who is the attacker?
3. **Asymmetry** — what is the one difference between us and the default that
   everything hangs on?
4. **Metaphor** — which single physical domain carries the document? (Two domains
   maximum, and the second must be deliberate and named.)

Only then draft the **spine**: belief (one line) → numbered claims → one falsifier per
claim → **one resolvable evidence pointer per claim** into the canonical home. In the
formal register this pointer is a per-claim footnote in the form established by the
baseline (`[^cN]: … **Falsifier:** … **Evidence:** FILE § Heading` — see
`./bin/git show c252640:README.md`). A later plain-register projection (Phase 3, pass 2)
may drop the per-claim footnotes; when it does, proof of origin is satisfied at the
**document level** by the `canonical_home` union of all claim homes plus the closing
note — which is exactly why `canonical_home` must list *every* claim's home, not just
the belief's.

**Phase 2 exit** is Operator sign-off on the spine itself — the elicitation answers are
inputs; the approved spine is the deliverable. Only after sign-off, expand the approved
spine into the full prose draft, inheriting the exemplar's section skeleton as form per
Phase 1 (definition section → stakes section → ask section → claims-and-falsifiers
section → closing pointer to the canonical home). Phase 3 then refines that draft.
*(The spine→draft transition is stated prescriptively, n=0 as an explicit gate: both
lived arcs ran it implicitly; re-rub if it does not survive.)*

*Origin:* Operator correction, materialization arc — *"what is the best approach to
achieve convergence with my expectation quicker? provide elicitation questions so that
you're 90% aligned with the next draft rather than this line-by-line editing"*
(`DYAD_LEDGER.md`, REFLECT `2026-07-08 21:07:16`, SH). This phase is the direct lever on
`craft_telos`: it converts line-editing turns into one elicitation turn.

## Phase 3 — Register passes (one steering vector per turn)

Refine the draft in Operator-steered passes. Each pass applies **exactly one** steering
vector; do not batch them. These are the passes the refinement arc ran, in order
(commit `313a317`, PR #154) — prescriptive as an ordered menu, not a fixed liturgy;
apply those a given README needs:

1. **No propaganda vocabulary.** Conviction comes from structure and the standing
   falsifier invitation, never from militant or slogan-shaped branding. A manifesto
   that reads settled is a closed system.
2. **Audience register.** For a public README: layman language. Gloss each term of
   art exactly once, then use plain words. The formal version loses nothing — it lives
   in the canonical home, which the closing note must point to.
3. **Load-bearing emphasis.** Name the case where the belief matters most (for
   `dyad-cairn`: long autonomous agent work, not chat convenience).
4. **Terminology taxonomy.** Fix the actor vocabulary and hold it (exemplar's:
   *agent* = the autonomous actor; *an AI* = the pair's junior half; *the model* =
   raw capability). Sweep for strays after every later edit.
5. **Accuracy over rhetoric.** Never exaggerate the failure mode you indict —
   overstated indictments cost the manifesto its credibility (arc decision "inference ≠
   invention", PR #154, commit `313a317`). Exemplar case: inference is
   reasonable-but-unverified, not "invention."
6. **Metaphor coherence sweep.** One metaphor domain, two maximum; purge organic,
   combat, navigation, cooking strays. *(Invariant, n=2 — this correction was issued
   independently in both arcs: materialization, `DYAD_LEDGER.md` REFLECT
   `2026-07-08 21:07:16` SH, Operator: "too many mixed metaphor: smoothing = rot is a
   large gap. tighten up the metaphor to one at most two" and "you don't 'mine' mortar";
   and the refinement arc's own metaphor pass, PR #154, commit `313a317`. Expect it;
   sweep before the Operator has to.)*

## Phase 4 — The Grounding Audit (the gate)

Register passes silently drift claim semantics — **proven, not hypothetical** (four
falsifier drifts shipped through six careful passes in the refinement arc, caught only
here; audit `wf_8918028a-253`). Before landing, audit **claim-by-claim** against three
anchor classes:

1. **The canonical home** (`DYAD.md` sections named in `canonical_home`);
2. **The formal baseline** (the last committed formal version, e.g.
   `./bin/git show HEAD:README.md` — falsifier wording with per-claim footnotes);
3. **The physical substrate** (every artifact a claim presupposes must exist on disk:
   wrappers, guards, playbooks).

**First-authorship branch (no committed formal baseline exists yet):** anchor 2 becomes
the **Operator-approved Phase-2 spine**, which fixed one falsifier per claim before any
register pass — so it is the falsifier-extension baseline. The honesty-field check is
re-anchored, not suspended: verify `status`/`grade`/`coverage`/`dogma` match the values
consensus-approved with the spine. The byte-identical-to-committed-baseline form of the
check applies from the second committed edit onward. *(First-authorship branch: n=0 —
no dyad has run it.)*

Adversarially verify every finding before applying it. The blocking class is
**falsifier-extension drift**: a paraphrase may change register freely but may not
widen or narrow what counts as a refutation — the manifesto's no-reword pledge makes the
falsifier's exact extension the commitment. Also blocking: any mutation of the honesty
fields (`status`/`grade`/`coverage`/`dogma`) by a register edit.

**Substrate gaps found during the audit are surfaced as todos, never smoothed.** The
exemplar audit surfaced four (ledger todos `cd799b7f`, `1ad107ed`); a fifth
(`0fa5ec7f`) was found during the d-land of PR #154 — same never-smoothed rule.

## Phase 5 — Mechanical close

**Adopting dyads — vendor the *How* first.** Copy `skills/readme_lint.py` **together
with** `tests/test_readme_lint.py` from `dyad-cairn` — they travel as a pair per the
No-Pure-G invariant — preserving the `skills/` + root-`README.md` layout (the test
imports `skills.readme_lint` and lints the README at repo root). Record the source
commit you vendored from. Runtime dependency: PyYAML. No extra CI wiring is needed
beyond your dyad's existing test gate; the vendored suite's `test_exemplar_readme_passes`
retargets to your own README once it is the repo's `README.md`.

1. Run `python3 skills/readme_lint.py README.md` — must exit 0. The linter enforces
   only the mechanical invariants (frontmatter schema, honesty-field presence + locks,
   `canonical_home` resolution, claim/falsifier pairing); it deliberately holds no
   opinion on register or metaphor, and does **not** validate `grade`/`coverage` values
   or per-claim inline pointers — those are audited in Phase 4 against the baseline
   (Builder vs Enforcer). Know the gate's boundary.
2. Land through your dyad's FSM discipline: branch → CI green → PR → Operator merges.

## Invariants (the discipline's non-negotiables)

- **Derived-view lock:** the README is never a content-home; cite the source, never
  the lens.
- **Honesty-field lock:** `status`/`grade`/`coverage`/`dogma` never weaken through a
  register edit; `dogma: false` is permanent; `grade` never reaches `settled` — status
  is the headline, not the footnote. (`readme_lint.py` enforces presence and the
  `dogma`/`status` locks; `grade`/`coverage` *values* are caught in Phase 4, not linted.)
- **Falsifier fidelity:** register changes freely; refutation-extension never.
- **Proof of origin (two layers):** the formal baseline carries one resolvable
  footnote pointer per claim; a plain-register projection carries proof of origin at the
  document level, and is legitimate only if `canonical_home` enumerates the home of
  *every* claim (so `readme_lint.py`'s `canonical_home` resolution covers them all).
- **Metaphor budget:** one domain, two max; exemplar metaphors — in body *and* in
  frontmatter comments — are translated, never carried.
- **Spine before form:** the four Elicitation Questions precede any large draft.
