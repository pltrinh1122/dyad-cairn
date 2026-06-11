# Research: Cognitive Tax of Context-Switching vs. Sequential Execution

## Background
The Operator questioned whether the terminal lock-up caused by `/goal` (sequential execution) is a bug or an essential Wu-Wei constraint designed to protect Operator attention.

## Findings
During the execution of node `node_todo_1781173503`, the Operator provided explicit falsification of the sequential execution constraint:
> "i'd like to retire the use of `/goal` as that was just a transitional 'walk' solution for the 'run' solution and that's Agent steering and execution."

## Conclusion
The terminal lock-up is **not** an essential Wu-Wei constraint. It was an artifact of a transitional architecture. The Operator's cognitive load is best managed through **Asynchronous Decoupling**:
- **Steering (Operator):** Remains completely unlocked in the main terminal, managing the DAG, rubbing intents, and reviewing PRs.
- **Execution (Agent):** Operates entirely asynchronously via `invoke_subagent` (`execute:` dialect) within an isolated worktree.

The cognitive tax of context-switching is mitigated not by forcing the Operator to wait sequentially, but by completely segregating the Execution environment from the Steering interface. The Operator can "dump" intent asynchronously without waiting for downstream execution to finish.

## Actions Taken
- The sequential lock-up was formally categorized as a structural bottleneck rather than a constraint.
- The `execute:` dialect has been introduced to resolve this, fulfilling the intent of this research probe.
