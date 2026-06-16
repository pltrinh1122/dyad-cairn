import sys
import os
import yaml
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: ./bin/lean <todo_id ... | rubbed>")
        sys.exit(1)
        
    targets = sys.argv[1:]
    
    if targets == ["rubbed"]:
        targets = []
        todo_dir = "artifacts/todos"
        if os.path.exists(todo_dir):
            for fname in sorted(os.listdir(todo_dir)):
                if fname.endswith(".yml"):
                    with open(os.path.join(todo_dir, fname), "r") as f:
                        data = yaml.safe_load(f) or {}
                        tid = list(data.keys())[0] if data else None
                        if tid and data[tid].get("status") == "RUBBED":
                            targets.append(tid)
                            
    if not targets:
        print("[FLOW] No valid targets found for batch execution.")
        sys.exit(0)
        
    nodes_to_execute = []
    
    for tid in targets:
        print(f"--- Processing {tid} ---")
        node_id = tid.replace("todo", "node_todo")
        try:
            # Run convert-todo
            subprocess.run(["./bin/node", "convert-todo", tid], check=True)
            # Run authorize
            subprocess.run(["./bin/node", "authorize", node_id], check=True)
            nodes_to_execute.append(node_id)
        except subprocess.CalledProcessError as e:
            print(f"🚨 CSI GUARD: Trapped failure for node {tid}. Isolating failure and proceeding. 🚨")
            print(f"   [Error: {e}]")
            continue
        
    print("================================================================================")
    print("📋 [MECHANICAL UI PRESENTATION: BATCH DISPATCHER]")
    print("================================================================================")
    print("[AGENT CTA] The batch has been structurally authorized. You are mechanically required to dispatch the following subagents in parallel (using invoke_subagent) to execute them:")
    for nid in nodes_to_execute:
        print(f"execute: {nid}")
    print("================================================================================")

if __name__ == "__main__":
    main()
