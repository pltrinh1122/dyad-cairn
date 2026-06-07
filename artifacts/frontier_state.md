# The Frontier State (DAG)

> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**
> Source of truth is `artifacts/frontier_state.yml`.
> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.


## 🔴 BLOCKED NODES
- **node_4c_probe_anchor_compilation** [PROBE]: Probe Anchor Compilation Invariant
  - *Goal:* Investigate how a fully saturated dip_state.yml is safely and deterministically projected into the immutable GEMINI.md anchor.
  - *Dependencies:* node_4a_execute_matrix_schema
- **node_12_plan_local_executioner_loop** [PLAN]: Plan Local Executioner Worktree Architecture
  - *Goal:* Design and formalize the Git Worktree partitioning strategy and the `./bin/claude-watch` listener script to safely isolate the Claude execution thread from the Architect's workspace without substrate entanglement.
  - *Dependencies:* node_13_probe_authorization_gate_collision

## 🔴 READY NODES
- **node_4b_execute_sonar_halting** [EXECUTE]: Execute Provenance Extraction Invariant
  - *Goal:* Implement the markdown parser in dip_sonar.py to dynamically extract the required dimensions, passing the TDD tests.
- **node_13_probe_authorization_gate_collision** [PROBE]: Probe Authorization Gate Collision
  - *Goal:* Investigate the Authorization Gate Collision where a full-auto Executioner clone running PLAN+EXECUTE autonomously bypasses the HTIL Design-Review Gate ('lean!'). Determine the architectural invariant for mapping the SPAOR phases across the dual-agent boundary.
