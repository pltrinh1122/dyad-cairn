import sys
import yaml
import os
from datetime import datetime

YML_FILE = "artifacts/rack_state.yml"

def load_stack():
    if not os.path.exists(YML_FILE):
        return {"stack": []}
    with open(YML_FILE, "r") as f:
        data = yaml.safe_load(f)
        if not data or "stack" not in data:
            return {"stack": []}
        return data

def save_stack(data):
    with open(YML_FILE, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

def push_task(task_string):
    data = load_stack()
    # Enforce LIFO: push to the front (index 0)
    data["stack"].insert(0, task_string)
    save_stack(data)
    print(f"[STACK] Pushed: '{task_string}'")

def pop_task():
    data = load_stack()
    if not data["stack"]:
        print("[STACK] Empty. No tasks to pop.")
        sys.exit(0)
    
    # Enforce LIFO: pop from the front (index 0)
    task = data["stack"].pop(0)
    save_stack(data)
    print(f"[STACK] Popped: '{task}'")

def list_tasks():
    data = load_stack()
    if not data["stack"]:
        print("[STACK] Empty.")
        sys.exit(0)
    
    print("--- EXECUTION STACK (LIFO) ---")
    for i, task in enumerate(data["stack"]):
        # Index 0 is TOP
        prefix = "-> [TOP] " if i == 0 else f"   [{i}]   "
        print(f"{prefix}{task}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 skills/prompt_manager.py <push|pop|list> [task_string]")
        sys.exit(1)
        
    command = sys.argv[1].lower()
    
    if command == "push":
        if len(sys.argv) < 3:
            print("Error: 'push' requires a task string.")
            sys.exit(1)
        push_task(sys.argv[2])
    elif command == "pop":
        pop_task()
    elif command == "list":
        list_tasks()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
