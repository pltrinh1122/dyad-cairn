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
    
    # 1. Push branch to remote
    # Get current branch
    branch = run_cmd("git rev-parse --abbrev-ref HEAD")
    print(f"[FLOW] Pushing branch {branch} to remote...")
    run_cmd(f"git push -u origin {branch}")
    
    # 2. Open Pull Request
    print("[FLOW] Generating Pull Request...")
    # Import inside function to avoid circular/early imports if not needed
    sys.path.append('.')
    from skills.github_client import create_pr
    title = f"[Node] Complete {node_id}"
    body = f"Automated PR for Node {node_id} completion."
    pr_url = create_pr(title, body)
    print(f"[FLOW] PR successfully opened at: {pr_url}")
    
    # 3. Transition DAG Status
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
