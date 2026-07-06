# Reflect: GAP Polling Race Condition & Flow Manager State Overrides

## Continue
- Relying on the deterministic test suite to falsify implementations before proceeding to the Green Phase merge.
- Using mechanical validation (Dialect Linter, Testing Harness) to rigorously enforce the Consistency Guardrails and prevent broken state transitions.

## Start
- Before modifying shared orchestrator scripts (`skills/flow_state_manager.py`), we must strictly verify the active branch context or commit fixes locally within the subagent worktree to prevent unintentionally overwriting active parallel work.
- We must anticipate structural race conditions in distributed systems (such as GitHub Actions pipeline polling) and proactively implement deterministic retry loops rather than relying on brittle, hardcoded sleep intervals.

## Stop
- Blindly copying files from the `main` directory into active parallel worktrees, which effectively deletes subagent context and triggers regression failures.
