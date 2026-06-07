# Execution Plan: Declarative HITL Gates

## 1. Intent
Migrate the `IN_REVIEW` Design-Review gate logic from a brittle magic-string environment check (`"audit" in DYAD_DAG_STORE`) to a declarative `config.gates` block embedded natively within the YAML state files. 

## 2. Structural Invariants
- `artifacts/frontier_state.yml` will embed:
  ```yaml
  config:
    gates:
      design_review: true
      execution_review: false
      reflection_review: true
  ```
- `artifacts/audit_state.yml` will embed:
  ```yaml
  config:
    gates:
      design_review: false
      execution_review: false
      reflection_review: true
  ```
- `skills/flow_state_manager.py::inject_node` will read `state.get("config", {}).get("gates", {}).get("design_review", True)`. If true, the node halts at `IN_REVIEW`.

## 3. Red Phase Tests
- Update `tests/test_audit_injection.py` to assert that `inject_node` checks the `config.gates.design_review` state rather than the environment variable.
- Remove `monkeypatch.setenv` from the logic evaluation tests, instead mocking `load_state` to return the `config` payload.
