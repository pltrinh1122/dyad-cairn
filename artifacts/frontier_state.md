# The Frontier State (DAG)

> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**
> Source of truth is `artifacts/frontier_state.yml`.
> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.


## 🟡 IN_REVIEW NODES
- **node_19_probe_state_sync_collision** [PROBE]: Probe Ledger and State Sync Collision
  - *Goal:* Investigate the Ledger and State Sync Collision. Determine the physical invariants for how concurrent agents mutating the same structural files resolve data consistency and merge conflicts without shattering.
  - *Dependencies:* node_4c_probe_anchor_compilation
- **node_20_probe_authorization_gate_collision** [PROBE]: Probe Authorization Gate Collision
  - *Goal:* Investigate the Authorization Gate Collision where a full-auto Executioner clone running PLAN+EXECUTE autonomously bypasses the HTIL Design-Review Gate.
  - *Dependencies:* node_19_probe_state_sync_collision
- **node_21_probe_reflect_boundary_collision** [PROBE]: Probe Reflect Boundary Collision
  - *Goal:* Investigate the Reflect Boundary Collision. Determine invariants for how agents coordinate git states during reflect-green.
  - *Dependencies:* node_19_probe_state_sync_collision
- **node_22_probe_retro_css_formatting** [PROBE]: Probe RETRO CSS Formatting
  - *Goal:* Spin up a trail to investigate the root cause of why RETRO logs are not presented using the CSS template, and resolve the formatting.

## 🔴 BLOCKED NODES
- **node_4c_probe_anchor_compilation** [PROBE]: Probe Anchor Compilation Invariant
  - *Goal:* Investigate how a fully saturated dip_state.yml is safely and deterministically projected into the immutable GEMINI.md anchor.
  - *Dependencies:* node_4a_execute_matrix_schema
