import os
import subprocess
import yaml
import shutil

def test_unrub_cli_execution():
    todo_dir = "artifacts/todos"
    todo_bak = "artifacts/todos_bak"
    if os.path.exists(todo_dir):
        shutil.copytree(todo_dir, todo_bak, dirs_exist_ok=True)
        shutil.rmtree(todo_dir)
    os.makedirs(todo_dir, exist_ok=True)
            
    if "DYAD_DAG_STORE" in os.environ:
        del os.environ["DYAD_DAG_STORE"]
        
    audit_dir = "artifacts/audit"
    audit_bak = "artifacts/audit_bak"
    if os.path.exists(audit_dir):
        shutil.move(audit_dir, audit_bak)
        
    frontier_dir = "artifacts/frontier"
    frontier_bak = "artifacts/frontier_bak"
    if os.path.exists(frontier_dir):
        shutil.copytree(frontier_dir, frontier_bak, dirs_exist_ok=True)
        shutil.rmtree(frontier_dir)
    os.makedirs(frontier_dir, exist_ok=True)
        
    try:
        # Create a dummy node in frontier
        node_id = "node_todo_12345"
        todo_id = "todo_12345"
        
        dummy_node = {
            node_id: {
                "title": "Convert Todo: todo_12345",
                "goal": "test raw thought\n\nWHAT: test what\nWHY: test why",
                "type": "PLAN",
                "scope": "FRONTIER",
                "status": "AUTHORIZED"
            }
        }
        
        with open(os.path.join(frontier_dir, f"{node_id}.yml"), "w") as f:
            yaml.dump(dummy_node, f, default_flow_style=False, sort_keys=False)
            
        result = subprocess.run(["./bin/unrub", node_id], capture_output=True, text=True)
        assert result.returncode == 0, f"unrub CLI failed: {result.stderr}\n{result.stdout}"
        
        assert not os.path.exists(os.path.join(frontier_dir, f"{node_id}.yml")), "Node file was not deleted"
        
        todo_file = os.path.join(todo_dir, f"{todo_id}.yml")
        assert os.path.exists(todo_file), "Todo file was not created"
        
        with open(todo_file, "r") as f:
            todo_data = yaml.safe_load(f)
            
        assert todo_id in todo_data, "todo_id not in todo data"
        todo = todo_data[todo_id]
        
        assert todo["status"] == "UNRUBBED"
        assert todo["raw_thought"] == "test raw thought"
        assert todo["rub_matrix"]["what"] is None
        assert todo["rub_matrix"]["why"] is None
        assert todo["rub_matrix"]["scope"] == "FRONTIER"
        
    finally:
        if os.path.exists(todo_bak):
            if os.path.exists(todo_dir):
                shutil.rmtree(todo_dir)
            shutil.move(todo_bak, todo_dir)
            
        if os.path.exists(frontier_bak):
            if os.path.exists(frontier_dir):
                shutil.rmtree(frontier_dir)
            shutil.move(frontier_bak, frontier_dir)
            
        if os.path.exists(audit_bak):
            shutil.move(audit_bak, audit_dir)
