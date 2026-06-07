# Retro: Trail Completion Invariants and the [REFLECT] Phase

## Continue
We must continue distinguishing between local node execution and global trail completion. The Operator correctly probed the boundary of the `[EXECUTE]` CSI Guard.

## Start
We must explicitly codify the `[REFLECT]` phase. Execute CSI guards (like `./bin/node complete`) are structurally insufficient for closing a trail. They only enforce the mechanical test invariants for a single leaf node. A trail represents a complete conversational and architectural arc, which requires its own universal invariants:
1. **The Reflect Synthesis Invariant**: The friction, pitfalls, and architectural drifts discovered during the execution of the trail must be physically condensed (Retro) and locked to the Ledger. This ensures the next trail inherits the wisdom, not just the code.
2. **The Issue Closure Invariant**: The GitHub issue bound to the active trail must be explicitly closed to clear the Meta-Orchestrator's backlog queue.
3. **The Trail Pruning Invariant**: The entire parent trail structure must be computationally pruned from the Frontier DAG.

We must introduce an explicit `[REFLECT]` node-type (or formalize the `./bin/node reflect` CSI Phase) that executes these three invariants before a trail can truly be considered finished.

## Stop
We must stop assuming a trail ends when the code merges. Code merge is the end of the `[EXECUTE]` phase, not the end of the SPAO loop.
