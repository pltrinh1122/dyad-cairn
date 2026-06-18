import sys
import yaml
import os

import glob

YML_DIR = "artifacts/audit" if "audit" in os.environ.get("DYAD_DAG_STORE", "artifacts/frontier_state.yml") else "artifacts/frontier"
CONFIG_FILE = "artifacts/audit_config.yml" if "audit" in YML_DIR else "artifacts/frontier_config.yml"
MD_FILE = "artifacts/audit_state.md" if "audit" in YML_DIR else "artifacts/frontier_state.md"

def load_state():
    state = {"nodes": {}}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            c = yaml.safe_load(f) or {}
            if "config" in c:
                state["config"] = c["config"]
    if os.path.exists(YML_DIR):
        for fname in os.listdir(YML_DIR):
            if fname.endswith(".yml"):
                with open(os.path.join(YML_DIR, fname), "r") as f:
                    node_data = yaml.safe_load(f) or {}
                    for k, v in node_data.items():
                        state["nodes"][k] = v
    return state

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
                    print("[STEERING VECTOR] Complete the current PROBE execution and formally reflect it to the Ledger before injecting its downstream PLAN node. Rerun your creation once the substrate is unblocked.")
                    print("==========================================================================")
                    sys.exit(1)

    # Enforce rules: WIP-N=1 at the execution level (QUARRY scope only)
    active_count = 0
    all_nodes = state["nodes"]
    for node_id, data in all_nodes.items():
        if data.get("scope", "").upper() == "SUBSTRATE":
            continue
        if derive_status(node_id, data, all_nodes) == "ACTIVE":
            active_count += 1
            
    if active_count > 1:
        print("ERROR: WIP-N=1 Violation. Cannot save state with multiple ACTIVE QUARRY nodes.")
        sys.exit(1)
        
    # Physically archive DONE nodes to prevent dead mass accumulation while retaining history
    excised = []
    import shutil
    archive_dir = os.path.join("artifacts", "archive", os.path.basename(YML_DIR))
    for node_id, data in list(state["nodes"].items()):
        if derive_status(node_id, data, all_nodes) == "DONE":
            del state["nodes"][node_id]
            excised.append(node_id)
            node_file = os.path.join(YML_DIR, f"{node_id}.yml")
            if os.path.exists(node_file):
                os.makedirs(archive_dir, exist_ok=True)
                shutil.move(node_file, os.path.join(archive_dir, f"{node_id}.yml"))
            
    # Clean up dependencies referencing excised nodes
    if excised:
        for node_id, data in state["nodes"].items():
            if "dependencies" in data:
                data["dependencies"] = [d for d in data["dependencies"] if d not in excised]
                
    os.makedirs(YML_DIR, exist_ok=True)
    if "config" in state:
        with open(CONFIG_FILE, "w") as f:
            yaml.dump({"config": state["config"]}, f, default_flow_style=False, sort_keys=False)
    for node_id, data in state["nodes"].items():
        with open(os.path.join(YML_DIR, f"{node_id}.yml"), "w") as f:
            yaml.dump({node_id: data}, f, default_flow_style=False, sort_keys=False)
            
    # Generate MD projection (Materialized View)
    from skills.frontier_reader import build_tree
    
    dag_name = "Audit State" if "audit" in YML_DIR else "Frontier State"
    source_file = "artifacts/audit" if "audit" in YML_DIR else "artifacts/frontier"
    
    md_lines = [
        f"# The {dag_name} (DAG)\n",
        "> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**",
        f"> Source of truth is `{source_file}`.",
        "> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.\n",
    ]
    
    # 3. Synchronize GEMINI.md Anchor
    try:
        from skills.anchor_compiler import compile_anchor
        compile_anchor()
    except Exception as e:
        print(f"[FLOW WARNING] Anchor Compilation skipped: {e}")

    md_lines.append("```text")
    tree_lines = build_tree(state.get("nodes", {}))
    md_lines.extend(tree_lines)
    md_lines.append("```")
    
    with open(MD_FILE, "w") as f:
        f.write("\n".join(md_lines) + "\n")

# Basic CLI stub for pipeline triggering
if __name__ == "__main__":
    state = load_state()
    if len(sys.argv) == 3:
        node_id = sys.argv[1]
        new_status = sys.argv[2].upper()
        if node_id in state["nodes"]:
            if new_status in ("IN_REVIEW", "AUTHORIZED"):
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
