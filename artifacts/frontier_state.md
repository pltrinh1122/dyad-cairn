# The Frontier State (DAG)

> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**
> Source of truth is `artifacts/frontier_state.yml`.
> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.


## 🔴 DONE NODES
- **node_0**: Instantiate Workflow State-Machine
  - *Goal:* Build the physical tracking layer for our SPAOR loop (this Frontier DAG and the LIFO Execution Stack).
- **node_1**: Cut First Stone (Hard Guardrails Playbook)
  - *Goal:* Extract the hard-guardrails lesson into a formal stone.yaml package and PR it to the commons/ Library.
  - *Dependencies:* node_0
- **node_2a**: Mason Toolchain Scaffold & CLI Skeleton
  - *Goal:* Build the generic CLI shell (./bin/mason) including argument parsing, logging, and I/O.
  - *Dependencies:* node_0
- **node_2b**: Mason Validation Engine & Installation Logic
  - *Goal:* Implement the strict schema validation against the local stone.yaml schema format and installation logic.
  - *Dependencies:* node_2a
