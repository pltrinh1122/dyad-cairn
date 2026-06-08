# Root Cause Analysis: node_audit_design_review_invariants

## 1. Description of the Issue
The `skills/design_review_ui.py` script mechanically gates the HTIL Design Review for `PLAN` nodes. However, it only surfaced the raw `goal:` string defined in `frontier_state.yml`. The Operator pointed out that this structural failure abstracted away the actual value discovered by the PROBE: the Unfalsified Condition, the Physical Invariants, and the logical Decomposition. Without these presented in the UI, the Operator could not effectively evaluate the true merit and structural validity of the proposed execution.

## 2. Root Cause
The presentation layer in `design_review_ui.py` was simply accessing the YAML definition of the `PLAN` node. It lacked a logical mapping to retrieve and extract the structural context documented by the parent `PROBE` node. 

## 3. Resolution Steps
- Implemented a structural parser inside `skills/design_review_ui.py` using robust Regex anchored to markdown H2 headers (`(?im)^##\s+`).
- The parser maps `node_{prefix}_plan_...` back to its physical markdown artifact `artifacts/probe_{prefix}_*.md`.
- Extract and explicitly present the `Unfalsified Condition` and `Discovered Invariants`.
- Implement a physical fallback check to mechanically detect decomposition strategy (by querying `frontier_state.yml` for multiple `PLAN` nodes sharing the same parent prefix) if no explicitly formatted markdown section exists.
- Renamed the existing `probe_state_sync_collision.md` to conform to the strict prefix naming convention (`probe_node_19_state_sync_collision.md`), cementing this as a physical invariant for all future `PROBE` nodes.

## 4. Testing
- Executed `python3 skills/design_review_ui.py node_19_plan_state_sync`.
- Mechanically verified that the output correctly rendered the exact markdown blocks containing the collision condition and the 3 physical invariants, and properly calculated the fallback decomposition strategy.
