# STATE: ARC-END

## Phase: Reflect & Synthesis
The arc-end state is the physical marker that the current execution arc has concluded its active implementation phase and must now undergo retrospective and synthesis.

## Invariants
- **PR Constraint:** The Agent must never use raw `gh pr create` or `gh pr merge`. All PR actions must be mapped to `./bin/pr-sync`.
1. **No Execution:** The Agent must not begin a new task or execute any proactive changes while in this state.
2. **Synthesis Required:** The Agent must synthesize the completed arc, logging the outcomes and updating the DYAD_LEDGER.md.

## Transitions
From ARC-END, the valid transitions are:
- `session-end`: If the Operator indicates the session is over.
- `arc-start`: If the Operator initiates a new execution arc.
