# Execution Plan: Frontier ASCII Tree and IN_REVIEW Override

## Context
The Operator raised two feedback observations:
1. `artifacts/frontier_state.md` is no longer presented as an ASCII-tree reflecting DAG relationships.
2. `IN_REVIEW` is meaningless without dependencies. Nodes are showing as `IN_REVIEW` even when they are physically `BLOCKED` by prerequisites.

## Root Cause Analysis
1. **ASCII-Tree Erasure:** In `skills/frontier_editor.py`, the Materialized View generation (lines 96-129) replaced the original `skills/frontier_reader.py::build_tree()` invocation with a flat, status-grouped list. This erases the topological structure from the markdown projection.
2. **IN_REVIEW Override:** In `skills/frontier_editor.py` (line 108), the status is explicitly overridden to `IN_REVIEW` if `current_cache == "IN_REVIEW"`, bypassing `derive_status`. This allows blocked nodes (e.g. `node_20`) to masquerade as reviewable before their dependencies (e.g. `node_19`) are complete.

## Implementation Plan
1. **Fix IN_REVIEW Logic:**
   - In `skills/frontier_editor.py` inside `save_state`, update the status resolution to compute the derived status *first*.
   - Only allow `IN_REVIEW` if the derived status evaluates to `READY` or `ACTIVE` (though `ACTIVE` overrides it anyway).
   ```python
   derived = derive_status(node_id, data, state["nodes"])
   if data.get("status") == "IN_REVIEW" and derived == "READY":
       status = "IN_REVIEW"
   else:
       status = derived
   ```

2. **Restore ASCII-Tree Rendering:**
   - Refactor `skills/frontier_reader.py::build_tree(nodes)` to return a list of formatted string lines instead of printing to `stdout`.
   - Update `skills/frontier_editor.py` to import `build_tree` and use its output to generate `MD_FILE`.
   - Ensure the printed nodes in the tree continue to display their title, goal, and type correctly formatted.

## Execution Nodes
- `node_23_plan_frontier_ascii_tree`: Structural PLAN node (injects this plan).
- `node_23a_execute_frontier_ascii_tree`: Implements the tree rendering and IN_REVIEW fix.
