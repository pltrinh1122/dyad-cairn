import os
import subprocess
import yaml
import shutil

def test_todo_cli_execution():
    todo_dir = "artifacts/todos"
    todo_bak = "artifacts/todos_bak"
    if os.path.exists(todo_dir):
        shutil.copytree(todo_dir, todo_bak, dirs_exist_ok=True)
        shutil.rmtree(todo_dir)
    os.makedirs(todo_dir, exist_ok=True)
            
    intent = "test_noisy_intent_12345"
    
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
        result = subprocess.run(["./bin/todo", intent], capture_output=True, text=True)
        assert result.returncode == 0, f"todo CLI failed: {result.stderr}"
        
        found = False
        todo_id = None
        for fname in os.listdir(todo_dir):
            if fname.endswith(".yml"):
                with open(os.path.join(todo_dir, fname), "r") as f:
                    content = f.read()
                    if intent in content:
                        found = True
                        data = yaml.safe_load(content)
                        todo_id = list(data.keys())[0]
                        break
        assert found, "Intent was not written to todos dir"
        assert todo_id is not None
        
        # Verify it appended to the ledger
        with open("dyad-state/ledger.jsonl", "r") as f:
            ledger_content = f.read()
            assert intent in ledger_content, "Intent was not logged to the ledger!"
            
        try:
            subprocess.run(["./bin/rub", todo_id, "what", "test"])
            subprocess.run(["./bin/rub", todo_id, "why", "test"])
            
            conv_fail = subprocess.run(["./bin/node", "convert-todo", todo_id], capture_output=True, text=True)
            assert conv_fail.returncode != 0, "Intent Gate failed to block conversion with missing scope"
            assert "fully populated" in conv_fail.stdout
            
            subprocess.run(["./bin/rub", todo_id, "scope", "INVALID_SCOPE"])
            conv_fail2 = subprocess.run(["./bin/node", "convert-todo", todo_id], capture_output=True, text=True)
            assert conv_fail2.returncode != 0, "Intent Gate failed to block conversion with invalid scope"
            assert "FRONTIER, INTEGRITY, SUBSTRATE" in conv_fail2.stdout
            
            subprocess.run(["./bin/rub", todo_id, "scope", "SUBSTRATE"])
            conv_res = subprocess.run(["./bin/node", "convert-todo", todo_id], capture_output=True, text=True)
            assert conv_res.returncode == 0, f"convert-todo failed: {conv_res.stderr}"
            
            assert not os.path.exists(os.path.join(todo_dir, f"{todo_id}.yml"))
        finally:
            pass
        
    finally:
        if os.path.exists(todo_bak):
            if os.path.exists(todo_dir):
                shutil.rmtree(todo_dir)
            shutil.move(todo_bak, todo_dir)
            
        if os.path.exists(frontier_bak):
            if os.path.exists(frontier_dir):
                shutil.rmtree(frontier_dir)
            shutil.move(frontier_bak, frontier_dir)
            
        if os.path.exists("artifacts/todos.md"):
            os.remove("artifacts/todos.md")
            
        if os.path.exists(audit_bak):
            shutil.move(audit_bak, audit_dir)
