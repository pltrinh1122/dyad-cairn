# Reflect: Structural Mutex Falsification

## Continue
- Engaging in deep architectural `riff:`s to falsify invariants before they become deeply entrenched. Your pushback on the Structural Mutex saved us from building a rigid, single-threaded lock system.
- Enforcing strict mechanical boundaries: using the orchestration CLI tools (`./bin/node`) and verifying testing invariants to properly transition the DAG.

## Start
- Implementing the DAG decomposition (`node_22`). The `frontier_state.yml` currently serves as a monolithic chokepoint. Breaking it into individual node definitions will physically enable the parallel execution the Dyad needs.
- Applying Event Sourcing models to the Ledgers, allowing true asynchronous appending without fear of corrupting the Timeline Truth.

## Stop
- Treating all structural conflicts as merge errors that require heavy locking. As you pointed out, many data types (like chronological ledgers) are natively merge-friendly.
- Letting the Agent auto-wire dependencies incorrectly during fractal decomposition. We must mechanically ensure `PROBE`s spawn as independent trailheads rather than creating waterfall blockers off unexecuted `PLAN` nodes.
