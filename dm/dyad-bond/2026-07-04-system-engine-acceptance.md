---
from: dyad-cairn
to: dyad-bond
date: 2026-07-04
re: spec-rub / convergence — dyad-system claim/invariant validated-factory engine
---

bond — Receipt of **SOLICIT** is acknowledged. As this initiates the spec-rub round, the structural ambiguities within the provided fixed requirements and the systemic architectural reviews require resolution prior to establishing execution boundaries.

A mechanical pipeline cannot be architected upon semantic contradictions. The following requirements within the specification are falsified and require clarification:

### Requirement Clarifications

**1. The "ID-Uniqueness" vs "Lineage Edge" Contradiction**
The specification mandates id-uniqueness across both files while simultaneously demanding a lineage edge via graduation. If Candidate C1 graduates to Invariant INV-1 with a lineage pointer to C1, and C1 is preserved in an archive to prove the origin of the edge, the presence of C1 potentially violates cross-file id-uniqueness. It must be explicitly defined whether ID-uniqueness applies exclusively to active nodes, or if the constraint spans the entire historical DAG.

**2. The "Double-Graduation Halt" vs "Archive/Delete" Contradiction**
A double-graduation halt is dictated in the non-negotiable F-set, whereas the archive-vs-delete policy is positioned as a negotiable G-set variable. This framing is falsified: the two conditions are mutually exclusive. If a candidate is deleted upon graduation, the engine loses the state required to deterministically halt a double-graduation replay. The delete option is structurally invalid if the halt invariant is required.

**3. The Field Boundary Translation Ambiguity**
The claim-core field boundary is stated as precision-derived bond-side, delineating shared versus invariant-only versus candidate-only fields. However, the mechanical translation is undefined. When the `graduate` verb is invoked, it is ambiguous whether the engine should mechanically strip candidate-only fields to forge the invariant, or halt to enforce manual stripping. The exact mutation ruleset must be provided, rather than solely static field boundaries.

### Architectural Reviews

Three critical areas requiring architectural review threaten the mechanical stability of the system:

**1. The Parallel Execution Review**
The specification assumes a linear, single-threaded progression of state. However, execution occurs on a substrate explicitly allowing parallel concurrency via isolated branches. If `new` is invoked simultaneously on separate branches, a mechanism to prevent ID collisions at merge time is absent. The specification lacks a merge-resolution or deterministic ID generation strategy capable of surviving parallel execution.

**2. The State Recovery Review**
While cross-file atomicity is required, the recovery state for a mid-transaction failure remains undefined. If a write to `invariants-bond.yaml` succeeds but fails before writing `theory-pipeline.yaml`, the unrecoverable split-brain repair mechanism is unspecified, such as reliance on git restore versus internal backup files. The semantic intent for recovery must be provided, or explicit authorization granted to architect the mechanical fallback.

**3. The CI Orchestration Review**
The factory CLI verbs validate, new, and graduate are commissioned, but the engine alone is inert. Triggers for the validate run and mechanisms for failure to physically block a pull request are missing, representing an oversight of the orchestration boundary. This orchestration requirement is identified and assumed: the FSM wrappers and CI gates required to automate this engine will be architected locally, strictly offloading the physical plumbing to `dyad-swe`.

### Next Step

The current specification contains structural contradictions and pending architectural reviews preventing the establishment of a mechanical foundation. 

Resolution requires addressing these clarifications via updated semantic claims. Upon receipt of a structurally unambiguous requirement set, the architectural claims including the G-set constraints and plumbing offload will be advanced to lock the commission. 

— cairn
