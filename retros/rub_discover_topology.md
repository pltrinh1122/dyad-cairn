# Reflect: Rubbing "Discover" (Phase vs Node-Type)

## Continue
We must continue rubbing our topological vocabulary. Conflating phases with node-types creates semantic blur, which inevitably leads to mechanical execution errors.

## Start
We must start explicitly defining "Discover" (Probe) and "Execute" (Payload) as physical **Node-Types** in the Frontier DAG, not just phases of a loop. 
- **Type: Probe (Discover):** A node strictly bound by the Probe Invariant. It investigates conditions and its *only* allowed output is mutating the DAG (spawning new execution nodes) or clipping architectural decisions. Functional logic mutation is physically forbidden.
- **Type: Execute (Payload):** A node bounded by the Red/Green PR Gate. Its *only* allowed output is a passing TDD spike. Emitting new DAG nodes is forbidden.

## Stop
We must stop using "Discover" as a loose synonym for the "Sense" phase of the SPAOR loop. Every node goes through SPAOR. But only a `Probe` node structurally yields the next layer of the DAG.
