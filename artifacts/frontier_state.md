# The Frontier State (DAG)

> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**
> Source of truth is `artifacts/frontier_state.yml`.
> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.

```text
├── node_19a_probe_pre_merge_sync [IN_REVIEW] [PROBE]: Probe Pre-Merge Sync
│   ├── node_20_probe_authorization_gate_collision [BLOCKED] [PROBE]: Probe Authorization Gate Collision
    ├── node_21_probe_reflect_boundary_collision [BLOCKED] [PROBE]: Probe Reflect Boundary Collision
├── node_19b_probe_ledger_resolution [IN_REVIEW] [PROBE]: Probe Ledger Resolution
│   ├── node_20_probe_authorization_gate_collision [BLOCKED] [PROBE]: Probe Authorization Gate Collision
    ├── node_21_probe_reflect_boundary_collision [BLOCKED] [PROBE]: Probe Reflect Boundary Collision
├── node_19c_probe_state_merging [IN_REVIEW] [PROBE]: Probe Structural State Merging
│   ├── node_20_probe_authorization_gate_collision [BLOCKED] [PROBE]: Probe Authorization Gate Collision
    ├── node_21_probe_reflect_boundary_collision [BLOCKED] [PROBE]: Probe Reflect Boundary Collision
```
