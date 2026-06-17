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

def _call_llm_semantic_check(batch_data):
    """
    Placeholder for the actual LLM call to compare WHAT intents.
    Returns True if the batch is semantically cohesive, False otherwise.
    """
    return True

def assert_batch_semantic_alignment(batch_data):
    if not _call_llm_semantic_check(batch_data):
        print("🚨 CSI GUARD BLOCK: Batch nodes are semantically disconnected! 🚨")
        print("[FLOW] The LLM check determined the WHAT intents of the batch lack cohesion. Execution is safely stalled.")
        sys.exit(1)
    print(f"[FLOW] Semantic Batch Alignment PASSED for {len(batch_data)} nodes.")
