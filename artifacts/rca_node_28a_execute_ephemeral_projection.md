# Execution RCA: Ephemeral Projection Strategy

## Falsification & Context
The architecture previously persisted `artifacts/frontier_state.md` to git as a materialized spatial view of the chronological ledger. This created an unnatural coupling where autonomous processes appending to the ledger bypassed the physical closure scripts, causing architectural drift.
We established that tracking the materialization in Git for PR gating is unnecessary because the HTIL gate can rely on an ephemeral, post-hoc snapshot computed on-the-fly.

## Execution
1. Moved `artifacts/frontier_state.md` and `artifacts/audit_state.md` to `.gitignore`.
2. Removed them from Git tracking (`git rm --cached`).
3. Modified `skills/flow_state_manager.py`'s `create_reflection_pr` method to dynamically compute the DAG state using `skills.frontier_reader.build_tree` and inject the textual representation into the body of generated Pull Requests.
4. Validated execution with `tests/test_ephemeral_projection.py`.
