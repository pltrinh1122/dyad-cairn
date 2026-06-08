# Execution Spec: Node Audit RCA Narrative Summary

## Goal
Enforce deterministic structural artifacts for EXECUTE and REFLECT nodes to satisfy the Operator's requirement for industry-standard Root Cause Analysis (RCA) reporting and Synthesis Narratives.

## Strategy
1. **EXECUTE RCA:** Any node containing `_execute_` transitioning to DONE (via `complete` or `reflect-green`) MUST physically possess an RCA artifact at `artifacts/rca_<node_id>.md`.
2. **REFLECT Narrative Synthesis:** `trail-reflect` MUST physically ingest its retro message from `artifacts/trail_synthesis_<trail_id>.md` instead of CLI arguments. The artifact MUST contain specific sub-headings asserting the "Probe Invariant" and "Execution RCA".

## Red Phase (TDD)
**`tests/test_node_complete.py` & `tests/test_trail_reflect.py`**
1. **Test EXECUTE RCA Guard:** `complete_node` and `reflect_node_green` must trap and exit(1) if `_execute_` is in the node ID but `artifacts/rca_<node_id>.md` is missing.
2. **Test Trail Synthesis Guard:** `trail_reflect` must trap and exit(1) if `artifacts/trail_synthesis_<trail_id>.md` is missing.
3. **Test Trail Synthesis Narrative Guard:** `trail_reflect` must trap and exit(1) if the synthesis artifact lacks the keywords "Probe Invariant" or "Execution RCA".

## Green Phase (Implementation)
**`skills/flow_state_manager.py`**
1. Inject the RCA file guard in both `complete_node` and `reflect_node_green`:
```python
    if "_execute_" in node_id:
        rca_file = f"artifacts/rca_{node_id}.md"
        if not os.path.exists(rca_file):
            print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
            print(f"Missing RCA artifact. EXECUTE nodes must author an industry standard RCA at '{rca_file}'.")
            sys.exit(1)
```
2. Refactor `trail_reflect` to read the payload from `artifacts/trail_synthesis_<trail_id>.md` and enforce the Narrative Content:
```python
    synthesis_file = f"artifacts/trail_synthesis_{trail_id}.md"
    if not os.path.exists(synthesis_file):
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print(f"Missing Trail Synthesis artifact. REFLECT must author '{synthesis_file}'.")
        sys.exit(1)
        
    with open(synthesis_file, "r") as f:
        retro_msg = f.read()
        
    if "Probe Invariant" not in retro_msg or "Execution RCA" not in retro_msg:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("Trail Synthesis must explicitly contain 'Probe Invariant' and 'Execution RCA'.")
        sys.exit(1)
```
3. Update `sys.argv` parsing for `trail-reflect` so `retro_msg` is no longer a mandatory CLI positional argument.

## Closure
Once tests fail (Red) and pass (Green), transition to DONE.
