# Design Proposal: HTIL Automation Guards

To safely disable the `design_review` gate, we must replace the human-in-the-loop (HTIL) operator verification with deterministic, mechanical grounding checks. 

## 1. Pre-requisite Grounding Guard
**Current state:** Operators manually check if a node's assumptions (the context) are valid.
**Automated Guard:** `skills/preflight_grounding.py`. 
When the `design_review` gate is bypassed, the `inject_node` or `authorize_node` scripts will physically invoke `preflight_grounding.py`. This script mandates that the node YAML explicitly defines an `assumptions` or `prerequisites` field. It will scan the substrate (files and ledger) to mechanically verify those assumptions exist. If they do not, the guard trips, halting the automation and falling back to Operator intervention.

## 2. Dependency Grounding Guard (Architectural Fit)
**Current state:** Operators review the node's proposed architectural footprint to ensure it integrates cleanly with the `commons/` and the local substrate without causing monolithic mass.
**Automated Guard:** An extension to `tests/test_topology_monitor.py` and `skills/dependency_guard.py`. 
Before authorization, a structural test is executed that verifies the node's intended scope does not violate the Asymmetric Guard invariants (e.g. no cross-contamination between `skills/` and `commons/`). If the node's scope is too broad or dependency tree is ungrounded, execution is mechanically stalled.

## Next Steps (Execution)
This node formally defines the required guards. The subsequent execution nodes will:
1. Implement `skills/preflight_grounding.py` and integrate it into `flow_state_manager.py`.
2. Expand `test_topology_monitor.py` to run predictive footprint analysis on newly injected nodes.
