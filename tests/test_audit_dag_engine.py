import os
import subprocess
import yaml
import pytest
import shutil

def test_audit_lock_blocks_frontier():
    """
    Validates that the Audit Lock mechanically freezes Frontier execution
    if the Audit DAG contains pending (non-DONE) nodes.
    """
    # Setup: Create a mock audit_state.yml with a pending node
    audit_path = "artifacts/audit_state.yml"
    backup_path = audit_path + ".bak"
    if os.path.exists(audit_path):
        shutil.copy(audit_path, backup_path)
    
    mock_audit = {
        "nodes": {
            "node_audit_test_1": {
                "status": "READY",
                "title": "Mock Audit Node",
                "goal": "Test the lock",
                "type": "audit"
            }
        }
    }
    
    # Ensure artifacts dir exists
    os.makedirs("artifacts", exist_ok=True)
    with open(audit_path, "w") as f:
        yaml.dump(mock_audit, f)
        
    try:
        # Action: Attempt to run a command on the Frontier DAG
        # We explicitly unset DYAD_DAG_STORE to ensure it defaults to Frontier
        env = os.environ.copy()
        if "DYAD_DAG_STORE" in env:
            del env["DYAD_DAG_STORE"]
            
        result = subprocess.run(
            ["python3", "skills/flow_state_manager.py", "plan", "node_14_probe_state_sync_collision"],
            capture_output=True,
            text=True,
            env=env
        )
        
        # Assert: It must fail and emit the governance guardrail
        assert result.returncode == 1, "Frontier orchestrator must fail when audit debt exists."
        assert "GOVERNANCE DEBT GUARDRAIL FIRED" in result.stdout, "Must emit the exact CSI Guard text."
        assert "The Audit DAG must be physically cleared" in result.stdout, "Must enforce the Alignment invariant."
        
    finally:
        # Teardown
        if os.path.exists(backup_path):
            shutil.move(backup_path, audit_path)
        elif os.path.exists(audit_path):
            os.remove(audit_path)

def test_audit_dag_execution_bypasses_lock():
    """
    Validates that executing the Audit DAG itself (via parameterized Data Store)
    is NOT blocked by its own Audit Lock.
    """
    # Setup
    audit_path = "artifacts/audit_state.yml"
    backup_path = audit_path + ".bak"
    if os.path.exists(audit_path):
        shutil.copy(audit_path, backup_path)
        
    mock_audit = {
        "nodes": {
            "node_audit_test_2": {
                "status": "READY",
                "title": "Mock Audit Node 2",
                "goal": "Test bypassing the lock",
                "type": "audit"
            }
        }
    }
    
    with open(audit_path, "w") as f:
        yaml.dump(mock_audit, f)
        
    try:
        # Action: Attempt to run a command explicitly ON the Audit DAG
        env = os.environ.copy()
        env["DYAD_DAG_STORE"] = audit_path
            
        result = subprocess.run(
            ["python3", "skills/flow_state_manager.py", "plan", "node_audit_test_2"],
            capture_output=True,
            text=True,
            env=env
        )
        
        # Assert: It must succeed, proving the dual-DAG parameterization
        assert result.returncode == 0, f"Audit DAG execution must not be blocked by its own lock. Stderr: {result.stderr}"
        assert "GOVERNANCE DEBT GUARDRAIL FIRED" not in result.stdout
        assert "Planning Node node_audit_test_2" in result.stdout
        
    finally:
        # Teardown
        if os.path.exists(backup_path):
            shutil.move(backup_path, audit_path)
        elif os.path.exists(audit_path):
            os.remove(audit_path)
