# The Frontier State (DAG)

> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**
> Source of truth is `artifacts/frontier_state.yml`.
> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.


## 🟢 ACTIVE NODES
- **node_14_probe_state_sync_collision** [PROBE]: Probe Ledger and State Sync Collision
  - *Goal:* Investigate the Ledger and State Sync Collision. Determine the physical invariants for how concurrent agents mutating the same structural files (DYAD_LEDGER.md, frontier_state.yml) resolve data consistency and merge conflicts without shattering autonomous execution.

## 🔴 BLOCKED NODES
- **node_4c_probe_anchor_compilation** [PROBE]: Probe Anchor Compilation Invariant
  - *Goal:* Investigate how a fully saturated dip_state.yml is safely and deterministically projected into the immutable GEMINI.md anchor.
  - *Dependencies:* node_4a_execute_matrix_schema

## 🔴 READY NODES
- **node_4b_execute_sonar_halting** [EXECUTE]: Execute Provenance Extraction Invariant
  - *Goal:* Implement the markdown parser in dip_sonar.py to dynamically extract the required dimensions, passing the TDD tests.
- **node_16_probe_reflect_boundary_collision** [PROBE]: Probe REFLECT Boundary Collision
  - *Goal:* Investigate the ownership of the [REFLECT] phase across the dual-agent boundary. If the Executioner executes the logic, how does the Architect synthesize the structural retro without hallucinatory decoupling? Determine the mechanical hand-off of the functional execution logs to the structural state.
