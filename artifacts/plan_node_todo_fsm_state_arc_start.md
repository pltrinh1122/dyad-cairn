# Execution Plan: Define state_arc_start.md anchor

## 1. Intent
Define the `state_arc_start.md` anchor. This provides a structural template for starting a state arc in the FSM, specifically for SUBSTRATE level operations.

## 2. Structural Invariants
- `kb/templates/state_arc_start.md` must exist and define the invariant layout for a state arc start.
- The template must contain the basic markdown structure for initiating a state arc.

## 3. Red Phase Tests
- `tests/test_fsm_state_arc_start.py` will assert that `kb/templates/state_arc_start.md` exists and contains the necessary schema heading `# State Arc Start`.
