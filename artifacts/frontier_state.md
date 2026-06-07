# The Frontier State (DAG)

> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**
> Source of truth is `artifacts/frontier_state.yml`.
> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.


## 🟡 IN_REVIEW NODES
- **node_17b_execute_audit_dag** [PLAN]: Execute Audit DAG Implementation
  - *Goal:* Parameterize the SPAOR engine and inject check_audit_lock() per plan_node_17a.md

## 🔴 BLOCKED NODES
- **node_4c_probe_anchor_compilation** [PROBE]: Probe Anchor Compilation Invariant
  - *Goal:* Investigate how a fully saturated dip_state.yml is safely and deterministically projected into the immutable GEMINI.md anchor.
  - *Dependencies:* node_4a_execute_matrix_schema
- **node_18_probe_spaor_plan_violation** [PROBE]: Audit SPAOR PLAN Violation
  - *Goal:* (AUDIT DEBT) Investigate and remediate the systemic SPAOR violation where the Agent pre-emptively hallucinates [PLAN] nodes for unexecuted [PROBE] nodes. Implement the necessary CSI Guard or architectural constraints to trap this hallucination.
  - *Dependencies:* node_17b_execute_audit_dag

## 🔴 READY NODES
- **node_4b_execute_sonar_halting** [EXECUTE]: Execute Provenance Extraction Invariant
  - *Goal:* Implement the markdown parser in dip_sonar.py to dynamically extract the required dimensions, passing the TDD tests.
