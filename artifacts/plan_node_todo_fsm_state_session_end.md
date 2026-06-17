# Execution Plan: Define state_session_end.md anchor

## 1. Intent
Define the `state_session_end.md` anchor. This provides a structural template for ending a state session in the FSM, specifically for SUBSTRATE level operations.

## 2. Structural Invariants
- `kb/templates/state_session_end.md` must exist and define the invariant layout for a state session end.
- The template must contain the basic markdown structure for concluding a state session.

## 3. Red Phase Tests
- `tests/test_fsm_state_session_end.py` will assert that `kb/templates/state_session_end.md` exists and contains the necessary schema heading `# State Session End`.
