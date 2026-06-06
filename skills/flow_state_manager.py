import sys
import subprocess

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def plan_node(node_id):
    print(f"[FLOW] Planning Node {node_id}...")
    # Calls bin/backlog to rack the node (stubbed logic)
    print(run_cmd(f"./bin/backlog rack {node_id}"))

def checkout_node(node_id):
    branch_name = f"active/{node_id}"
    print(f"[FLOW] Checking out branch: {branch_name}")
    run_cmd(f"git checkout -b {branch_name}")

def reflect_node(node_id):
    print(f"[FLOW] Reflecting Node {node_id}...")
    # Commits code, opens PR, and updates frontier status
    print("Code committed and PR generation simulated.")
    # Here we would call frontier_editor.py to change status to IN_REVIEW
    run_cmd(f"python3 skills/frontier_editor.py")
    print(f"[FLOW] Node {node_id} status transitioned to IN_REVIEW. Execution halted.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 skills/flow_state_manager.py <plan|checkout|reflect> <node_id>")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    node = sys.argv[2]
    
    if action == "plan":
        plan_node(node)
    elif action == "checkout":
        checkout_node(node)
    elif action == "reflect":
        reflect_node(node)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
