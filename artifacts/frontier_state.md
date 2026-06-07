# The Frontier State (DAG)

> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**
> Source of truth is `artifacts/frontier_state.yml`.
> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.


## 🔴 BLOCKED NODES
- **node_4c_probe_anchor_compilation** [PROBE]: Probe Anchor Compilation Invariant
  - *Goal:* Investigate how a fully saturated dip_state.yml is safely and deterministically projected into the immutable GEMINI.md anchor.
  - *Dependencies:* node_4a_execute_matrix_schema
- **node_12b_plan_authorization_handshake** [PLAN]: Plan Executioner Authorization Handshake
  - *Goal:* Formalize the ./bin/claude-watch listener script to strictly halt Claude's execution pending the lean! authorization gate.
  - *Dependencies:* node_12a_plan_worktree_substrate
- **node_12c_plan_reflect_handoff** [PLAN]: Plan REFLECT Execution Handoff
  - *Goal:* Formalize the mechanical transfer of the functional execution logs from Claude's Worktree back to the Architect to satisfy the structural REFLECT boundary.
  - *Dependencies:* node_12a_plan_worktree_substrate

## 🔴 READY NODES
- **node_4b_execute_sonar_halting** [EXECUTE]: Execute Provenance Extraction Invariant
  - *Goal:* Implement the markdown parser in dip_sonar.py to dynamically extract the required dimensions, passing the TDD tests.
- **node_12a_plan_worktree_substrate** [PLAN]: Plan Local Worktree Partition
  - *Goal:* Design and formalize the Git Worktree partitioning strategy to safely isolate the Claude execution thread from the Architect's workspace based on the Context Partition invariant.
