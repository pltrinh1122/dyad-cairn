import yaml
import sys

def main():
    try:
        with open("artifacts/todos.yml", "r") as f:
            todos = yaml.safe_load(f) or {}
    except Exception:
        todos = {}
        
    backlog = todos.get("backlog", {})
    print("TODO RACK (Pre-DAG Holding Pen):")
    
    if not backlog:
        print("└── (empty)")
        return
        
    items = list(backlog.items())
    for i, (tid, data) in enumerate(items):
        prefix = "└──" if i == len(items) - 1 else "├──"
        print(f"{prefix} {tid} ({data['timestamp']}): {data['intent']}")

if __name__ == "__main__":
    main()
