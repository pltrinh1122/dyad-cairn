import os
import subprocess
import yaml

def test_todo_cli_execution():
    todo_path = "artifacts/todos.yml"
    original_content = ""
    if os.path.exists(todo_path):
        with open(todo_path, "r") as f:
            original_content = f.read()
            
    intent = "test_noisy_intent_12345"
    
    if "DYAD_DAG_STORE" in os.environ:
        del os.environ["DYAD_DAG_STORE"]
        
    audit_path = "artifacts/audit_state.yml"
    audit_bak = audit_path + ".testbak"
    if os.path.exists(audit_path):
        import shutil
        shutil.move(audit_path, audit_bak)
        
    try:
        result = subprocess.run(["./bin/todo", intent], capture_output=True, text=True)
        assert result.returncode == 0, f"todo CLI failed: {result.stderr}"
        
        assert os.path.exists(todo_path)
        with open(todo_path, "r") as f:
            content = f.read()
        
        assert intent in content, "Intent was not written to todos.yml"
        
        # Extract the todo_id
        todo_id = None
        todos = yaml.safe_load(content)
        for tid, tdata in todos["backlog"].items():
            if tdata["intent"] == intent:
                todo_id = tid
                break
        
        assert todo_id is not None
        
        # Verify it appended to the ledger
        with open("dyad-state/ledger.jsonl", "r") as f:
            ledger_content = f.read()
            assert intent in ledger_content, "Intent was not logged to the ledger!"
            
        # Test converting the todo
        # The node_id will be node_todo_...
        # We need to make sure we don't accidentally pollute the DAG if test fails, so we'll just check if it parses, but wait, convert-todo mutates frontier_state.yml!
        # It's better to just ensure convert-todo successfully parses and runs without error, then we prune it from frontier_state.
        
        # Restore frontier_state.yml later
        frontier_path = "artifacts/frontier_state.yml"
        frontier_original = ""
        if os.path.exists(frontier_path):
            with open(frontier_path, "r") as f:
                frontier_original = f.read()
                
        try:
            conv_res = subprocess.run(["./bin/node", "convert-todo", todo_id], capture_output=True, text=True)
            assert conv_res.returncode == 0, f"convert-todo failed: {conv_res.stderr}"
            
            with open(todo_path, "r") as f:
                new_todos = yaml.safe_load(f)
            assert todo_id not in new_todos.get("backlog", {})
        finally:
            if frontier_original:
                with open(frontier_path, "w") as f:
                    f.write(frontier_original)
        
    finally:
        # Restore original state
        if original_content:
            with open(todo_path, "w") as f:
                f.write(original_content)
        else:
            if os.path.exists(todo_path):
                os.remove(todo_path)
                
        # We also created a markdown file
        if os.path.exists("artifacts/todos.md"):
            os.remove("artifacts/todos.md")
            
        if os.path.exists(audit_bak):
            import shutil
            shutil.move(audit_bak, audit_path)
