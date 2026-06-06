import yaml
import sys

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
        if not deps:
            roots.append(n)
        else:
            for d in deps:
                if d in children:
                    children[d].append(n)
                else:
                    children[d] = [n]

    def print_tree(node_id, prefix=""):
        status = nodes[node_id].get('status', 'UNKNOWN')
        title = nodes[node_id].get('title', 'Unknown')
        print(f"{prefix}├── {node_id} [{status}]: {title}")
        
        node_children = children.get(node_id, [])
        for i, child in enumerate(node_children):
            if i == len(node_children) - 1:
                print_tree(child, prefix + "    ")
            else:
                print_tree(child, prefix + "│   ")

    for root in roots:
        print_tree(root, "")

def main():
    try:
        with open("artifacts/frontier_state.yml", "r") as f:
            state = yaml.safe_load(f)
        nodes = state.get('nodes', {})
        print("FRONTIER DAG:")
        build_tree(nodes)
    except Exception as e:
        print(f"Error reading frontier: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
