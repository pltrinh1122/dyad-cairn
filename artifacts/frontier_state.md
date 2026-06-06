# The Frontier State (DAG)

> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**
> Source of truth is `artifacts/frontier_state.yml`.
> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.


## 🟢 ACTIVE NODES
- **node_0**: Instantiate Workflow State-Machine
  - *Goal:* Build the physical tracking layer for our SPAO loop (this Frontier DAG and the LIFO Execution Stack).

## 🔴 BLOCKED NODES
- **node_1**: Cut First Stone (Hard Guardrails Playbook)
  - *Goal:* Extract the hard-guardrails lesson into a formal stone.yaml package and PR it to the commons/ Library.
  - *Dependencies:* node_0
- **node_2**: The Mason Toolchain (The Chisel)
  - *Goal:* Build the ./bin/mason universal validation and installation CLI for the Commons.
  - *Dependencies:* node_1
