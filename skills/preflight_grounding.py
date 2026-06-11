import os
import sys

def assert_grounding(node_id, node_data):
    prerequisites = node_data.get("prerequisites", [])
    if not prerequisites:
        print(f"🚨 CSI GUARD BLOCK: Pre-requisite missing! Node '{node_id}' does not define any prerequisites.")
        print("[FLOW] Autonomous execution requires deterministic grounding bounds. Add 'prerequisites' to the node YAML.")
        sys.exit(1)
        
    for req in prerequisites:
        if not os.path.exists(req):
            print(f"🚨 CSI GUARD BLOCK: Pre-requisite '{req}' is missing from the physical substrate! 🚨")
            print("[FLOW] The DAG topological clearance is overridden. Execution is safely stalled.")
            sys.exit(1)
    
    print(f"[FLOW] Mechanical Grounding PASSED for {node_id}.")
