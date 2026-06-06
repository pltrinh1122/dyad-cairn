# The SPAOR Workflow Engine

This document defines the exact mechanical mapping between the **SPAOR Execution Loop** and our physical **State-Machine Architecture** (The DAG and the LIFO Stack).

## 1. SENSE (Horizon Scan)
*Where are we, and what is unlocked?*
- **Action:** Read `artifacts/frontier_state.yml` to identify the current `ACTIVE` Node. 
- **Rule:** If `ACTIVE` count is 0, scan for `BLOCKED` nodes that have had all dependencies met.
- **Physical Tool:** `skills/frontier_editor.py` (to read the computational state) and `./bin/backlog list` (to check remote GH alignment).

## 2. PLAN (Blueprinting & Racking)
*Prepare the environment and unroll the execution footprint.*
- **Action:** Transition the newly unlocked Node to `ACTIVE` (Strictly enforcing WIP-N=1).
- **Action:** Use `./bin/backlog rack <node_id>` to formalize the Node as a GitHub Issue in the Commons Backlog.
- **Action:** Exhaustively map the Data, Logic, and Orchestration files required.
- **Physical Tool:** Use `./bin/prompt push <task>` to completely populate the LIFO Execution Stack (`prompt_backlog.yml`) with the necessary steps *before* writing code.
- **Physical Tool:** Execute `./bin/node checkout` to switch to an isolated `active/<node_id>` git branch.

## 3. ACT (The Depth-First Chisel)
*Execute tactical steps and computationally validate them.*
- **Action:** Loop `./bin/prompt pop` to pull the top-most instruction.
- **Action:** Generate code (`skills/`, `bin/`, `tests/`).
- **Action:** If unexpected friction occurs, `./bin/prompt push` the sub-task to mathematically enforce depth-first resolution.
- **Physical Tool:** Use `./bin/run-tests` to satisfy the Validation (V) Invariant. Manual inspection is invalid.
- **Exit Condition:** The Act phase loops until the LIFO Stack is completely `EMPTY`.

## 4. OBSERVE (The PR Gate)
*Halt execution and defer to HITL.*
- **Action:** The code is complete and validated locally. We must transition across the Boundary.
- **Physical Tool:** Execute `./bin/node reflect`. This pushes the branch, generates the Pull Request, and mutates the Node in `frontier_state.yml` from `ACTIVE` to `IN_REVIEW`.
- **Rule:** Execution on this Node halts. The Agent is mathematically cleared to `Sense` the next unlocked Node while this PR waits for Operator/Commons ratification (Parallel WIP > 1 at the Review layer).

## 5. REFLECT (Ledger Anchor)
*Consolidate knowledge after the merge.*
- **Action:** Once the PR is merged, update `frontier_state.yml` to `DONE`.
- **Physical Tool:** Use `./bin/retro` or `./bin/clip` to append any structural lessons or friction extracted during the cut directly to the `DYAD_LEDGER.md`. 
- **Cycle:** Loop back to Step 1 (Sense).
