import os
import subprocess
import yaml
import shutil

def test_rub_multiple_fields():
    todo_dir = "artifacts/todos"
    todo_bak = "artifacts/todos_bak"
    if os.path.exists(todo_dir):
        shutil.copytree(todo_dir, todo_bak, dirs_exist_ok=True)
        shutil.rmtree(todo_dir)
    os.makedirs(todo_dir, exist_ok=True)
    
    frontier_dir = "artifacts/frontier"
    frontier_bak = "artifacts/frontier_bak"
    if os.path.exists(frontier_dir):
        shutil.copytree(frontier_dir, frontier_bak, dirs_exist_ok=True)
        shutil.rmtree(frontier_dir)
    os.makedirs(frontier_dir, exist_ok=True)

    try:
        todo_id = "todo_99999"
        todo_content = {
            todo_id: {
                "raw_thought": "Test multiple fields",
                "status": "UNRUBBED",
                "rub_matrix": {"what": None, "why": None, "scope": None}
            }
        }
        with open(os.path.join(todo_dir, f"{todo_id}.yml"), "w") as f:
            yaml.dump(todo_content, f)

        # Execute rub with multiple fields
        result = subprocess.run(["./bin/rub", todo_id, "--what", "test what", "--why", "test why", "--scope", "SUBSTRATE"], capture_output=True, text=True)
        assert result.returncode == 0, f"rub failed: {result.stderr}\nSTDOUT: {result.stdout}"

        # Should only emit one log when complete
        stdout_lines = [l for l in result.stdout.split('\n') if l.strip()]
        # We don't want to see 3 separate "[RUB] Successfully updated" logs
        updates_log_count = sum(1 for line in stdout_lines if "[RUB] Successfully updated" in line)
        assert updates_log_count <= 1, "Should emit at most one final state log for multiple updates"
        
        assert not os.path.exists(os.path.join(todo_dir, f"{todo_id}.yml")), "Todo file was not deleted"
        
        node_id = "node_todo_99999"
        node_file = os.path.join(frontier_dir, f"{node_id}.yml")
        assert os.path.exists(node_file), "Node file was not created"
        
        with open(node_file, "r") as f:
            node_data = yaml.safe_load(f)
            assert node_data[node_id]["status"] == "AUTHORIZED"
            assert "WHAT: test what" in node_data[node_id]["goal"]

    finally:
        if os.path.exists(todo_bak):
            if os.path.exists(todo_dir):
                shutil.rmtree(todo_dir)
            shutil.move(todo_bak, todo_dir)
        if os.path.exists(frontier_bak):
            if os.path.exists(frontier_dir):
                shutil.rmtree(frontier_dir)
            shutil.move(frontier_bak, frontier_dir)

def test_rub_commission_semantic_csi_guard():
    commission_dir = "artifacts/commissions"
    commission_bak = "artifacts/commissions_bak"
    if os.path.exists(commission_dir):
        shutil.copytree(commission_dir, commission_bak, dirs_exist_ok=True)
        shutil.rmtree(commission_dir)
    os.makedirs(commission_dir, exist_ok=True)
    
    try:
        target_id = "commission_99999"
        
        # Execute rub with --type commission
        result = subprocess.run([
            "./bin/rub", target_id, "--type", "commission", 
            "--what", "test what", "--why", "test why", "--scope", "INTEGRITY"
        ], capture_output=True, text=True)
        
        assert result.returncode == 0, f"rub failed: {result.stderr}\nSTDOUT: {result.stdout}"
        
        # Verify the CSI Guard is emitted
        stdout = result.stdout
        assert "INTENT VERIFICATION" in stdout
        assert "kb/commission_protocol_commissionee.md" in stdout
        assert "SEMANTIC evaluation" in stdout
        assert "pressure-test the 'WHY'" in stdout
        
    finally:
        if os.path.exists(commission_bak):
            if os.path.exists(commission_dir):
                shutil.rmtree(commission_dir)
            shutil.move(commission_bak, commission_dir)
