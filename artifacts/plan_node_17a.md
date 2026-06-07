# Plan: Audit DAG Architecture Implementation

## Physical Invariant
The SPAOR execution engine (`flow_state_manager.py` and `frontier_editor.py`) must be mathematically agnostic to the DAG it operates on. The Dual-DAG architecture is achieved by parameterizing the Data Store via an environment variable (`DYAD_DAG_STORE`), defaulting to `artifacts/frontier_state.yml`. 

The "Audit Lock" is a conditional trap injected into `flow_state_manager.py` that asserts: "If the mounted Data Store is the Frontier DAG, mechanically halt all execution if `artifacts/audit_state.yml` exists and contains non-DONE nodes."

## Execution Spec (node_17b_execute_audit_dag)

### 1. Engine Parameterization
**Target:** `skills/frontier_editor.py` and `skills/flow_state_manager.py`
- Modify the hardcoded `YML_FILE = "artifacts/frontier_state.yml"` to check `os.environ.get("DYAD_DAG_STORE", "artifacts/frontier_state.yml")`.
- Update `MD_FILE` computation to derive from the `YML_FILE` base name (e.g., `artifacts/audit_state.md`).

### 2. The Audit Lock (Governance Guardrail)
**Target:** `skills/flow_state_manager.py`
- Introduce `check_audit_lock()`.
- Condition: `if os.environ.get("DYAD_DAG_STORE", "artifacts/frontier_state.yml") == "artifacts/frontier_state.yml":`
- Logic: Check if `artifacts/audit_state.yml` exists. If so, parse it. If any node has a status other than `DONE` (meaning `ACTIVE`, `IN_REVIEW`, `READY`, `BLOCKED`), log a severe Governance Guardrail violation and `sys.exit(1)`.

### 3. The CLI Router (`bin/audit`)
**Target:** `bin/audit`
- Create a bash wrapper `bin/audit`.
- It sets `DYAD_DAG_STORE="artifacts/audit_state.yml"`.
- It forwards arguments to `skills/flow_state_manager.py`.
- If invoked without arguments, it defaults to executing a script to spawn an audit node, or simply wraps `./bin/node`. 
- Actually, a generic `bin/audit-node` that perfectly mirrors `bin/node` but prefixes with `DYAD_DAG_STORE=artifacts/audit_state.yml` is required. Then `bin/audit` can be a helper that specifically injects a new probe node into the audit DAG.

### 4. Tests
**Target:** `tests/test_audit_dag_engine.py`
- **Red Phase TDD:**
  - Mock `artifacts/audit_state.yml` with a `READY` node.
  - Assert that calling `flow_state_manager.py` (default Frontier) throws `sys.exit(1)` and outputs "Governance Guardrail".
  - Assert that calling `flow_state_manager.py` with `DYAD_DAG_STORE=artifacts/audit_state.yml` executes successfully without tripping the lock.
