# The Frontier State (DAG)

> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**
> Source of truth is `artifacts/frontier_state.yml`.
> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.


## 🔴 BLOCKED NODES
- **node_14a_plan_design_review_gate** [PLAN]: Implement DAG Authorization Lock
  - *Goal:* Build ./bin/node inject and ./bin/node authorize to physically decouple node creation from execution authorization.
  - *Dependencies:* node_16_probe_stone_schema
