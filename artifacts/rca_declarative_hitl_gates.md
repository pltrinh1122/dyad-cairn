# Root Cause Analysis: Declarative HITL Gates

## 1. Problem Statement
The Dyad's routing engine (`skills/flow_state_manager.py`) relied on a "magic string" environment check (`"audit" in DYAD_DAG_STORE`) to determine if a node should bypass the Design-Review gate (`IN_REVIEW`). This approach was fundamentally brittle: it obfuscated the structural intent of the DAG by abstracting it into an environment variable rather than encoding it directly in the data model.

## 2. Root Cause
The `inject_node` function lacked a formal configuration schema to determine node routing. Instead of reading explicit rules from the DAG being mutated, it guessed the rules based on the filename of the DAG substrate. This meant the DAG itself was completely ignorant of its own operating parameters, violating the principle of self-documenting architectures.

## 3. The Conceptual Drift
When intent (e.g., whether a workflow requires human-in-the-loop validation) is decoupled from the data structure that executes the workflow (the DAG YAML), we invite configuration drift. The YAML file should be the single source of truth not only for the execution graph (the nodes) but also for the *physics* of how the graph operates (the gates).

## 4. Resolution & Structural Invariants
1. **Declarative State Migration**: We injected an explicit `config.gates` block at the root of both `artifacts/frontier_state.yml` and `artifacts/audit_state.yml`.
   - The Frontier DAG now overtly declares: `design_review: true`, `reflection_review: true`.
   - The Audit DAG explicitly declares: `design_review: false`, `reflection_review: true`.
2. **Context-Aware Routing**: `inject_node` was refactored to consume the `state.get("config").get("gates").get("design_review")` parameter directly from the loaded YAML state, executing the precise intent defined by the data structure itself.
3. **Magic String Elimination**: The fragile `DYAD_DAG_STORE` string check has been entirely excised from the HITL boundary logic.

## 5. Prevention
We implemented `test_audit_dag_injection_bypasses_in_review` and `test_frontier_dag_injection_sets_in_review` which strictly mock the DAG configuration payload, ensuring the `flow_state_manager` reliably respects the data-driven invariants. Any attempt to regress to hardcoded logic will mechanically fail the test suite.
