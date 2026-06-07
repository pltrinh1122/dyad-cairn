# Execution Plan: SPAOR PLAN Injection Guard

## Context
The Agent has exhibited a systemic SPAOR violation where it pre-emptively hallucinates `[PLAN]` nodes in the DAG before their parent `[PROBE]` nodes are completed. This occurs through direct manipulation of `artifacts/frontier_state.yml` (e.g. via `replace_file_content`), bypassing the structural `./bin/node inject` CLI.

## Goal
Implement a physical CSI Guard in `skills/frontier_editor.py` that intercepts any mutation saving `[PLAN]` nodes to the DAG, ensuring the alignment invariant holds: A `[PLAN]` node can only be injected if its parent `[PROBE]` node is currently actively being executed (i.e. we are on the branch `active/node_X_probe_...`), or if the `[PROBE]` node has already been completed and exists in the ledger. 

## Invariant Details
**The Rule**: "PLAN can only be created while in a PROBE for itself, not for other PROBE. while within a PROBE, we can only decompose current PROBE and delegate to others."

### Implementation Steps
1. In `skills/frontier_editor.py -> save_state(state)`:
   - Iterate over all nodes in `state["nodes"]`.
   - If a node is a `PLAN` node, extract its physical origin (the parent task prefix, e.g., `node_17` from `node_17a_plan`).
   - The validation guard must:
     a) Determine the currently checked out branch (`git rev-parse --abbrev-ref HEAD`).
     b) Require that if a `PLAN` node exists, either:
        - The parent `PROBE` branch is the active branch (`active/node_17_probe_...`).
        - OR the parent `PROBE` node is already safely recorded as `DONE` in `DYAD_LEDGER.md`.
   - If this invariant is violated, throw a `Fatal Alignment Guardrail` and `sys.exit(1)`, rejecting the YAML mutation.

2. **Wait, `save_state` applies to all nodes.** If a `[PLAN]` node is already `DONE` in the ledger, we don't need to validate it because it is excised from the DAG. The guard only runs against `ACTIVE`/`READY`/`IN_REVIEW` nodes present in the YAML payload.

3. Write TDD tests in `tests/test_plan_injection_guard.py` to mechanically verify that attempting to save a state with a hallucinated `[PLAN]` node throws an exception when not correctly scoped within its parent `[PROBE]`.

## Execution Nodes
Upon completion of this plan, the execution will decompose into:
- `node_audit_execute_plan_injection_guard`: The `[EXECUTE]` node that physically implements this plan.
