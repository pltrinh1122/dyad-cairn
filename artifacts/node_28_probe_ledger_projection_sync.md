# Design Review: Ledger Projection Sync

## Hypothesis
The materialization of `frontier_state.md` as a physical, tracked artifact forces an unnatural coupling between the Ledger (append-only) and the Orchestrator (DAG compiler). Autonomous scripts writing to the Ledger cause "drift" because they bypass the orchestrator.

## Synthesis
We falsified the requirement that `frontier_state.md` must be tracked in Git for PR gating. We reached an architectural consensus:
1. Abolish the tracked `artifacts/frontier_state.md` file.
2. Generate it strictly as an ephemeral, post-hoc projection when `./bin/read` is invoked.
3. Move `artifacts/frontier_state.md` to `.gitignore` to prevent any future Git-tracked drift.

## Decomposition
- **node_28a_execute_ephemeral_projection**: "Execute the Ephemeral Projection strategy by untracking artifacts/frontier_state.md, adding it to .gitignore, and ensuring bin/read generates it purely on-the-fly."
