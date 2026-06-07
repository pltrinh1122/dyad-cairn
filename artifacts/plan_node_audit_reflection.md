# Execution Plan: Reflection Review HITL Blocks

## Context
1. **Design Review Gate:** Nodes injected into the Frontier DAG halt at `IN_REVIEW` pending Operator `lean!`. The Audit DAG currently suffers from this as well. It should skip it and be evaluated topologically immediately (straight to `READY` or `BLOCKED`).
2. **Reflection Review Gate:** Both DAGs must feature a HITL block before trail synthesis (`TRAIL-RETRO`) is durably merged and the trail is pruned.

## Implementation Plan

### 1. Audit DAG: Bypassing Design Review
In `skills/flow_state_manager.py` within `inject_node()`:
- Check if the current context is the Audit DAG (`"audit" in os.environ.get("DYAD_DAG_STORE", "")`).
- If it is the Audit DAG, do NOT set `state["nodes"][node_id]["status"] = "IN_REVIEW"`. Simply allow it to be injected without an explicit status, so `derive_status` evaluates it as `READY` or `BLOCKED`.
- For Frontier DAG, continue to set `"status": "IN_REVIEW"`.

### 2. Both DAGs: Reflection Review Gate (`trail-reflect` & `trail-dispose`)
The trail closure sequence is currently a synchronous monolithic action (`trail_reflect`). It must be fractured into two mechanical steps:
- **`trail_reflect(trail_id, retro_msg)`**:
  - Branches to `active/reflect_{trail_id}`.
  - Appends `retro_msg` to the Ledger.
  - Commits, pushes to remote.
  - Generates a Pull Request titled `[REFLECT] Trail Synthesis {trail_id}`.
  - **HALTS** (Transitions the state in the Dyad to await Operator Review).
- **`trail_dispose(trail_id)`**:
  - Executed explicitly by the Operator (e.g., via `./bin/node dispose {trail_id}`).
  - Automatically merges the `[REFLECT]` PR (`gh pr merge --merge --delete-branch`).
  - Closes the Orchestrator's tracking GH Issue (`gh issue close {trail_id}`).
  - Prunes the trail from the DAG (`python3 skills/frontier_editor.py {trail_id} PRUNE`).

### Test Assertions (Red Phase)
- Modify `tests/test_trail_reflect.py` to assert that `fsm.trail_reflect` creates a PR and halts, rather than pruning.
- Add `tests/test_trail_dispose.py` to assert `trail_dispose` merges the PR, closes the issue, and prunes.
- Update `tests/test_plan_injection_guard.py` or create `tests/test_audit_injection.py` to assert that Audit DAG injections skip `IN_REVIEW`.
