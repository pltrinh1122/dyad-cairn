# HOW-0004: Subagent Execution Dialect

## The Core Concept
The Dyad Practice leverages an asynchronous execution model to prevent locking up the main orchestration terminal.

## The `execute:` Dialect
When the Operator issues the conversational moniker `execute: <node_id>` in the main terminal, the Agent (Architect) must recognize this and trigger the `invoke_subagent` tool. 

### Subagent Parameters:
- **TypeName**: `self` (or another appropriate worker)
- **Workspace**: `share` (this maps to an isolated git worktree sharing the same underlying repository, ensuring no state collisions with the main thread).
- **Prompt**: "Checkout the branch `active/<node_id>`. Implement the required code, execute TDD (running `python3 skills/testing_harness.py`), and upon success, invoke the flow state manager to transition the node to completed (`./bin/node complete <node_id>`)."

By dispatching a subagent via the `execute:` dialect, the Architect cements its autonomy over execution while keeping the main terminal unlocked. As such, the UI-level `/goal` command is strictly retired and forbidden. This approach ensures the Architect remains completely free to engage with the Operator, handle design reviews, parse `todo:` statements, or plan the next `PROBE` node without being bottlenecked.

## Hand-off & Completion
1. The Architect uses `invoke_subagent`.
2. The subagent operates in the background, working within a branched or shared worktree.
3. Once the subagent finishes and issues the `node complete` or reflection logic, it sends a message back to the Architect.
4. The Architect alerts the Operator that the subagent has finished the execution node.
