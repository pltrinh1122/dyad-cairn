import sys
import yaml
import os

def present_design_review(node_id, state=None):
    state_file = os.environ.get("DYAD_DAG_STORE", "artifacts/frontier_state.yml")
    if state is None:
        if not os.path.exists(state_file):
            print(f"ERROR: {state_file} not found.")
            sys.exit(1)
            
        with open(state_file, "r") as f:
            state = yaml.safe_load(f) or {}
        
    nodes = state.get("nodes", {})
    if node_id not in nodes:
        print(f"ERROR: Node {node_id} not found in {state_file}.")
        sys.exit(1)
        
    node_data = nodes[node_id]
    print("\n" + "="*80)
    print(f"📋 [MECHANICAL UI PRESENTATION: HTIL DESIGN REVIEW]")
    print(f"Node:  {node_id}")
    print(f"Type:  {node_data.get('type', 'UNKNOWN')}")
    print(f"Title: {node_data.get('title', 'Untitled')}")
    print(f"Goal:  {node_data.get('goal', 'No goal specified')}")
    print("="*80)
    print(f"[CYBERNETIC STEERING VECTOR] To authorize this node for execution, run:")
    # Detect CLI context
    cli_prefix = "./bin/audit-node" if "audit" in state_file else "./bin/node"
    print(f"-> {cli_prefix} authorize {node_id}")
    print("="*80 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 skills/design_review_ui.py <node_id>")
        sys.exit(1)
    present_design_review(sys.argv[1])
