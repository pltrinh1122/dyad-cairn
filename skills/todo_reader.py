import yaml
import sys

def main():
    import os
    todos = {"backlog": {}}
    todo_dir = "artifacts/todos"
    if os.path.exists(todo_dir):
        for fname in sorted(os.listdir(todo_dir)):
            if fname.endswith(".yml"):
                with open(os.path.join(todo_dir, fname), "r") as f:
                    data = yaml.safe_load(f) or {}
                    for k, v in data.items():
                        todos["backlog"][k] = v
        
    backlog = todos.get("backlog", {})
    print("TODO RACK (Pre-DAG Holding Pen):")
    
    if not backlog:
        print("└── (empty)")
        return
        
    items = list(backlog.items())
    for i, (tid, data) in enumerate(items):
        prefix = "└──" if i == len(items) - 1 else "├──"
        intent = data.get('intent', data.get('raw_thought', ''))
        status = data.get('status', 'UNRUBBED')
        print(f"{prefix} [{status}] {tid} ({data.get('timestamp', '')}): {intent}")

if __name__ == "__main__":
    main()
