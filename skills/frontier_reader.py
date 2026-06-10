import yaml
import sys
import os
import subprocess

def derive_status(node_id, node_data, all_nodes, ledger_content=None, active_branches=None):
    if ledger_content is None:
        if os.path.exists("DYAD_LEDGER.md"):
            with open("DYAD_LEDGER.md", "r", encoding="utf-8") as f:
                ledger_content = f.read()
        else:
            ledger_content = ""
            
    if active_branches is None:
        try:
            res = subprocess.run(["git", "branch"], capture_output=True, text=True)
            active_branches = res.stdout if res.returncode == 0 else ""
        except Exception:
            active_branches = ""

    import re
    prefix_match = re.match(r"(node_[0-9a-z]+)", node_id)
    prefix = prefix_match.group(1) if prefix_match else node_id

    if ledger_content:
        norm_prefix = prefix.replace("_", " ").lower()
        if node_id in ledger_content or (prefix and norm_prefix in ledger_content.lower()):
            return "DONE"
            
    if active_branches:
        for line in active_branches.splitlines():
            branch = line.replace("*", "").strip()
            if branch == 'main':
                continue
            if node_id in branch:
                return "ACTIVE"
        
    deps = node_data.get('dependencies', [])
    if not deps:
        return "READY"
        
    for dep_id in deps:
        if dep_id not in all_nodes:
            dep_status = derive_status(dep_id, {}, all_nodes, ledger_content, active_branches)
            if dep_status != "DONE":
                return "BLOCKED"
            continue
        dep_status = derive_status(dep_id, all_nodes[dep_id], all_nodes, ledger_content, active_branches)
        if dep_status != "DONE":
            return "BLOCKED"
            
    return "READY"

def build_tree(nodes):
    # A simple horizontal ASCII tree
    # Since nodes have dependencies, we can map them.
    # We want a tree like:
    # ├── node_0 [DONE]
    # │   ├── node_1 [DONE]
    # │   └── node_2a [DONE]
    # │       └── node_2b [BLOCKED]
    
    # Build reverse mapping (children)
    children = {n: [] for n in nodes}
    roots = []
    
    for n, data in nodes.items():
        deps = data.get('dependencies', [])
        is_root = True
        
        for d in deps:
            if d in nodes:
                is_root = False
                if d in children:
                    children[d].append(n)
                else:
                    children[d] = [n]
                    
        if is_root:
            roots.append(n)

    lines = []

    def print_tree(node_id, prefix=""):
        derived = derive_status(node_id, nodes[node_id], nodes)
        if nodes[node_id].get('status') == "IN_REVIEW" and derived == "READY":
            status = "IN_REVIEW"
        elif nodes[node_id].get('status') == "AUTHORIZED" and derived == "READY":
            status = "AUTHORIZED"
        else:
            status = derived
            
        title = nodes[node_id].get('title', 'Unknown')
        node_type = f" [{nodes[node_id]['type'].upper()}]" if "type" in nodes[node_id] else ""
        node_scope = f" [{nodes[node_id]['scope'].upper()}]" if "scope" in nodes[node_id] else ""
        lines.append(f"{prefix}├── {node_id} [{status}]{node_type}{node_scope}: {title}")
        
        node_children = children.get(node_id, [])
        for i, child in enumerate(node_children):
            if i == len(node_children) - 1:
                print_tree(child, prefix + "    ")
            else:
                print_tree(child, prefix + "│   ")

    for root in roots:
        print_tree(root, "")
        
    return lines

def main():
    try:
        yml_file = os.environ.get("DYAD_DAG_STORE", "artifacts/frontier_state.yml")
        with open(yml_file, "r") as f:
            state = yaml.safe_load(f)
        nodes = state.get('nodes', {})
        dag_name = "AUDIT DAG" if "audit" in yml_file else "FRONTIER DAG"
        print("================================================================================")
        print(f"📋 [MECHANICAL UI PRESENTATION: {dag_name}]")
        print("================================================================================")
        tree_lines = build_tree(nodes)
        for line in tree_lines:
            print(line)
        print("================================================================================")
    except Exception as e:
        print(f"Error reading frontier: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
