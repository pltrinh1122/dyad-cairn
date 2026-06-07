import sys
import yaml
import os

YML_FILE = os.environ.get("DYAD_DAG_STORE", "artifacts/frontier_state.yml")
MD_FILE = YML_FILE.replace(".yml", ".md")

def load_state():
    if not os.path.exists(YML_FILE):
        return {"nodes": {}}
    with open(YML_FILE, "r") as f:
        return yaml.safe_load(f) or {"nodes": {}}

def save_state(state):
    sys.path.append('.')
    from skills.frontier_reader import derive_status
    
    # Enforce SPAOR PLAN Injection Guard
    import subprocess
    import re
    
    # Get current branch safely
    try:
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], 
            capture_output=True, text=True, check=True
        )
        current_branch = branch_result.stdout.strip()
    except Exception:
        current_branch = "unknown"
        
    for node_id, data in state.get("nodes", {}).items():
        if data.get("type", "").upper() == "PLAN":
            # Extract parent prefix, e.g., node_17a_plan_x -> node_17a
            # Also handle if it's node_17_plan_x -> node_17
            match = re.match(r"(node_[0-9a-z]+)_plan", node_id)
            if match:
                parent_prefix = match.group(1)
                # The parent probe node must start with this prefix and contain _probe
                # But in DYAD_LEDGER.md, it's just recorded by its exact ID.
                # However, we only have the prefix from the plan node!
                # Wait, DYAD_LEDGER.md records [node_X_probe_Y]. We can just regex search for `\[{parent_prefix}_probe`
                
                # Condition 1: Are we currently checked out on the parent PROBE branch?
                is_on_probe_branch = current_branch.startswith(f"active/{parent_prefix}_probe")
                
                # Condition 2: Is the parent PROBE node in the Ledger as DONE?
                is_probe_in_ledger = False
                ledger_path = "DYAD_LEDGER.md"
                if os.path.exists(ledger_path):
                    with open(ledger_path, "r") as lf:
                        ledger_content = lf.read()
                    # e.g., `[node_17_probe`
                    if re.search(rf"\[{parent_prefix}_probe", ledger_content):
                        is_probe_in_ledger = True
                        
                if not (is_on_probe_branch or is_probe_in_ledger):
                    print("==========================================================================")
                    print("🚨 SPAOR PLAN INJECTION GUARD FIRED 🚨")
                    print(f"You attempted to inject PLAN node '{node_id}' for unexecuted PROBE '{parent_prefix}'.")
                    print("PLAN can only be created while in a PROBE for itself, not for other PROBE.")
                    print("==========================================================================")
                    sys.exit(1)

    # Enforce rules: WIP-N=1 at the execution level
    active_count = 0
    all_nodes = state["nodes"]
    for node_id, data in all_nodes.items():
        if derive_status(node_id, data, all_nodes) == "ACTIVE":
            active_count += 1
            
    if active_count > 1:
        print("ERROR: WIP-N=1 Violation. Cannot save state with multiple ACTIVE nodes.")
        sys.exit(1)
        
    # Physically excise DONE nodes to prevent dead mass accumulation
    excised = []
    for node_id, data in list(state["nodes"].items()):
        if derive_status(node_id, data, all_nodes) == "DONE":
            del state["nodes"][node_id]
            excised.append(node_id)
            
    # Clean up dependencies referencing excised nodes
    if excised:
        for node_id, data in state["nodes"].items():
            if "dependencies" in data:
                data["dependencies"] = [d for d in data["dependencies"] if d not in excised]
                
    with open(YML_FILE, "w") as f:
        yaml.dump(state, f, default_flow_style=False, sort_keys=False)
        
    # Generate MD projection (Materialized View)
    md_lines = [
        "# The Frontier State (DAG)\n",
        "> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**",
        "> Source of truth is `artifacts/frontier_state.yml`.",
        "> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.\n"
    ]
    
    # Sort nodes by status for display
    status_order = ["ACTIVE", "IN_REVIEW", "BLOCKED", "READY"]
    
    from collections import defaultdict
    nodes_by_status = defaultdict(dict)
    
    for node_id, data in state["nodes"].items():
        # Keep the IN_REVIEW string if it exists in the DAG, else dynamically derive
        current_cache = data.get("status")
        if current_cache == "IN_REVIEW":
            status = "IN_REVIEW"
        else:
            status = derive_status(node_id, data, state["nodes"])
        nodes_by_status[status][node_id] = data
    
    for status in status_order:
        status_nodes = nodes_by_status.get(status, {})
        if status_nodes:
            icon = "🟢" if status == "ACTIVE" else "🟡" if status == "IN_REVIEW" else "🔴"
            md_lines.append(f"\n## {icon} {status} NODES")
            for node_id, data in status_nodes.items():
                node_type = f" [{data['type'].upper()}]" if "type" in data else ""
                md_lines.append(f"- **{node_id}**{node_type}: {data.get('title', 'Unknown')}")
                if "goal" in data:
                    md_lines.append(f"  - *Goal:* {data['goal']}")
                if "dependencies" in data and data["dependencies"]:
                    md_lines.append(f"  - *Dependencies:* {', '.join(data['dependencies'])}")
    
    with open(MD_FILE, "w") as f:
        f.write("\n".join(md_lines) + "\n")

# Basic CLI stub for pipeline triggering
if __name__ == "__main__":
    state = load_state()
    if len(sys.argv) == 3:
        node_id = sys.argv[1]
        new_status = sys.argv[2].upper()
        if node_id in state["nodes"]:
            if new_status == "IN_REVIEW":
                state["nodes"][node_id]["status"] = new_status
            else:
                # For ACTIVE, READY, DONE, we delete the explicit status cache to let derive_status compute it
                if "status" in state["nodes"][node_id]:
                    del state["nodes"][node_id]["status"]
            print(f"[FRONTIER] Transitioned Node {node_id} toward {new_status}")
        else:
            if new_status == "DONE":
                print(f"[FRONTIER] Node {node_id} not found in DAG. It may have been autonomously excised.")
            else:
                print(f"ERROR: Node {node_id} not found in DAG.")
                sys.exit(1)
    save_state(state)
    print("[FRONTIER] State computationally validated and View projected.")
