# The Frontier State (DAG)

> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**
> Source of truth is `artifacts/frontier_state.yml`.
> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.


## 🟡 IN_REVIEW NODES
- **node_12_plan_ontological_binder** [PLAN]: Construct the Ontological Binder
  - *Goal:* Build bin/bind to enforce simultaneous mutation of the Ledger, AGENT.md, and the physical substrate.
- **node_14_plan_design_review_gate** [PLAN]: Construct the Design-Review Gate
  - *Goal:* Build bin/node inject (defaults to IN_REVIEW) and bin/node authorize (flips to READY) to map the lean. and lean! HTIL gates.
- **node_15_plan_wuwei_closure_gate** [PLAN]: Construct the Wu-Wei Closure Gate
  - *Goal:* Update skills/flow_state_manager.py to enforce a retro_msg synthesis block on reflect-green.
