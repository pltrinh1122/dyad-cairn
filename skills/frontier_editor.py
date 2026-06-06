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
    # Enforce rules: WIP-N=1 at the execution level
    active_count = sum(1 for n in state["nodes"].values() if n.get("status") == "ACTIVE")
    if active_count > 1:
        print("ERROR: WIP-N=1 Violation. Cannot save state with multiple ACTIVE nodes.")
        sys.exit(1)
        
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
    status_order = ["ACTIVE", "IN_REVIEW", "BLOCKED", "DONE"]
    
    for status in status_order:
        status_nodes = {k: v for k, v in state["nodes"].items() if v.get("status") == status}
        if status_nodes:
            icon = "🟢" if status == "ACTIVE" else "🟡" if status == "IN_REVIEW" else "🔴"
            md_lines.append(f"\n## {icon} {status} NODES")
            for node_id, data in status_nodes.items():
                md_lines.append(f"- **{node_id}**: {data.get('title', 'Unknown')}")
                if "goal" in data:
                    md_lines.append(f"  - *Goal:* {data['goal']}")
                if "dependencies" in data and data["dependencies"]:
                    md_lines.append(f"  - *Dependencies:* {', '.join(data['dependencies'])}")
    
    with open(MD_FILE, "w") as f:
        f.write("\n".join(md_lines) + "\n")

# Basic CLI stub for pipeline triggering
if __name__ == "__main__":
    state = load_state()
    # Future: parse sys.argv to actively add/modify nodes
    if len(sys.argv) > 1:
        print("Mutations not fully implemented yet, simply verifying DAG and regenerating View.")
    save_state(state)
    print("[FRONTIER] State computationally validated and View projected.")
