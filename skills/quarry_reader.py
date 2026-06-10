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
    print("1. [ACTIVE] The Execution DAG (artifacts/frontier_state.yml)")
    try:
        from skills.frontier_reader import build_tree, derive_status
        with open("artifacts/frontier_state.yml", "r") as f:
            frontier = yaml.safe_load(f) or {}
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

    print("2. [PRE-QUARRY] The Passive Backlog (artifacts/todos.yml)")
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
            intent = data.get('intent', 'UNKNOWN')
            print(f"{prefix} {tid}: {intent}")
            
    print("")
    print("--- [SUBSTRATE] (Monitoring & Remediation) ---")
    print("3. [FROZEN] The Integrity Audits (artifacts/audit_state.yml)")
    try:
        with open("artifacts/audit_state.yml", "r") as f:
            audit = yaml.safe_load(f) or {}
    except Exception:
        audit = {}
    audit_nodes = audit.get("nodes", {})
    
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
