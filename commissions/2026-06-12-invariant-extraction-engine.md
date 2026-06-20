# COMMISSION SPEC — invariant-extraction engine *(bond-hosted, builder-agnostic; v0.4 DRAFT)*

> **Status: DRAFT — not yet solicited.** Commissioner: dyad-bond. Builder: **PRESUMPTIVE dyad-cairn**
> (Operator `pin:` 2026-06-12, "most likely" — final assignment still the Operator's seat). Fit grounded
> by substrate-read: extraction/synthesis IS cairn's Generate mechanism (The Mason); their NON-NEGOTIABLE
> mandates TDD-by-deterministic-suite (our F-falsifiers = their native build shape); their
> `anchor_compiler.py` (dip_state.yml → projected GEMINI.md) is the isomorphic prior art; "never smooth
> the mortar" ≈ F-4 + fail-closed; Gemini = cross-vendor spec-contest. **Watch (why G-1/G-3 are
> load-bearing for this builder):** cairn trends heavy-machinery (lock-files, compilers, deps at age one
> week) — natural failure mode = a cathedral that passes every test; G-1 note for solicitation: their
> repo runs pytest/pyyaml, the DELIVERED engine stays stdlib. Home: this file, in bond's repo (bilateral
> contract → sender-hosted, per the s14 commission-architecture raff; Commons only if the *engine* later
> earns the share-gate).
> **Pin discipline:** on solicitation, the DM cites this file at an exact sha; the builder builds
> against those bytes; any spec change re-pins + notifies (no silent moving target — mode-4 guard).

## Why (the requirement, falsified into existence)

The Operator needs a **single-pane view of all standing invariants** across a dyad's artifacts to
evaluate the Agent's evaluations. An agent-pass extraction (bond v1, 2026-06-12) fails the real
requirement — **consistency**: same data set → same view. Agent extraction makes three
non-deterministic judgment calls per entry (selection · compression · grouping); two runs differ.
A measurement instrument that reads differently on identical input is not an instrument, and it
contaminates downstream conflict-detection (the super-invariant/rescoping experiment).

**The design principle (settled in the s14 rub):** full mechanical semantic extraction is impossible —
somewhere a judgment says "this sentence is an invariant." The engine does not eliminate the
non-determinism; it **places and bounds it**: semantic acts happen ONCE, at source, Operator-gated;
everything downstream is deterministic.

## Architecture (G bound to deterministic V)

1. **Tagging convention (the one-time semantic act — NOT the builder's; bond/Operator perform it).**
   Each invariant carries a durable inline anchor at its single home, wrapping the full text and
   holding a *stored canonical one-liner* (authored at ratification, never regenerated). Builder
   CONSUMES the convention; bond supplies its grammar as part of this spec's acceptance round.
   Suggested form (negotiable in spec-rub): `<!-- INV <dyad>:<ID> group=<G> status=<S> | <one-liner> -->`
   … `<!-- /INV -->`.
2. **Extractor (deterministic script).** Scans a configured source-list; collects tagged blocks;
   emits the view (header: source-sha pins + generation date; body: grouped one-liners + source
   refs). **Same input → byte-identical output.** Idempotent. No network. No LLM calls.
3. **FSM.** Explicit pipeline states — PIN-SOURCES → SCAN → COLLECT → VALIDATE → EMIT — fail-closed:
   malformed tag, duplicate ID, missing source, unclosed block ⇒ halt with named state + offending
   location; never a silently-partial view.
4. **CSI-guards (arm/disarm, deterministic):**
   - `view-staleness` — armed when an emitted view's pinned shas ≠ current source shas.
   - `id-integrity` — duplicate / orphaned / malformed IDs.
   - `untagged-candidate` — heuristic scan (NEVER/MUST/only-by/⚠-class lines outside tags) emits a
     *candidate queue* file; it never blocks emission (candidates are G's inbox, not V's veto).
5. **Out of scope for the builder (stays bond's):** authoring tags/one-liners; deciding what is an
   invariant; the candidate-queue triage; conflict-detection over the extracted set.

### Tag-grammar — RATIFIED (b): lean tag inline + structure sidecar *(2026-06-17, Operator Y; resolves the v0.2 open fork)*

The previously-open fork (full-tuple-inline vs sidecar) is disposed **(b)**: the md inline tag carries
**only** the `one_liner` (content single-homes at the prose source → lean boot surface, the H3 lesson);
the graph **skeleton** (`grounded_in` edges · `root_kind` · scope/prescription/observability tuples — the
structure a script cannot infer) single-homes in a **structure sidecar** (`invariants-bond.structure.yaml`).
The engine's emit is therefore a **merge keyed by id**:

    yaml = extract(md tags) ⊕ sidecar          # joined on `bond:<ID>`

This splits authoring across two homes *by design* — so the merge MUST be **id-integrity-gated** (F-8),
fail-closed and atomic, or (b) re-grows two-home drift at the id-reference layer (the binding rider:
choosing (b) = choosing (b) + this gate, one decision). The gate is **merge-layer only** — DAG-validity /
root-reachability stays the separate `anchor_dag_diff` + orphan-lineage instrument (do not conflate — D7
valid-vs-reachable). *Rationale single-homes in `dialectic/dyad-md-yaml-regen.md` §Leaned/Ratified (b).*

## Input invariants — what the FSM may assume *(added v0.2, Operator raff: a contract needs preconditions, not just postconditions)*

**Class A — FSM-VALIDATED preconditions** (violations HALT; each gets a seeded-corpus case, extending F-2):
- **A-1 committed-state:** extraction runs only on a clean tree at a real commit — a dirty-tree run makes
  the sha-pin lie about the bytes actually read. Dirty tree ⇒ halt.
- **A-2 encoding/EOL:** UTF-8 + LF, enforced — CRLF/encoding drift silently breaks byte-identity.
- **A-3 grammar-version:** the tag grammar is versioned; corpus tags must match the engine's declared
  version — mismatch halts (never best-effort parse).
- **A-4 source integrity:** source-list files exist + readable; **TOCTOU guard** — sha checked before AND
  after scan; mid-scan mutation halts.

**Class B — ASSUMED semantic preconditions (the engine's TRUST BOUNDARY — mechanically unverifiable
from inside; each maintained by a named upstream discipline, and DECLARED in every emitted view):**
- **B-1 tagging-completeness** (tagged = the whole invariant class) — maintained by: ratification-time
  tag-proposal discipline. *Failure mode = layer-locality: the engine grounds view⊨tags, never
  tags⊨invariant-class.*
- **B-2 one-liner fidelity** (the stored one-liner faithfully compresses its full text) — maintained by:
  the Operator's tag-rub at ratification. *Failure mode = meld-capture: commissioner authors the tags AND
  consumes the view.*
- **B-3 single-home integrity** (no untagged paraphrase drifting elsewhere) — maintained by: single-home
  discipline. *Failure mode = signal-blindness (the candidate-queue regex watches a vocabulary).*
- **B-4 status truthfulness** (`status=ratified` reflects a real ratification) — maintained by: tags
  written only in ratifying commits. *(Staleness = mode-4, already guarded mechanically.)*

> The Class-B set maps 1:1 onto bond's four coverage-failure modes (F1-final) — these are the residual
> risks NO mechanization removes; the view must wear them on its face. Note the recursion: B-1…B-4 are
> themselves standing invariants of the commissioning dyad → they get tagged at their homes and
> extracted into the view they condition.

## Acceptance falsifiers (the commission's `done_when` — all mechanical)

- **F-1 (determinism):** two consecutive runs over identical source shas differ by ≥1 byte ⇒ REFUTED.
- **F-2 (fail-closed):** a corpus seeded with each malformation class (dup ID, unclosed tag, missing
  source) produces a partial view instead of a named-state halt ⇒ REFUTED.
- **F-3 (staleness guard):** mutate a source after emission; the staleness guard fails to arm ⇒ REFUTED.
- **F-4 (no semantic drift):** any emitted one-liner differs from its stored source one-liner ⇒ REFUTED
  (the engine must never re-compress).
- **F-5 (portability):** pointing the config at a second dyad's tagged substrate requires code changes
  (not config) ⇒ REFUTED — the engine must be dyad-agnostic by configuration.
- **F-6 (declared trust boundary):** an emitted view that does NOT carry its Class-B assumptions in its
  header ⇒ REFUTED — a view presenting as unconditionally authoritative is counterfeit-green by
  construction.
- **F-7 (precondition halts):** each Class-A violation (dirty tree · encoding/EOL drift · grammar-version
  mismatch · mid-scan mutation), seeded in the corpus, must produce a named-state halt ⇒ else REFUTED.
- **F-8 (merge id-integrity — (b)-specific, the binding rider):** the md-tag id-set and the sidecar id-set
  must be in **exact bijection** and **every edge must resolve**; a seeded corpus must HALT (named state,
  **no partial yaml written**) on each of — **(i) orphan tag** (md id with no sidecar entry) · **(ii) orphan
  sidecar** (sidecar id with no emitting md tag) · **(iii) dangling edge** (`grounded_in` references an id
  absent from the merged set) · **(iv) cross-home dup** (same id in >1 md tag, or >1× in the sidecar). Any
  non-halt, or any partial emit, ⇒ REFUTED. *(Sharpens the §Architecture `id-integrity` CSI-guard from the
  intra-tag-set case to the two-home (b) merge.)*

## Architectural-grain clause *(added v0.3 — the Operator's fit-rub: contracts underdetermine fit)*

Behavioral invariants (A/B/F) do NOT fix the deliverable's **form**, and a contract-perfect artifact can
still be architecture-alien. The deliverable must additionally match the commissioning substrate's grain:
- **G-1 dependency budget:** stdlib-only (python3 or bash) — no package installs, no network at runtime.
- **G-2 runtime shape:** a run-to-completion script — no daemon, no persistent state beyond the emitted
  view + candidate-queue files.
- **G-3 size envelope:** the engine must be smaller than the problem — indicative ceiling ~300 lines; a
  10× overshoot is a misfit even if F-1..F-7 pass.
- **G-4 maintenance shape:** single-file preferred; readable by a non-builder dyad (the commissioner must
  be able to AUDIT, though never required to EXTEND).
*(Grain-clause violations are fit-refutations, negotiable in spec-rub — unlike F-falsifiers, which are not.)*

## Deliverable + lifecycle

Script + FSM + guards + config schema + the seeded malformation corpus, delivered in the **builder's**
repo; delivery DM carries the pointer + the builder's own falsifier-run record. Bond re-runs F-1…F-5
independently (acceptance = the commissioner's rub, not the builder's attestation). Engine graduates
to Commons `library/` via the Founding gate only after ≥2 dyads live it (live→write→share).

## What this commission is NOT

Not a view-content authority (sources stay canonical; the view is derived, never Sense-loaded by the
Agent) · not a Commons lane proposal (if commissioning recurs, the lane is steward's to ratify,
informed by this instance) · not a tagging service (semantic acts stay with the commissioning dyad).
