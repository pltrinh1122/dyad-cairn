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
    items = list(backlog.items())
    strategic_items = [(tid, data) for tid, data in items if data.get('status', 'UNRUBBED') != 'AUTO-REPLY']
    auto_reply_items = [(tid, data) for tid, data in items if data.get('status', 'UNRUBBED') == 'AUTO-REPLY']

    print("TODO RACK (Pre-DAG Holding Pen):")
    if not strategic_items:
        print("└── (empty)")
    else:
        for i, (tid, data) in enumerate(strategic_items):
            prefix = "└──" if i == len(strategic_items) - 1 else "├──"
            intent = data.get('intent', data.get('raw_thought', ''))
            status = data.get('status', 'UNRUBBED')
            print(f"{prefix} [{status}] {tid} ({data.get('timestamp', '')}): {intent}")

    if auto_reply_items:
        print("\nAUTO-REPLY RACK (Non-Strategic Traffic):")
        for i, (tid, data) in enumerate(auto_reply_items):
            prefix = "└──" if i == len(auto_reply_items) - 1 else "├──"
            intent = data.get('intent', data.get('raw_thought', ''))
            status = data.get('status', 'UNRUBBED')
            print(f"{prefix} [{status}] {tid} ({data.get('timestamp', '')}): {intent}")

if __name__ == "__main__":
    main()
