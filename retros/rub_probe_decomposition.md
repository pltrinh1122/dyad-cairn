# Retro: Mechanical Lifecycle of a Probe

## Continue
We must continue physicalizing abstract phases into concrete, deterministic state-machine transitions. 

## Start
We must start enforcing the exact mechanical lifecycle of a `[PROBE]` node:
1. **Identify:** The Probe investigates to find root physical invariants.
2. **Decompose (Fractal Expansion):** If multiple invariants are discovered, the Probe cannot proceed. It must spawn a sibling `[PROBE]` node for each invariant and transition itself to `DONE`.
3. **Transition to Plan:** If the Probe discovers exactly ONE invariant (atomic), its final act is to populate a `[PLAN]` node onto the DAG and transition itself to `DONE`.

## Stop
We must stop allowing a single Probe to output multiple execution trails directly. We must stop allowing Probes to skip the `[PLAN]` phase. A Probe discovers the *Why*; it spawns a `[PLAN]` to design the *How*.
