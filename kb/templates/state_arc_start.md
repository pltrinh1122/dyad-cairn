# State Arc Start

## Intent
<What is the exact goal of this state arc?>

## Initial State
<What is the current state of the workspace and the DAG?>

## Actions Required
- [ ] Define boundaries
- [ ] List required nodes
- [ ] Identify dependencies

## Transition Conditions
<What must be true for this state arc to be considered complete?>


## Invariants
- **PR Constraint:** The Agent must never use raw `gh pr create` or `gh pr merge`. All PR actions must be mapped to `./bin/pr-sync`.
