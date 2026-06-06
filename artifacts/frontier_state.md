# The Frontier State (DAG)

> This file is the topological tracker for `dyad-cairn`. It maps the strategic dependencies of our macroscopic milestones. 
> **WIP-N=1:** Only one Node may be ACTIVE at a time.

## 🟢 ACTIVE NODE
- **Node 0: Instantiate Workflow State-Machine**
  - *Goal:* Build the physical tracking layer for our SPAO loop (this Frontier DAG and the LIFO Execution Stack).
  - *Required Artifacts:* `artifacts/frontier_state.md`, `artifacts/prompt_backlog.yml`, and the `./bin/backlog` CLI interface.
  - *Status:* **ACTIVE** (In Progress)

## 🔴 BLOCKED / RACKED NODES
- **Node 1: Cut First Stone (Hard Guardrails Playbook)**
  - *Goal:* Extract the hard-guardrails lesson into a formal `stone.yaml` package and PR it to the `commons/` Library.
  - *Dependency:* Blocked by Node 0 (We must finish the state-machine before executing complex cross-repo work).
  - *Status:* **BLOCKED**

- **Node 2: The Mason Toolchain (The Chisel)**
  - *Goal:* Build the `./bin/mason` universal validation and installation CLI for the Commons.
  - *Dependency:* Blocked by Node 1 (We must manually push the first Stone to validate the protocol before automating it).
  - *Status:* **BLOCKED**

---
*Last mutated during Session 2.*
