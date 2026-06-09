import yaml
import os
import sys

def main():
    print("================================================================================")
    print("📋 [MECHANICAL UI PRESENTATION: ALL QUARRIES & OUTBOXES]")
    print("================================================================================")
    
    print("--- [DEVELOPMENT QUARRIES] (Requires Engine Execution) ---")
    
    # 1. Frontier Quarry (frontier_state.yml)
    print("1. [ACTIVE] The Frontier DAG (artifacts/frontier_state.yml)")
    try:
        from frontier_reader import build_tree
        with open("artifacts/frontier_state.yml", "r") as f:
            frontier = yaml.safe_load(f) or {}
        frontier_nodes = frontier.get("nodes", {})
        if not frontier_nodes:
            print("   └── (empty)")
        else:
            lines = build_tree(frontier_nodes)
            for line in lines:
                print("   " + line)
    except Exception as e:
        print(f"   └── (error: {e})")
        
    print("")

    # 2. Substrate Quarry (todos.yml)
    print("2. [SUBSTRATE] The Passive Quarry (artifacts/todos.yml)")
    try:
        with open("artifacts/todos.yml", "r") as f:
            todos = yaml.safe_load(f) or {}
    except Exception:
        todos = {}
    backlog = todos.get("backlog", {})
    if not backlog:
        print("   └── (empty)")
    else:
        items = list(backlog.items())
        for i, (tid, data) in enumerate(items):
            prefix = "   └──" if i == len(items) - 1 else "   ├──"
            print(f"{prefix} {tid}: {data['intent']}")
            
    print("")
            
    # 3. Integrity Quarry (audit_state.yml)
    print("3. [INTEGRITY] The Active Freeze DAG (artifacts/audit_state.yml)")
    try:
        with open("artifacts/audit_state.yml", "r") as f:
            audit = yaml.safe_load(f) or {}
    except Exception:
        audit = {}
    nodes = audit.get("nodes", {})
    if not nodes:
        print("   └── (empty)")
    else:
        items = list(nodes.items())
        for i, (nid, data) in enumerate(items):
            prefix = "   └──" if i == len(items) - 1 else "   ├──"
            print(f"{prefix} {nid} [{data.get('status', 'UNKNOWN')}]: {data.get('goal', '')}")
            
    print("\n--- [ADMINISTRATIVE OUTBOXES] (Messaging & Sync) ---")
            
    # 4. Spawner Outbox (dm/dyad-touchstone)
    print("4. [SPAWNER] The Touchstone Outbox (dm/dyad-touchstone)")
    try:
        files = os.listdir("dm/dyad-touchstone")
        files = [f for f in files if f.endswith('.md')]
        if not files:
            print("   └── (empty)")
        else:
            print(f"   └── ({len(files)} offline signals pending sync)")
    except Exception:
        print("   └── (directory missing)")
        
    print("")
        
    # 5. Sister Outbox (dm/dyad-wu-wei)
    print("5. [SISTER] The Wu-Wei Outbox (dm/dyad-wu-wei)")
    try:
        files = os.listdir("dm/dyad-wu-wei")
        files = [f for f in files if f.endswith('.md')]
        if not files:
            print("   └── (empty)")
        else:
            for i, f in enumerate(files):
                prefix = "   └──" if i == len(files) - 1 else "   ├──"
                print(f"{prefix} {f}")
    except Exception:
        print("   └── (directory missing)")
        
    print("================================================================================")

if __name__ == "__main__":
    main()
