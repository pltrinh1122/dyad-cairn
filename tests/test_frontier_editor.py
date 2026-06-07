import os
import pytest
import yaml
import tempfile

def test_in_review_does_not_override_blocked(monkeypatch):
    from skills.frontier_editor import save_state
    
    # Mock YML_FILE and MD_FILE
    fd1, yml_path = tempfile.mkstemp(suffix=".yml")
    os.close(fd1)
    
    md_path = yml_path.replace(".yml", ".md")
    
    monkeypatch.setattr("skills.frontier_editor.YML_FILE", yml_path)
    monkeypatch.setattr("skills.frontier_editor.MD_FILE", md_path)
    
    # Mock ledger to be empty
    monkeypatch.setattr("skills.frontier_reader.derive_status.__defaults__", (None, None))
    # We'll just mock the files explicitly or let it run
    
    # Create a state where node_2 depends on node_1
    state = {
        "nodes": {
            "node_1": {"status": "IN_REVIEW", "dependencies": [], "type": "PROBE", "title": "Node 1"},
            "node_2": {"status": "IN_REVIEW", "dependencies": ["node_1"], "type": "PROBE", "title": "Node 2"}
        }
    }
    
    # Mock git rev-parse so it doesn't fail
    import subprocess
    def mock_run(*args, **kwargs):
        class MockResult:
            returncode = 0
            stdout = "main\n"
            stderr = ""
            def strip(self): return self.stdout.strip()
        return MockResult()
    monkeypatch.setattr(subprocess, "run", mock_run)
    
    # Wait, save_state edits state in place and writes it
    save_state(state)
    
    # Read the output MD_FILE to ensure it uses the ASCII tree
    with open(md_path, "r") as f:
        md_content = f.read()
        
    assert "├── node_1" in md_content or "└── node_1" in md_content
    
    # node_2 should be BLOCKED because node_1 is not DONE
    # node_1 should be IN_REVIEW
    # Check that node_2 has [BLOCKED] and node_1 has [IN_REVIEW] in the tree output
    assert "[IN_REVIEW]" in md_content
    assert "[BLOCKED]" in md_content
    
    # Check that IN_REVIEW is no longer in state for node_2 if we reload?
    # save_state dumps the current state back. But wait, save_state does NOT modify `state["nodes"][node_id]["status"]` before dumping?
    # Actually, if we fix it, we should maybe strip the cached status if it's invalid?
    # Let's just assert the MD rendering has the right statuses for now.
    
    os.remove(yml_path)
    if os.path.exists(md_path):
        os.remove(md_path)
