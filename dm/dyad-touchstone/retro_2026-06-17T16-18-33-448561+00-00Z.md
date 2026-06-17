# Retro: Extracting Workflow Invariants to FSM Templates

## Continue
- Using the Invisible Elicitor protocol (`ask_question`) to define the WHY, WHAT, and SCOPE before locking a node in the DAG.
- Offloading the actual execution securely to subagents, maintaining the parallel branch and PR review invariant.

## Start
- We must explicitly ensure executable permissions (`chmod +x`) are set on all newly created or modified scripts to prevent mechanical CI failures.

## Stop
- Relying on global `DYAD.md` documentation for state-specific operations. We must strictly enforce writing mechanical bindings directly into their corresponding `kb/templates/state_*.md` files.
