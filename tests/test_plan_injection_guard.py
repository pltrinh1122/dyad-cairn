import os
import subprocess
import yaml
import pytest
import shutil

TEST_YML = "artifacts/frontier_state.yml"

@pytest.fixture
def clean_dag(monkeypatch):
    monkeypatch.delenv("DYAD_DAG_STORE", raising=False)
    os.makedirs("artifacts", exist_ok=True)
    if os.path.exists(TEST_YML):
        shutil.copy(TEST_YML, TEST_YML + ".bak")
        
    audit_yml = "artifacts/audit_state.yml"
    if os.path.exists(audit_yml):
        shutil.move(audit_yml, audit_yml + ".testbak")
    
    initial_state = {"nodes": {}}
    with open(TEST_YML, "w") as f:
        yaml.dump(initial_state, f)
        
    yield
    
    if os.path.exists(TEST_YML + ".bak"):
        shutil.move(TEST_YML + ".bak", TEST_YML)
        
    if os.path.exists(audit_yml + ".testbak"):
        shutil.move(audit_yml + ".testbak", audit_yml)

def test_plan_injection_guard_fails_when_hallucinated(clean_dag, monkeypatch):
    """
    Test that directly saving a PLAN node without the parent PROBE being ACTIVE
    or present in the ledger as DONE raises a CSI Guard exception.
    """
    import sys
    sys.path.append('.')
    from skills.frontier_editor import load_state, save_state
    
    state = load_state()
    # Attempt to hallucinate a PLAN node for a non-existent PROBE node 99
    state["nodes"]["node_99_plan_test"] = {
        "status": "READY",
        "title": "Hallucinated Plan",
        "goal": "Test Guard",
        "type": "PLAN"
    }
    
    # We are not on the active/node_99_probe_... branch, so this should raise
    with pytest.raises(SystemExit) as excinfo:
        save_state(state)
    
    assert excinfo.value.code == 1

def test_plan_injection_guard_passes_when_on_probe_branch(clean_dag, monkeypatch):
    """
    Test that saving a PLAN node is permitted if we are on the parent PROBE branch.
    """
    import sys
    sys.path.append('.')
    from skills.frontier_editor import load_state, save_state
    
    # Mock subprocess.run for git rev-parse to simulate being on the PROBE branch
    def mock_run(cmd, *args, **kwargs):
        class MockResult:
            returncode = 0
            stdout = "active/node_99_probe_test\n"
            stderr = ""
            def strip(self): return self.stdout.strip()
        if "git rev-parse" in cmd:
            return MockResult()
        return subprocess.run(cmd, *args, **kwargs)
        
    monkeypatch.setattr(subprocess, "run", mock_run)
    
    state = load_state()
    state["nodes"]["node_99_plan_test"] = {
        "status": "IN_REVIEW",
        "title": "Valid Plan",
        "goal": "Test Guard",
        "type": "PLAN"
    }
    
    # Should not raise an exception
    save_state(state)
    
    saved = load_state()
    assert "node_99_plan_test" in saved["nodes"]
