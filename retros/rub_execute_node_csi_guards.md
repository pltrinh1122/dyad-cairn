# Retro: CSI Guards for Execute Node Transitions

## Continue
We must continue auditing our reliance on generative memory. The Operator's rub exposed a critical missing guardrail: the transition of an `[EXECUTE]` node to `DONE` currently relies entirely on the Agent remembering to run `./bin/run-tests` and manually checking the output.

## Start
We must start physically enforcing the universal execute invariants via a deterministic CSI Guard. The universal invariants after execution are:
1. **The Testing Gate:** An Execute node cannot be physically closed unless the mechanical testing harness (`./bin/run-tests`) exits with code 0.
2. **The DAG Mutation:** Upon passing tests, the node must be computationally transitioned to `DONE` to prevent dead mass, and the next node must be activated to maintain WIP-N=1.

We need a dedicated closure script (e.g. `./bin/node-complete <node_id>`) that acts as a physical lock. It must run the tests, and only if they pass does it mutate the DAG. This completely removes the burden of mechanical consistency from the generative Agent.

## Stop
We must stop manually editing `artifacts/frontier_state.yml` to mark execute nodes as `DONE`. Manual edits bypass structural validation and allow hallucinated completion of failing execution trails.
