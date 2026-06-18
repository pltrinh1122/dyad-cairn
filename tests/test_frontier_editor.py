import os
import pytest
import yaml
import tempfile

def test_in_review_does_not_override_blocked(monkeypatch):
    from skills.frontier_editor import save_state
    
    # Mock YML_DIR and MD_FILE
    import shutil
    yml_path = tempfile.mkdtemp()
    
    md_path = yml_path + "_md.md"
    
    monkeypatch.setattr("skills.frontier_editor.YML_DIR", yml_path)
    monkeypatch.setattr("skills.frontier_editor.MD_FILE", md_path)
    
    # Mock ledger to be empty
    monkeypatch.setattr("skills.frontier_reader.derive_status.__defaults__", (None, None))
    # We'll just mock the files explicitly or let it run
    
    # Create a state where node_2 depends on node_1
    state = {
        "nodes": {
            "node_fake_991": {"status": "IN_REVIEW", "dependencies": [], "type": "PROBE", "title": "Node 1"},
            "node_fake_992": {"status": "IN_REVIEW", "dependencies": ["node_fake_991"], "type": "PROBE", "title": "Node 2"}
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
        
    assert "├── node_fake_991" in md_content or "└── node_fake_991" in md_content
    
    # node_2 should be BLOCKED because node_1 is not DONE
    # node_1 should be IN_REVIEW
    # Check that node_2 has [BLOCKED] and node_1 has [IN_REVIEW] in the tree output
    assert "[IN_REVIEW]" in md_content
    assert "[BLOCKED]" in md_content
    
    # Check that IN_REVIEW is no longer in state for node_2 if we reload?
    # save_state dumps the current state back. But wait, save_state does NOT modify `state["nodes"][node_id]["status"]` before dumping?
    # Actually, if we fix it, we should maybe strip the cached status if it's invalid?
    # Let's just assert the MD rendering has the right statuses for now.
    
    shutil.rmtree(yml_path)
    if os.path.exists(md_path):
        os.remove(md_path)

def test_archive_done_nodes(monkeypatch):
    from skills.frontier_editor import save_state
    import shutil
    import os
    yml_path = tempfile.mkdtemp()
    md_path = yml_path + "_md.md"
    
    monkeypatch.setattr("skills.frontier_editor.YML_DIR", yml_path)
    monkeypatch.setattr("skills.frontier_editor.MD_FILE", md_path)
    
    # Mock derive_status to return DONE
    def mock_derive(*args, **kwargs):
        return "DONE"
    monkeypatch.setattr("skills.frontier_reader.derive_status", mock_derive)
    
    node_file = os.path.join(yml_path, "node_fake_123.yml")
    with open(node_file, "w") as f:
        yaml.dump({"node_fake_123": {"status": "DONE", "type": "PROBE", "title": "Node 1"}}, f)
        
    state = {
        "nodes": {
            "node_fake_123": {"status": "DONE", "dependencies": [], "type": "PROBE", "title": "Node 1"}
        }
    }
    
    import subprocess
    def mock_run(*args, **kwargs):
        class MockResult:
            returncode = 0
            stdout = "main\n"
            stderr = ""
        return MockResult()
    monkeypatch.setattr(subprocess, "run", mock_run)
    
    save_state(state)
    
    archive_dir = os.path.join("artifacts", "archive", os.path.basename(yml_path))
    archived_file = os.path.join(archive_dir, "node_fake_123.yml")
    
    assert not os.path.exists(node_file)
    assert os.path.exists(archived_file)
    
    # Clean up
    shutil.rmtree(yml_path)
    if os.path.exists(md_path):
        os.remove(md_path)
    if os.path.exists(archive_dir):
        shutil.rmtree(archive_dir)
