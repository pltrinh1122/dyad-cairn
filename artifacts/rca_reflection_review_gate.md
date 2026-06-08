# Root Cause Analysis: The Audit DAG Design-Review Hallucination

## 1. Problem Statement
The Dyad encountered a structural paralysis when autonomous self-healing routines (Audit DAGs) were injected. Specifically, `node_audit_probe_reflection_review_gates` became artificially trapped at the `IN_REVIEW` Design-Review gate—a gate designed exclusively to prevent generative hallucination in the *Frontier DAG*.

## 2. Root Cause
The `skills/flow_state_manager.py` routing engine utilized a monolithic injection invariant (`inject_node`). It forcefully hardcoded the `"status": "IN_REVIEW"` state onto every node injected into the local YAML substrate, completely disregarding whether the substrate was `artifacts/frontier_state.yml` (Forward Generation) or `artifacts/audit_state.yml` (Backward Self-Healing). 

## 3. The Conceptual Drift
The Dyad's cognitive architecture maintains two asymmetric boundaries:
- **Frontier DAG (Intent Phase):** Highly entropic. The Dyad hallucinates futures (PLANS). Operator `lean!` is mechanically required to constrain the search space before action.
- **Audit DAG (Self-Healing Phase):** Highly deterministic. The Dyad reacts to physical invariants (failed tests, structural decay, SPAOR violations). Waiting for an Operator `lean!` here is an anti-pattern because the Agent must autonomously mend the substrate to restore homeostasis.

By imposing the Frontier DAG's Intent Gate on the Audit DAG, the architecture conflated *Generative Intent* with *Deterministic Remediation*.

## 4. Resolution & Structural Invariants
1. **Context-Aware Injection:** `inject_node` was fractured. It now sniffs the `DYAD_DAG_STORE` environment variable. If the Dyad is operating in the Audit context, it bypasses the `"IN_REVIEW"` assignment entirely, allowing topological evaluation (`READY` vs `BLOCKED`) to compute instantaneously.
2. **The Reflection Review Gate (`trail-dispose`):** To preserve the Asymmetric Guard invariant, while the Audit DAG may *act* autonomously, it cannot permanently etch its *learnings* into the cognitive ledger (`DYAD_LEDGER.md`) without Operator synthesis. We fractured the monolithic `trail_reflect` script into a two-phase commit:
   - `trail-reflect` (Drafting & PR generation -> HALT)
   - `trail-dispose` (Operator execution `lean!`/`dispose` -> Merge & DAG Pruning)

## 5. Prevention
The CI/CD pipeline now enforces `test_audit_dag_injection_bypasses_in_review` and `test_trail_dispose_csi_guard`. Future regressions attempting to monolithically enforce `IN_REVIEW` across both DAGs will physically shatter the test suite and trigger a remote GAP failure.
