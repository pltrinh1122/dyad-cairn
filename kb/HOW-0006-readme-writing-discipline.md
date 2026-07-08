# HOW-0006: The README-Writing Discipline

> Procedural *When* of the Ontological Bond: *Why* in `kb/WHY-0001-readme-writing-discipline.md`,
> deterministic *How* in `skills/readme_lint.py` (+ `tests/test_readme_lint.py`).
>
> **This discipline is stated as conditions, not instructions.** A discipline that
> produces *falsifiable* manifestos must itself be falsifiable: an imperative ("copy the
> schema") carries no truth-value you can attack, but a condition ("the schema matches
> the exemplar's field set") is a state of the world that is either true or false of a
> given README, and can be checked, grounded, and refuted. So the discipline is a list
> of **what must be true** of a conforming README and the process that produced it. A
> dyad satisfies the discipline by making every condition true — by whatever route fits
> its own substrate — not by replaying `dyad-cairn`'s keystrokes.
>
> **Grade: `survives — intra-dyad`, CANDIDATE for cross-dyad use.** No dyad other than
> `dyad-cairn` has run it. Per the no-dogma rule this document is true-for-now,
> re-rubbable. Component survival differs and is graded honestly:
> - **Form, style, spine, claims (C1–C4, C7, C10–C11): n=1** — established by the
>   2026-07-08 materialization arc (`DYAD_LEDGER.md` REFLECT `2026-07-08 21:07:16`).
> - **Content-form and content-tone (C5, C6): n=1** — the refinement arc's layman
>   re-projection and voice corrections (PR #154, commit `313a317`).
> - **Metaphor conditions (C8, C9): n=2** — materialization (same REFLECT, SH) **and**
>   the refinement arc's metaphor pass (PR #154, commit `313a317`).
> - **Falsifier-fidelity + grounding conditions (C12–C16): n=1** — the refinement arc
>   (audit `wf_8918028a-253`, PR #154).
> - **This document's own conditions: hardened n=1** by an adversarial run of the
>   discipline against itself (`wf_aa885aeb-4ec`).

## What a conforming README is

A root `README.md` in the **falsifiable-manifesto** form: a `derived-view` lens that
states one belief with conviction, decomposes it into numbered attackable claims, pairs
every claim with an explicit falsifier, and carries machine-readable honesty fields
(`status`/`grade`/`coverage`/`dogma`) that never overstate the evidence.

**Exemplar:** `dyad-cairn/README.md` (this repo — the reference output). The exemplar is
the model for the three *content* conditions (C5–C7): a consumer reads its structure,
audience-handling, tone, and stance off the exemplar rather than off a re-specification here.
**Form ancestor:** `dyad-bond/README.md` ("The Covalent Bond", `github.com/pltrinh1122/dyad-bond`,
`updated: 2026-06-25`). Its derived-view frontmatter keys are bond's own prior art (bond's
`dialectic/loaded-status-frontmatter.md` repo scan, 2026-07-04, records them among the only
pre-existing front-matter schemes there, alongside the `locus:` key and `dm/` headers). Per
`cairn:never-guess`, assert no deeper lineage than the artifacts show.

## How each condition is verified (the Builder-vs-Enforcer axis)

Each condition names its **verifier** — who or what can falsify it:
- **LINT** — mechanically decidable; `skills/readme_lint.py` checks it. The linter holds
  no opinion on register, tone, or meaning (Builder vs Enforcer): it may not judge taste.
- **AUDIT** — decidable only by reading the claim against its sources; checked by the
  **Grounding Audit** (below), an adversarial claim-by-claim pass.
- **OPERATOR** — a generative judgment (structure, audience, tone, style, metaphor,
  emphasis); only a human can settle it.

## Glossary

- **`craft_telos`** — a dyad's charter metric. `dyad-cairn`'s (`DYAD.md § Craft`):
  minimize the discovery + structuring turns to turn a messy challenge into a proven
  skill. Adopting dyads substitute their own.
- **smoothing** — silently rewording a claim so it stops presupposing a missing artifact
  ("smoothing the mortar", `DYAD.md § The Abstraction Boundary`); the banned move. The
  only legitimate reword is a consensus change in the canonical home, then re-projection.
- **No-Pure-G invariant** (`DYAD.md § NON-NEGOTIABLE`) — no pure Generative execution;
  every generated script/logic block ships paired with a deterministic test suite.

---

## The conditions — what must be true

A README conforms to this discipline **iff every condition below holds.** Each is
declarative; its *violation* names the observation that refutes conformance.

### Form (the frontmatter lens)

**C1 — The lens declares itself a lens.** `kind: derived-view`, `dogma: false`, and
`rule: "cite the source, never this lens"` are present with exactly those values.
*Violation:* any other `kind`; `dogma` true or absent; a README used as a content-home.
*Verifier:* LINT.

**C2 — The frontmatter carries the whole schema.** Present: `doc, kind, genre, rule,
belief{statement, foundation, stance, status}, grade, coverage, dogma, caution, cta,
canonical_home, governed_by, updated`. *Violation:* a missing field. *Verifier:* LINT.
The schema's explanatory comments travel with it as form — except any comment carrying a
metaphor, which is bound by C8.

**C3 — The status never overstates.** `belief.status` is `hypothesis` or `theory` —
never `conjecture`, never `settled`; `grade` never reads `settled`. *Violation:* a
settled/conjecture status, a "settled" grade. *Verifier:* LINT (status/dogma locks); the
`grade`/`coverage` *values* are AUDIT (C4), not LINT.

**C4 — Evidence fields are this dyad's own, re-derived.** The dyad-derived-value fields
(`belief.*, grade, coverage, caution, cta, canonical_home, updated`) state THIS dyad's
evidence, re-derived from its ledger. `grade` caps at `survives` (an unexercised README
says so, e.g. `"unexercised — no arc survived yet"`); `coverage` uses the E-scale (`E0` =
no outside attack; `En` per independent outside attack survived — raising confidence, not
status). *Violation:* an exemplar's evidence string copied onto an unearned base (e.g.
`survives — intra-dyad` on a README no arc has survived). *Verifier:* AUDIT.

### Content (what the prose is — modeled on the exemplar)

**C5 — content-form: structure and audience are the exemplar's.** The document follows
the exemplar's section skeleton — opening belief, then *what it is* (definition), *why it
matters* (stakes), *the ask*, the *numbered claims with falsifiers*, and a *closing
pointer to the canonical home* — and it sustains, throughout, the single reader/attacker
it declared (C11's target). *Violation:* a missing structural section; an order that
buries the belief; or a body that drifts to a different audience than the one declared
(insider vocabulary in a lay-targeted manifesto). *Verifier:* OPERATOR. *Origin (n=1):*
the refinement arc's layman re-projection reshaped the exemplar to this skeleton and
audience (PR #154).

**C6 — content-tone: plain, accessible language.** The prose is plain and accessible to
the declared audience: each term of art is glossed once, then plain words are used; no
unexplained jargon; no propaganda or slogan register standing in for argument; the actor
vocabulary is fixed and held (the taxonomy — the autonomous *agent*, the paired *AI*, the
raw *model* — named once, consistent throughout); and every failure mode it indicts is
described accurately, never exaggerated. *Violation:* unglossed jargon; militant/
propaganda vocabulary ("revolutionary", "regime"); register above the audience; drifting
actor terms (tool/agent/AI used interchangeably); an exaggerated indictment (calling
reasonable-but-unverified inference "invention" or "fabrication"). *Verifier:* OPERATOR.
*Origin (n=1):* the refinement arc — the layman-paraphrase pass, the no-propaganda
correction, the agent≠tool taxonomy, and inference≠invention accuracy (PR #154, commit
`313a317`).

**C7 — content-style: a manifesto.** The document states one belief with conviction and
immediately hands over the knife — it *declares* (does not hedge) and *invites attack*
(does not assert closure). *Violation:* wishy-washy hedging that states no attackable
belief (conviction absent); OR a settled/dogmatic register that declares without exposing
its falsifier (the `caution` field's "a manifesto that reads as settled is a closed
system"). *Verifier:* OPERATOR. *Origin (n=1):* the genre + `caution` fields and the
falsifiable-manifesto form inherited from dyad-bond; this arc's propaganda-strip kept the
conviction while refusing the dogma.

**C8 — Every metaphor is the dyad's own.** No metaphor — in body prose *or* in a
frontmatter comment — is carried untranslated from an exemplar. *Violation:* an
exemplar's figure appearing verbatim (bond's "hands you the knife", "pipeline",
"engine"). *Verifier:* OPERATOR. *Origin (n=1):* materialization arc recorded the
carry-anti-pattern verbatim (`DYAD_LEDGER.md` REFLECT `2026-07-08 21:07:16`, Stop).

**C9 — One metaphor domain, two at most.** The document rests on a single physical
domain (the second, if any, deliberate and named). *Violation:* a third domain, or a
stray from another (organic, combat, navigation, cooking). *Verifier:* OPERATOR.
*Origin (n=2):* materialization ("too many mixed metaphor: smoothing = rot is a large
gap … one at most two"; "you don't 'mine' mortar" — REFLECT `2026-07-08 21:07:16`, SH)
**and** the refinement arc's metaphor pass (PR #154, commit `313a317`).

### Claims (the attackable spine)

**C10 — Every claim hands over a knife.** The body contains numbered claims, and every
non-terminal claim is paired with an explicit falsifier (`Break it:`). A single terminal
"standing invitation" claim may carry the invitation instead of a falsifier. *Violation:*
a substantive claim with no falsifier. *Verifier:* LINT.

**C11 — The spine is fixed before the form.** Before any large prose draft exists, four
things are known and Operator-approved: the belief's **falsifier**, the **target**
(reader and attacker), the one **asymmetry** vs. the default, and the **metaphor
domain** — and from them, a spine of belief → numbered claims → one falsifier per claim
→ one evidence pointer per claim. *Violation:* a full draft produced before the spine is
approved (the "form before spine" failure that forces the Operator into line-editing).
*Verifier:* OPERATOR / process. *Origin (n=1):* Operator correction, materialization arc
("provide elicitation questions so that you're 90% aligned with the next draft rather
than this line-by-line editing" — REFLECT `2026-07-08 21:07:16`, SH). This condition is
the direct lever on `craft_telos`.

### Grounding

**C12 — Falsifier fidelity.** Each claim's refutation-extension matches its
canonical/baseline falsifier exactly: register may change, the extension may not.
*Violation:* a paraphrase that widens or narrows what counts as a refutation (e.g.
dropping "generative", dropping the Operator as the party asked, collapsing a three-axis
bond to two). *Verifier:* AUDIT. *Origin (n=1):* the refinement arc shipped four such
drifts through six careful register passes; only the audit caught them (`wf_8918028a-253`).

**C13 — Proof of origin resolves, at whichever layer.** In the formal register, each
claim carries a resolvable footnote pointer (`[^cN]: … Evidence: FILE § Heading` — see
`./bin/git show c252640:README.md`). A plain-register projection may drop the footnotes;
then proof of origin holds at the document level **iff `canonical_home` enumerates the
home of *every* claim** (not just the belief's) — which is exactly why the exemplar's
`canonical_home` lists all four homes its six claims cite. *Violation:* a claim whose
canonical home appears in no `canonical_home` entry. *Verifier:* LINT (each entry
resolves to a real file + heading) + AUDIT (the entries cover every claim).

**C14 — The substrate under a claim exists.** Every artifact a claim presupposes (a
wrapper, a guard, a playbook) is present on disk. *Violation:* a claim standing on an
absent artifact. *Verifier:* AUDIT.

**C15 — Honesty-field values are consensus-set and register-stable.** `status`/`grade`/
`coverage`/`dogma` carry the values approved with the spine, and no register edit weakens
them. From the second committed edit onward this is checkable as byte-identical-to-baseline
frontmatter; on first authorship it anchors to the approved spine. *Violation:* a register
edit that softened an honesty field. *Verifier:* AUDIT.

**C16 — Gaps are surfaced, never smoothed.** A substrate gap found while grounding is
recorded in the dyad's task tracker, never dissolved by rewording the claim. *Violation:*
a claim quietly reworded to stop presupposing a missing artifact. *Verifier:* AUDIT /
OPERATOR. *Origin:* the exemplar audit surfaced four gaps as todos (`cd799b7f`,
`1ad107ed`); a fifth (`0fa5ec7f`) surfaced at PR #154's d-land — none smoothed.

### Close and adoption

**C17 — The mechanical gate is green.** `python3 skills/readme_lint.py README.md` exits
0. *Violation:* nonzero exit. *Verifier:* LINT (self).

**C18 — It landed through the FSM, not around it.** The README reached `main` via
branch → CI green → PR → Operator merge, never a direct mutation. *Violation:* a
direct-to-main change. *Verifier:* the dyad's own guards.

**C19 — The tool was vendored whole.** An adopting dyad holds `skills/readme_lint.py`
**and** `tests/test_readme_lint.py` together (No-Pure-G), in the `skills/` + root-`README.md`
layout the test imports assume, with the source commit recorded; runtime dep PyYAML.
*Violation:* the linter vendored without its test suite. *Verifier:* the adopting dyad's gate.

---

## The Grounding Audit (the verifier for the AUDIT conditions)

C4, C12, C13, C14, C15, C16 are decided here. Register passes silently drift claim
semantics — proven, not hypothetical — so before a README lands, each claim is audited
against three anchor classes, and each finding is adversarially verified before it is
applied:

1. **The canonical home** — the `DYAD.md` sections named in `canonical_home`.
2. **The formal baseline** — the last committed formal version
   (`./bin/git show HEAD:README.md`). **First-authorship branch (no committed baseline
   yet):** the Operator-approved spine (C11) serves as the falsifier-extension baseline,
   since it fixed one falsifier per claim before any register pass. *(This branch: n=0 —
   no dyad has run it.)*
3. **The physical substrate** — the artifacts each claim presupposes (C14).

The audit is adversarial by construction: a finding survives only if an independent pass
fails to refute it. This is what makes C12–C16 conditions rather than hopes.

## The load-bearing conditions

If a dyad keeps only a few, keep the ones whose violation was lived, not imagined:
**C5/C6** (structure/audience and plain tone are the exemplar's — the layman arc),
**C7** (manifesto stance — conviction without dogma), **C8/C9** (metaphors are yours,
budget one–two), **C11** (spine before form), **C12** (falsifier fidelity), **C13**
(proof of origin resolves), **C15** (honesty fields never weaken), **C16** (gaps
surfaced, never smoothed). The rest are mechanically held by `readme_lint.py` (C1–C3,
C10, C13-lint, C17) or by the dyad's existing gates (C18–C19).
