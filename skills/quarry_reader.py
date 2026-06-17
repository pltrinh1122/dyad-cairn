import yaml
import os
import sys
import subprocess

def main():
    print("================================================================================")
    print("📋 [MECHANICAL UI PRESENTATION: DYAD STATE]")
    print("================================================================================")
    print("")
    
    print("--- [QUARRY] (Research & Development) ---")
    print("1. [ACTIVE] The Execution DAG (artifacts/frontier/)")
    try:
        from skills.frontier_reader import build_tree, derive_status
        import sys
        sys.path.append('.')
        from skills.frontier_editor import load_state
        frontier = load_state()
        frontier_nodes = frontier.get("nodes", {})
        
        ledger_content = ""
        if os.path.exists("DYAD_LEDGER.md"):
            with open("DYAD_LEDGER.md", "r", encoding="utf-8") as lf:
                ledger_content = lf.read()
        try:
            res = subprocess.run(["git", "branch"], capture_output=True, text=True)
            active_branches = res.stdout if res.returncode == 0 else ""
        except Exception:
            active_branches = ""

        active_nodes = {}
        for k, v in frontier_nodes.items():
            st = derive_status(k, v, frontier_nodes, ledger_content, active_branches)
            if st != "DONE":
                active_nodes[k] = v
                
        if not active_nodes:
            print("   └── (empty)")
        else:
            lines = build_tree(active_nodes)
            for line in lines:
                print("   " + line)
    except Exception as e:
        print(f"   └── (error: {e})")
        
    print("")

    print("2. [PRE-QUARRY] The Passive Backlog (artifacts/todos/)")
    todos = {"backlog": {}}
    if os.path.exists("artifacts/todos"):
        for fname in sorted(os.listdir("artifacts/todos")):
            if fname.endswith(".yml"):
                with open(os.path.join("artifacts/todos", fname), "r") as f:
                    data = yaml.safe_load(f) or {}
                    for k, v in data.items():
                        todos["backlog"][k] = v
    backlog = todos.get("backlog", {})
    if not backlog:
        print("   └── (empty)")
    else:
        items = list(backlog.items())
        for i, (tid, data) in enumerate(items):
            prefix = "   └──" if i == len(items) - 1 else "   ├──"
            status = data.get('status', 'UNRUBBED')
            raw_thought = data.get('raw_thought', 'UNKNOWN')
            if len(raw_thought) > 60:
                raw_thought = raw_thought[:57] + "..."
            print(f"{prefix} {tid} [{status}]: {raw_thought}")
            
    print("")
    print("--- [SUBSTRATE] (Monitoring & Remediation) ---")
    print("3. [FROZEN] The Integrity Audits (artifacts/audit/)")
    audit_nodes = {}
    if os.path.exists("artifacts/audit"):
        for fname in sorted(os.listdir("artifacts/audit")):
            if fname.endswith(".yml"):
                try:
                    with open(os.path.join("artifacts/audit", fname), "r") as f:
                        data = yaml.safe_load(f) or {}
                        if "nodes" in data:
                            for k, v in data["nodes"].items():
                                audit_nodes[k] = v
                        else:
                            for k, v in data.items():
                                audit_nodes[k] = v
                except Exception:
                    pass
    
    total_audits = len(audit_nodes)
    failing_audits = {k: v for k, v in audit_nodes.items() if str(v.get("status", "")).upper() == "FAILING"}
    
    if total_audits == 0:
        print("   └── [HEALTH: UNKNOWN] (No invariants defined)")
    elif not failing_audits:
        print(f"   └── [HEALTH: GREEN] ({total_audits} invariants actively guarding)")
    else:
        passing_count = total_audits - len(failing_audits)
        print(f"   ├── [HEALTH: BREACHED] ({passing_count} invariants guarding)")
        items = list(failing_audits.items())
        for i, (nid, data) in enumerate(items):
            prefix = "   └──" if i == len(items) - 1 else "   ├──"
            print(f"{prefix} {nid} [FAILING]: {data.get('goal', '')}")
            
    print("================================================================================")

if __name__ == "__main__":
    main()
