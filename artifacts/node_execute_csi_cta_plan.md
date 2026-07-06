# Architectural Plan: node_execute_csi_cta

## Context
The Dyad architecture strictly preserves the human Operator's asymmetry. The Agent acts as an Executioner bound by constraints. If the Operator uses a "pure command" (i.e. one lacking an explicit semantic prefix such as `rub:`, `riff:`, `execute:`), the Agent must not silently execute it and assume authorization. The Agent must convert it into an Operator Call to Action (CTA), requesting the Operator to run it or explicitly grant execution.

## The Goal
Modify `skills/dialect_linter.py` to assert this CSI Guard:
- If a `USER_INPUT` does not start with any recognized dialect prefix.
- And the Agent responds by invoking a command (e.g., `CommandLine`).
- The Linter must raise a violation.

## Implementation Steps
1. In `skills/dialect_linter.py`, compile a list of recognized prefixes: `["read:", "audit:", "rub:", "rub?", "reflect:", "lean:", "lean?", "riff:", "execute:", "plan:", "probe:", "todo:"]`.
2. For each `USER_INPUT`, check if it starts with any of these prefixes.
3. If it does not, scan the `PLANNER_RESPONSE` for any tool calls that execute a script or raw command (`CommandLine`).
4. If found, append a violation: "Violation at step X: Operator issued a pure command without a dialect prefix. Agent executed a raw command. Agent must convert this into an Operator CTA."
5. Ensure the failing test in `tests/test_dialect_linter.py` validates this logic.

## Falsifiability
- `tests/test_dialect_linter.py` will contain a scenario testing this CSI guard.
- Remote GAP pipeline validates this.
