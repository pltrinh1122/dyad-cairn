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
    
    # Teardown
    if os.path.exists(TEST_DIR + "_bak"):
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)
        shutil.move(TEST_DIR + "_bak", TEST_DIR)
        
    if os.path.exists(audit_dir + "_bak"):
        if os.path.exists(audit_dir):
            shutil.rmtree(audit_dir)
        shutil.move(audit_dir + "_bak", audit_dir)

def test_node_inject_forces_in_review(clean_dag):
    cmd = ["bash", "./bin/node", "inject", "node_99_test", "Test Node", "Test Goal", "SUBSTRATE"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Inject failed: {result.stderr}"
    
    import sys
    sys.path.append('.')
    from skills.frontier_editor import load_state
    state = load_state()
        
    assert "node_99_test" in state["nodes"]
    assert state["nodes"]["node_99_test"]["status"] == "IN_REVIEW"
    assert state["nodes"]["node_99_test"]["title"] == "Test Node"
    assert state["nodes"]["node_99_test"]["goal"] == "Test Goal"

def test_node_authorize_requires_in_review(clean_dag):
    cmd = ["bash", "./bin/node", "authorize", "node_unknown"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode != 0
    assert "not found" in result.stdout or "not found" in result.stderr
    
    import sys
    sys.path.append('.')
    from skills.frontier_editor import load_state, save_state
    state = load_state()
    state["nodes"]["node_99_active"] = {"status": "ACTIVE", "type": "PLAN", "title": "test", "goal": "test", "scope": "SUBSTRATE"}
    save_state(state)
        
    cmd = ["bash", "./bin/node", "authorize", "node_99_active"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode != 0
    assert "must be IN_REVIEW" in result.stdout or "must be IN_REVIEW" in result.stderr
    
    state["nodes"]["node_99_review"] = {"status": "IN_REVIEW", "type": "PLAN", "title": "test", "goal": "test", "scope": "SUBSTRATE"}
    save_state(state)
        
    cmd = ["bash", "./bin/node", "authorize", "node_99_review"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    
    state = load_state()
    assert state["nodes"]["node_99_review"]["status"] == "AUTHORIZED"
