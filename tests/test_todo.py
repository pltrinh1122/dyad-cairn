import os
import subprocess
import shutil

def test_todo_id_collision():
    todo_dir = "artifacts/todos"
    todo_bak = "artifacts/todos_bak_col"
    if os.path.exists(todo_dir):
        shutil.copytree(todo_dir, todo_bak, dirs_exist_ok=True)
        shutil.rmtree(todo_dir)
    os.makedirs(todo_dir, exist_ok=True)
    
    try:
        n_calls = 50
        procs = []
        for i in range(n_calls):
            procs.append(subprocess.Popen(["./bin/todo", f"collision_intent_{i}"]))
        
        for p in procs:
            p.wait()
            
        files = [f for f in os.listdir(todo_dir) if f.endswith('.yml')]
        assert len(files) == n_calls, f"Expected {n_calls} unique todos, got {len(files)}. Collision occurred!"
    finally:
        if os.path.exists(todo_bak):
            if os.path.exists(todo_dir):
                shutil.rmtree(todo_dir)
            shutil.move(todo_bak, todo_dir)
