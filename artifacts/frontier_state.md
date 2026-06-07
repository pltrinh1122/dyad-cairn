# The Frontier State (DAG)

> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**
> Source of truth is `artifacts/frontier_state.yml`.
> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.


## 🟢 ACTIVE NODES
- **node_4b_execute_sonar_halting** [EXECUTE]: Execute Provenance Extraction Invariant
  - *Goal:* Implement the markdown parser in dip_sonar.py to dynamically extract the required dimensions, passing the TDD tests.

## 🔴 BLOCKED NODES
- **node_4c_probe_anchor_compilation** [PROBE]: Probe Anchor Compilation Invariant
  - *Goal:* Investigate how a fully saturated dip_state.yml is safely and deterministically projected into the immutable GEMINI.md anchor.
  - *Dependencies:* node_4a_execute_matrix_schema
- **node_7_plan_csi_guard_execute** [PLAN]: Plan CSI Guard for Execute Nodes
  - *Goal:* Design and test a deterministic CLI command (e.g., ./bin/node complete) that enforces the Testing Invariant before allowing a node to transition to DONE.
- **node_9_probe_css_presentation** [PROBE]: Probe Missing CSS Presentation
  - *Goal:* Investigate why the Agent consistently fails to explicitly present the CSS (Continue, Start, Stop) template in the chat UI during Dyad Retros, despite the mechanical UI presentation firing in the logs.
