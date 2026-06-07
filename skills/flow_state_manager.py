import sys
import subprocess
import os

def run_cmd(cmd, allow_fail=False):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and not allow_fail:
        print(f"ERROR: {result.stderr}")
        sys.exit(1)
    if allow_fail and result.returncode != 0:
        return result.stdout.strip() + "\n" + result.stderr.strip()
    return result.stdout.strip()

def check_retro_lock():
    import os
    if os.path.exists("dyad-state/RETRO_ACTIVE.lock"):
        print("==========================================================================")
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("A Retro is currently active. You are mechanically forbidden from transitioning")
        print("the SPAOR state machine (plan/checkout/reflect) while a retro is open.")
        print("You must resolve the retro and physically execute `./bin/retro` to unlock.")
        print("==========================================================================")
        sys.exit(1)

def check_sovereignty_trigger():
    # Durably monitors if stone.yaml has been codified into the Commons boundary.
    # Relies on the state of the commons/ submodule rather than ephemeral background processes.
    result = subprocess.run("git -C commons grep -i '\\bstone\\.yaml\\b'", shell=True, capture_output=True, text=True)
    if result.returncode == 0 and result.stdout.strip():
        print("==========================================================================")
        print("🚨 SOVEREIGNTY TRIGGER FIRED 🚨")
        print("The Commons has formally adopted 'stone.yaml'. Local sovereignty is void.")
        print("Any mutations to the mason schema must now be treated as external blockers.")
        print("==========================================================================")
        # In a fully realized state, this might sys.exit(1) until Operator acknowledges.

def check_audit_lock():
    import yaml
    import os
    # Only enforce if we are operating on the Frontier DAG
    current_store = os.environ.get("DYAD_DAG_STORE", "artifacts/frontier_state.yml")
    if current_store != "artifacts/frontier_state.yml":
        return

    audit_file = "artifacts/audit_state.yml"
    if os.path.exists(audit_file):
        with open(audit_file, "r") as f:
            state = yaml.safe_load(f) or {"nodes": {}}
        for node_id, data in state.get("nodes", {}).items():
            if data.get("status") != "DONE":
                print("==========================================================================")
                print("🚨 GOVERNANCE DEBT GUARDRAIL FIRED 🚨")
                print("The Audit DAG has unresolved alignment nodes. Alignment Precedes Execution.")
                print("You are mechanically forbidden from transitioning the Frontier DAG until")
                print("the Audit DAG is physically cleared (all nodes DONE).")
                print("==========================================================================")
                sys.exit(1)
def plan_node(node_id):
    print(f"[FLOW] Planning Node {node_id}...")
    print(f"[FLOW] Local DAG asserts planning. No remote issue required.")

def checkout_node(node_id):
    branch_name = f"active/{node_id}"
    print(f"[FLOW] Checking out branch: {branch_name}")
    run_cmd(f"git checkout -b {branch_name}")

def inject_node(node_id, title, goal):
    print(f"[FLOW] Injecting Node {node_id} (IN_REVIEW)...")
    sys.path.append('.')
    from skills.frontier_editor import load_state, save_state
    state = load_state()
    if node_id in state["nodes"]:
        print(f"ERROR: Node {node_id} already exists.")
        sys.exit(1)
        
    node_type = "PROBE" if "probe" in node_id else "PLAN"
    state["nodes"][node_id] = {
        "status": "IN_REVIEW",
        "title": title,
        "goal": goal,
        "type": node_type
    }
    save_state(state)
    print(f"[FLOW] Node {node_id} successfully injected and blocked at the Design-Review Gate.")

def authorize_node(node_id):
    print(f"[FLOW] Authorizing Node {node_id}...")
    sys.path.append('.')
    from skills.frontier_editor import load_state, save_state
    state = load_state()
    if node_id not in state["nodes"]:
        print(f"ERROR: Node {node_id} not found.")
        sys.exit(1)
        
    current_status = state["nodes"][node_id].get("status")
    if current_status != "IN_REVIEW":
        print(f"ERROR: Node {node_id} is {current_status}. It must be IN_REVIEW to be authorized.")
        sys.exit(1)
        
    state["nodes"][node_id]["status"] = "READY"
    save_state(state)
    print(f"[FLOW] Node {node_id} transitioned to READY. Execution authorized.")

def reflect_node_red(node_id):
    print(f"[FLOW] Reflecting RED Phase (Intent Gate) for Node {node_id}...")
    print("[FLOW] Asserting Mechanical Gate (TDD must FAIL)...")
    sys.path.append('.')
    try:
        from skills.testing_harness import run_tests
        test_result = run_cmd("python3 skills/testing_harness.py", allow_fail=True)
        print(test_result)
    except Exception as e:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("TDD execution threw an unhandled exception. Fix syntax errors before reflecting red.")
        sys.exit(1)
        
    if "🚨" in test_result:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("A structural CSI Guard was tripped during the Red Phase.")
        print("You are mechanically forbidden from generating an Intent PR until the substrate is physically unblocked.")
        sys.exit(1)
        
    if "PASS" in test_result:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("Tests PASSED in the Red phase. You must write failing tests that map to Operator intent before reflecting.")
        sys.exit(1)
        
    create_reflection_pr(node_id, is_green=False)

def reflect_node_green(node_id, retro_msg):
    print(f"[FLOW] Reflecting GREEN Phase (Mechanical Gate) for Node {node_id}...")
    print("[FLOW] Asserting Mechanical UI Gate (Dialect Linter)...")
    linter_result = subprocess.run("python3 skills/dialect_linter.py", shell=True, capture_output=True, text=True)
    if linter_result.returncode != 0:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print(linter_result.stdout)
        print("The Agent must physically run the UI presentation tools. You are blocked.")
        sys.exit(1)
        
    print("[FLOW] Asserting Mechanical Gate (TDD must PASS)...")
    sys.path.append('.')
    try:
        from skills.testing_harness import run_tests
        test_result = run_cmd("python3 skills/testing_harness.py", allow_fail=True)
        print(test_result)
    except Exception as e:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("TDD execution failed. The PR Gate is mechanically sealed until tests pass.")
        sys.exit(1)
        
    if "🚨" in test_result:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("A structural CSI Guard was tripped during the Green Phase.")
        print("You are mechanically forbidden from generating a Green PR until the substrate is physically unblocked.")
        sys.exit(1)
        
    if "FAIL" in test_result:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("Tests failed. You are mathematically forbidden from generating a Green PR.")
        sys.exit(1)
        
    print(f"[FLOW] Synthesis Invariant: Appending retro_msg to Ledger...")
    from skills import ledger_manager
    full_retro_msg = f"[{node_id}] {retro_msg}"
    ledger_manager.append_ledger("node-retro", full_retro_msg)
    
    # Commit the ledger before generating the PR so it's included in the execution payload
    run_cmd('git add DYAD_LEDGER.md dyad-state/ledger.jsonl && git commit -m "chore(ledger): retro synthesis for green phase"')
    
    create_reflection_pr(node_id, is_green=True)

def create_reflection_pr(node_id, is_green):
    # 1. Push branch to remote
    # Get current branch
    branch = run_cmd("git rev-parse --abbrev-ref HEAD")
    print(f"[FLOW] Pushing branch {branch} to remote...")
    run_cmd(f"git push -u origin {branch}")
    
    # 2. Open Pull Request
    print("[FLOW] Generating Pull Request...")
    
    # Extract Test Spec for PR Body
    test_spec_body = "### Operator Validation Spec (The Tests)\n\n"
    try:
        import ast
        import os
        # Find test files modified in this branch compared to main
        diff_files = run_cmd("git diff --name-only main...HEAD").splitlines()
        test_files = [f for f in diff_files if f.startswith('tests/') and f.endswith('.py') and os.path.exists(f)]
        
        if test_files:
            for tf in test_files:
                test_spec_body += f"#### `{tf}`\n"
                with open(tf, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                            doc = ast.get_docstring(node)
                            doc_text = f": {doc}" if doc else ""
                            test_spec_body += f"- **{node.name}**{doc_text}\n"
                test_spec_body += "\n"
        else:
            test_spec_body += "*No new or modified tests detected in this PR.*\n"
    except Exception as e:
        test_spec_body += f"*Failed to extract test specs: {e}*\n"
        
    sys.path.append('.')
    from skills.github_client import create_pr
    if is_green:
        title = f"[GREEN Node] Complete {node_id}"
        body = f"Automated PR update for Node {node_id} GREEN completion.\n\n{test_spec_body}"
    else:
        title = f"[RED Node] Intent Validation {node_id}"
        body = f"Automated PR for Node {node_id} RED Intent Validation.\n\n{test_spec_body}"
    
    pr_url = create_pr(title, body)
    print(f"[FLOW] PR successfully opened/updated at: {pr_url}")
    
    print("[FLOW] Synchronizing with remote GitHub Actions Pipeline (GAP)...")
    import time
    time.sleep(5) # Allow GitHub to register the PR and start workflows
    gap_result = subprocess.run("gh pr checks --watch", shell=True, capture_output=True, text=True)
    
    if is_green:
        if gap_result.returncode != 0:
            print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
            print("A structural CSI Guard was tripped: The remote GAP failed during the Green Phase!")
            print("This indicates a Survivor Bias split-brain (e.g. environmental drift).")
            sys.exit(1)
        print("[FLOW] Remote GAP successfully passed. Split-brain falsified.")
    else:
        if gap_result.returncode == 0:
            print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
            print("A structural CSI Guard was tripped: The remote GAP PASSED during the Red Phase!")
            print("Tests must fail in the remote environment to validate the Intent Gate.")
            sys.exit(1)
        print("[FLOW] Remote GAP successfully failed as expected. Split-brain falsified.")
    
    # 3. Transition DAG Status and Merge (if Green)
    if is_green:
        print(f"[FLOW] Executing Autonomous Merge for Green Phase...")
        run_cmd("gh pr merge --merge --delete-branch")
        run_cmd(f"python3 skills/frontier_editor.py {node_id} DONE")
        print(f"[FLOW] Node {node_id} status transitioned to DONE. Execution completed.")
    else:
        run_cmd(f"python3 skills/frontier_editor.py {node_id} IN_REVIEW")
        print(f"[FLOW] Node {node_id} status transitioned to IN_REVIEW. Execution halted pending Operator Approval.")

def complete_node(node_id, retro_msg):
    print(f"[FLOW] Executing CSI Guard (Test Suite) for Node {node_id} completion...")
    
    print("[FLOW] Asserting Mechanical UI Gate (Dialect Linter)...")
    linter_result = subprocess.run("python3 skills/dialect_linter.py", shell=True, capture_output=True, text=True)
    if linter_result.returncode != 0:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print(linter_result.stdout)
        print("The Agent must physically run the UI presentation tools. You are blocked from Completion.")
        sys.exit(1)
        
    # Enforce Testing Invariant
    sys.path.append('.')
    try:
        test_result = run_cmd("python3 skills/testing_harness.py", allow_fail=True)
        print(test_result)
    except Exception:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("TDD execution failed to run. You cannot complete an EXECUTE node without passing tests.")
        sys.exit(1)
        
    if "🚨" in test_result:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("A structural CSI Guard was tripped. You cannot complete this node.")
        sys.exit(1)
        
    if "FAIL" in test_result or "ERROR" in test_result:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("Tests failed. The Testing Invariant is violated. You are mechanically forbidden from closing this node.")
        sys.exit(1)
        
    print(f"[FLOW] Synthesis Invariant: Appending retro_msg to Ledger...")
    from skills import ledger_manager
    full_retro_msg = f"[{node_id}] {retro_msg}"
    ledger_manager.append_ledger("node-retro", full_retro_msg)
    run_cmd('git add DYAD_LEDGER.md dyad-state/ledger.jsonl && git commit -m "chore(ledger): retro synthesis for completion"')
        
    print(f"[FLOW] Tests passed mechanically. Transitioning Node {node_id} to DONE.")
    run_cmd(f"python3 skills/frontier_editor.py {node_id} DONE")

def trail_reflect(trail_id, retro_msg):
    print(f"[FLOW] Executing Trail Reflect for {trail_id}...")
    
    # 1. Synthesis Invariant
    sys.path.append('.')
    from skills import ledger_manager
    ledger_manager.append_ledger("trail-retro", retro_msg)
    
    # 2. Issue Closure Invariant
    # We call gh issue close to shut down the orchestrator's tracked task
    run_cmd(f"gh issue close {trail_id}")
    
    # 3. Trail Pruning Invariant
    run_cmd(f"python3 skills/frontier_editor.py {trail_id} PRUNE")
    
    print(f"[FLOW] Trail {trail_id} successfully closed and pruned.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 skills/flow_state_manager.py <plan|checkout|reflect-red|reflect-green|complete|trail-reflect> <node_id> [retro_msg]")
        sys.exit(1)
    
    check_retro_lock()
    check_sovereignty_trigger()
    check_audit_lock()
    
    # Assert outbox sync
    sys.path.append('.')
    try:
        from skills.sync_checker import check_outbox_sync
        check_outbox_sync()
    except Exception as e:
        if isinstance(e, SystemExit):
            sys.exit(e.code)
        pass

    action = sys.argv[1].lower()
    node = sys.argv[2]
    
    if action == "plan":
        plan_node(node)
    elif action == "checkout":
        checkout_node(node)
    elif action == "convert-todo":
        # Convert a parked todo into an injected node
        import yaml
        todo_yml = "artifacts/todos.yml"
        if not os.path.exists(todo_yml):
            print("ERROR: No todos holding pen found.")
            sys.exit(1)
            
        with open(todo_yml, "r") as f:
            todos = yaml.safe_load(f) or {}
            
        if "backlog" not in todos or node not in todos["backlog"]:
            print(f"ERROR: Todo ID {node} not found in holding pen.")
            sys.exit(1)
            
        intent = todos["backlog"][node]["intent"]
        
        # Inject the node
        node_id = f"node_todo_{node.split('_')[1]}"
        inject_node(node_id, f"Convert Todo: {node}", intent)
        
        # Remove from backlog
        del todos["backlog"][node]
        with open(todo_yml, "w") as f:
            yaml.dump(todos, f, default_flow_style=False, sort_keys=False)
            
        print(f"[TODO] Successfully converted {node} into {node_id} (IN_REVIEW).")
    elif action == "inject":
        if len(sys.argv) < 5:
            print("Usage: python3 skills/flow_state_manager.py inject <node_id> \"<Title>\" \"<Goal>\"")
            sys.exit(1)
        inject_node(node, sys.argv[3], sys.argv[4])
    elif action == "authorize":
        authorize_node(node)
    elif action == "reflect-red":
        reflect_node_red(node)
    elif action == "reflect-green":
        if len(sys.argv) < 4:
            print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
            print("A retro_msg synthesis block is mandatory for reflect-green.")
            sys.exit(1)
        reflect_node_green(node, sys.argv[3])
    elif action == "complete":
        if len(sys.argv) < 4:
            print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
            print("A retro_msg synthesis block is mandatory for complete.")
            sys.exit(1)
        complete_node(node, sys.argv[3])
    elif action == "trail-reflect":
        retro_msg = sys.argv[3] if len(sys.argv) > 3 else "No retro message provided."
        trail_reflect(node, retro_msg)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
