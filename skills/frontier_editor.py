import sys
import yaml
import os

YML_FILE = "artifacts/frontier_state.yml"
MD_FILE = "artifacts/frontier_state.md"

def load_state():
    if not os.path.exists(YML_FILE):
        return {"nodes": {}}
    with open(YML_FILE, "r") as f:
        return yaml.safe_load(f) or {"nodes": {}}

def save_state(state):
    sys.path.append('.')
    from skills.frontier_reader import derive_status
    
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
            print(f"ERROR: Node {node_id} not found in DAG.")
            sys.exit(1)
    save_state(state)
    print("[FRONTIER] State computationally validated and View projected.")
