# Architectural Reflect: Substrate Concurrency & Ledger Collisions

## 1. Symptom & Evidence
During concurrent subagent execution, the `dyad-state/ledger.jsonl` and `DYAD_LEDGER.md` manifest massive bursts of `collision_intent_*` items with identical/near-identical timestamps (e.g., `2026-06-22 18:21:49.538...`).
These collisions originate from the `TODO` action (via `bin/todo`), which calls `ledger_manager.append_ledger`.

## 2. Root Cause Analysis (FSM State Synchronization)
The DYAD architecture correctly partitions execution into two regimes:
- **Outer-FSM (Independent)**: `WIP-N = 1` for Substrate State mutations (DAG, Ledger).
- **Inner-FSM (Dependent)**: `WIP-N > 1` for parallel payload execution.

However, **there is no physical lock or serialization mechanism** enforcing the `WIP-N = 1` invariant at the file system level. 
When multiple Inner-FSM subagents autonomously run actions that mutate the Substrate State (e.g., `bin/todo`, `complete_node`, `reflect_node_green`), they execute concurrently:
1. `ledger_manager.append_ledger` opens `ledger.jsonl`, appends, and then simultaneously reads and rewrites the entire `DYAD_LEDGER.md`. Concurrent rewrites of the markdown file cause data loss, corruption, and interleaving.
2. `bin/todo` concurrently reads and writes to `artifacts/todos/` and rewrites `artifacts/todos.md`.
3. `frontier_editor.py save_state` reads and rewrites the DAG yml files and generates `frontier_state.md`.

These scripts currently assume they are the only actor operating at any given millisecond, which is false under autonomous concurrent execution.

## 3. Proposed Structural Fix (The Bake)
We must implement a **Substrate Concurrency Lock** using standard POSIX `fcntl.flock`.

### A. The Mechanism
Create a universal locking decorator or context manager in `skills/substrate_lock.py` that acquires an exclusive file lock on a dedicated `dyad-state/substrate.lock` file.

### B. The Integration Points
1. `ledger_manager.py`: Wrap `append_ledger`, `append_carry_forward`, and `process_retro` with the lock.
2. `frontier_editor.py`: Wrap `save_state` and `load_state` (or at least mutations) with the lock.
3. `flow_state_manager.py`: Wrap `session_start`, `session_end`, and `d_start` (which modify `fsm_state.yml`) with the lock.
4. `bin/todo`: Wrap the todo file generation loop with the lock.

This physically enforces the `WIP-N = 1` invariant at the OS level across all concurrent processes.

## 4. Next Steps
1. Push the RED Phase PR containing failing tests that assert `fcntl.flock` is invoked during Substrate mutations.
2. Await Operator Intent Validation.
3. In the GREEN Phase, implement `substrate_lock.py` and apply it to the designated targets.
