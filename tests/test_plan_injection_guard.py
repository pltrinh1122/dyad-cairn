import os
import subprocess
import yaml
import pytest
import shutil

TEST_DIR = "artifacts/frontier"

@pytest.fixture
def clean_dag(monkeypatch):
    monkeypatch.delenv("DYAD_DAG_STORE", raising=False)
    # Setup
    os.makedirs("artifacts", exist_ok=True)
    if os.path.exists(TEST_DIR):
        shutil.copytree(TEST_DIR, TEST_DIR + "_bak", dirs_exist_ok=True)
        shutil.rmtree(TEST_DIR)
        
    audit_dir = "artifacts/audit"
    if os.path.exists(audit_dir):
        shutil.move(audit_dir, audit_dir + "_bak")
    
    os.makedirs(TEST_DIR, exist_ok=True)
        
    yield
    
    if os.path.exists(TEST_DIR + "_bak"):
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)
        shutil.move(TEST_DIR + "_bak", TEST_DIR)
        
    if os.path.exists(audit_dir + "_bak"):
        if os.path.exists(audit_dir):
            shutil.rmtree(audit_dir)
        shutil.move(audit_dir + "_bak", audit_dir)

def test_plan_injection_guard_fails_when_hallucinated(clean_dag, monkeypatch):
    import sys
    sys.path.append('.')
    from skills.frontier_editor import load_state, save_state
    
    state = load_state()
    state["nodes"]["node_99_plan_test"] = {
        "status": "READY",
        "title": "Hallucinated Plan",
        "goal": "Test Guard",
        "type": "PLAN"
    }
    
    with pytest.raises(SystemExit) as excinfo:
        save_state(state)
    
    assert excinfo.value.code == 1

def test_plan_injection_guard_passes_when_on_probe_branch(clean_dag, monkeypatch):
    import sys
    sys.path.append('.')
    from skills.frontier_editor import load_state, save_state
    
    def mock_run(cmd, *args, **kwargs):
        class MockResult:
            returncode = 0
            stdout = "active/node_99_probe_test\n"
            stderr = ""
            def strip(self): return self.stdout.strip()
        if isinstance(cmd, list) and cmd[0].endswith("git") and cmd[1] == "rev-parse":
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
    
    save_state(state)
    
    saved = load_state()
    assert "node_99_plan_test" in saved["nodes"]
