# State Session End

## Summary
(Write a summary of the session here)

## Artifacts Generated
- (List artifacts)

## Outstanding Issues
- (List remaining issues or blockers)

## Hand-off Notes
- (Notes for the next session)

## Closure Guardrails
- `reflect-green` / `complete` (Wu-Wei Closure). **Mechanically mapped to:** requiring a `<reflect_msg>` argument to append the closure synthesis to the Ledger before locking the state.

## Invariants
- **PR Constraint:** The Agent must never use raw `gh pr create` or `gh pr merge`. All PR actions must be mapped to `./bin/pr-sync`.
