# The Frontier State (DAG)

> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**
> Source of truth is `artifacts/frontier_state.yml`.
> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.

```text
├── node_4c_probe_anchor_compilation [ACTIVE] [PROBE]: Probe Anchor Compilation Invariant
    ├── node_19_probe_state_sync_collision [BLOCKED] [PROBE]: Probe Ledger and State Sync Collision
    │   ├── node_20_probe_authorization_gate_collision [BLOCKED] [PROBE]: Probe Authorization Gate Collision
        ├── node_21_probe_reflect_boundary_collision [BLOCKED] [PROBE]: Probe Reflect Boundary Collision
├── node_4c_plan_anchor_compiler [IN_REVIEW] [PLAN]: Anchor Compilation Schema
├── node_4c_execute_anchor_compiler [IN_REVIEW] [PLAN]: Anchor Compiler Implementation
```
