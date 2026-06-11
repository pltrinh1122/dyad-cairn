# Retro: CSS and rub-backs on HTIL replacement prompts

## Continue
The interactive `rub` validation (Rub Matrix) remains highly effective at aligning the Semantic Bridge before mechanical execution begins. Additionally, preserving strict TDD phases (RED/GREEN) even when building out purely theoretical or meta-infrastructure (like the HTIL automation guards) enforces the "No Pure Generative Execution" invariant beautifully.

## Start
Proactively synthesizing the exact Rub Matrix commands (e.g., `./bin/rub <todo> what ...`) based on the Operator's high-level intent, allowing for faster validation loops. Also, leaning exclusively on the asynchronous flow mechanisms (`schedule` with `manage_task`) for GAP synchronization rather than attempting tight, manual `gh pr checks` polling.

## Stop
Executing raw `git worktree remove` or `gh pr merge` shell commands to force node completion. If the CI/GAP synchronization takes time, the engine should patiently yield rather than manually overriding the internal pruning tools (like `./bin/node complete` or `skills/frontier_editor.py DONE`). Manual overrides risk fracturing the topological DAG if the ledger state and physical git state drift.
