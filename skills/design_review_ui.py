import sys
import yaml
import os
import re
import glob

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
    node_type = node_data.get('type', 'UNKNOWN').upper()
    
    print("\n" + "="*80)
    print(f"📋 [MECHANICAL UI PRESENTATION: HTIL DESIGN REVIEW]")
    print(f"Node:  {node_id}")
    print(f"Type:  {node_type}")
    print(f"Title: {node_data.get('title', 'Untitled')}")
    
    if node_type == "PLAN":
        match = re.match(r"(node_[0-9a-z]+)_plan", node_id)
        if match:
            prefix = match.group(1)
            probe_files = glob.glob(f"artifacts/probe_{prefix}_*.md")
            if probe_files:
                probe_file = probe_files[0]
                with open(probe_file, "r") as f:
                    content = f.read()
                    
                print(f"--- [PROBE CONTEXT: {os.path.basename(probe_file)}] ---")
                
                condition_match = re.search(r"(?im)^##\s+.*?(?:Condition|Problem).*?\n(.*?)(?=\n##\s|\Z)", content, re.DOTALL)
                if condition_match:
                    print(f"Unfalsified Condition:\n{condition_match.group(1).strip()}\n")
                else:
                    print("Unfalsified Condition: (Not explicitly formatted in Probe artifact)\n")
                    
                invariant_match = re.search(r"(?im)^##\s+.*?Invariant.*?\n(.*?)(?=\n##\s|\Z)", content, re.DOTALL)
                if invariant_match:
                    print(f"Discovered Invariants:\n{invariant_match.group(1).strip()}\n")
                else:
                    print("Discovered Invariants: (Not explicitly formatted in Probe artifact)\n")
                    
                decomp_match = re.search(r"(?im)^##\s+.*?Decomposition.*?\n(.*?)(?=\n##\s|\Z)", content, re.DOTALL)
                if decomp_match:
                    print(f"Decomposition Strategy:\n{decomp_match.group(1).strip()}\n")
                else:
                    print("Decomposition Strategy: Atomic Probe (Mapped 1:1 to this PLAN).")
            else:
                print(f"Goal:  {node_data.get('goal', 'No goal specified')}")
                print(f"Warning: No parent probe artifact found (expected artifacts/probe_{prefix}_*.md).")
        else:
            print(f"Goal:  {node_data.get('goal', 'No goal specified')}")
    else:
        print(f"Goal:  {node_data.get('goal', 'No goal specified')}")
        
    print("="*80)
    print(f"[CYBERNETIC STEERING VECTOR] To authorize this node for execution, run:")
    cli_prefix = "./bin/audit-node" if "audit" in state_file else "./bin/node"
    print(f"-> {cli_prefix} authorize {node_id}")
    print("="*80 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 skills/design_review_ui.py <node_id>")
        sys.exit(1)
    present_design_review(sys.argv[1])
