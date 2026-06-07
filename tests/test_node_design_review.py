import os
import subprocess
import yaml
import pytest
import shutil

TEST_YML = "artifacts/frontier_state.yml"

@pytest.fixture
def clean_dag(monkeypatch):
    monkeypatch.delenv("DYAD_DAG_STORE", raising=False)
    # Setup
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
    
    # Teardown
    if os.path.exists(TEST_YML + ".bak"):
        shutil.move(TEST_YML + ".bak", TEST_YML)
        
    if os.path.exists(audit_yml + ".testbak"):
        shutil.move(audit_yml + ".testbak", audit_yml)

def test_node_inject_forces_in_review(clean_dag):
    """
    Test that 'bin/node inject' physically defaults a new node to IN_REVIEW.
    It should not be possible to inject a node directly to READY.
    """
    cmd = ["bash", "./bin/node", "inject", "node_99_test", "Test Node", "Test Goal"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Inject failed: {result.stderr}"
    
    with open(TEST_YML, "r") as f:
        state = yaml.safe_load(f)
        
    assert "node_99_test" in state["nodes"]
    assert state["nodes"]["node_99_test"]["status"] == "IN_REVIEW"
    assert state["nodes"]["node_99_test"]["title"] == "Test Node"
    assert state["nodes"]["node_99_test"]["goal"] == "Test Goal"

def test_node_authorize_requires_in_review(clean_dag):
    """
    Test that 'bin/node authorize' fails if the node is not IN_REVIEW,
    and succeeds in transitioning to READY if it is IN_REVIEW.
    """
    # 1. Authorize an unknown node
    cmd = ["bash", "./bin/node", "authorize", "node_unknown"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode != 0
    assert "not found" in result.stdout or "not found" in result.stderr
    
    # 2. Authorize a node that is ACTIVE
    with open(TEST_YML, "r") as f:
        state = yaml.safe_load(f)
    state["nodes"]["node_99_active"] = {"status": "ACTIVE"}
    with open(TEST_YML, "w") as f:
        yaml.dump(state, f)
        
    cmd = ["bash", "./bin/node", "authorize", "node_99_active"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode != 0
    assert "must be IN_REVIEW" in result.stdout or "must be IN_REVIEW" in result.stderr
    
    # 3. Authorize an IN_REVIEW node successfully
    state["nodes"]["node_99_review"] = {"status": "IN_REVIEW"}
    with open(TEST_YML, "w") as f:
        yaml.dump(state, f)
        
    cmd = ["bash", "./bin/node", "authorize", "node_99_review"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    
    with open(TEST_YML, "r") as f:
        state = yaml.safe_load(f)
    assert state["nodes"]["node_99_review"]["status"] == "READY"
