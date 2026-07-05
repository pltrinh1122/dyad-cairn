import sys
import subprocess
import os

os.environ["PATH"] = os.path.abspath("bin") + os.pathsep + os.environ.get("PATH", "")

def get_active_anchor():
    """Returns the name of the active platform anchor."""
    return "GEMINI.md"

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
    result = subprocess.run("bin/git -C commons grep -i '\\bstone\\.yaml\\b'", shell=True, capture_output=True, text=True)
    if result.returncode == 0 and result.stdout.strip():
        print("==========================================================================")
        print("🚨 SOVEREIGNTY TRIGGER FIRED 🚨")
        print("The Commons has formally adopted 'stone.yaml'. Local sovereignty is void.")
        print("Telemetry Exhaust:")
        print(result.stdout.strip())
        print("Any mutations to the mason schema must now be treated as external blockers.")
        print("[STEERING VECTOR] Synchronize with the Commons using `./bin/sync-commons` or pull upstream changes to resolve this blockage.")
        print("==========================================================================")
        # In a fully realized state, this might sys.exit(1) until Operator acknowledges.

def check_audit_lock():
    import yaml
    import os
    # Only enforce if we are operating on the Frontier DAG
    current_store = os.environ.get("DYAD_DAG_STORE", "artifacts/frontier_state.yml")
    if current_store != "artifacts/frontier_state.yml":
        return

    audit_dir = "artifacts/audit"
    if os.path.exists(audit_dir):
        failing_nodes = []
        for fname in sorted(os.listdir(audit_dir)):
            if fname.endswith(".yml"):
                try:
                    with open(os.path.join(audit_dir, fname), "r") as f:
                        data = yaml.safe_load(f) or {}
                        if "nodes" in data:
                            for node_id, node_data in data.get("nodes", {}).items():
                                if node_data.get("status") != "DONE":
                                    failing_nodes.append(node_id)
                        else:
                            for node_id, node_data in data.items():
                                if node_data.get("status") != "DONE":
                                    failing_nodes.append(node_id)
                except Exception:
                    pass
        if failing_nodes:
            print("==========================================================================")
            print("🚨 GOVERNANCE DEBT GUARDRAIL FIRED 🚨")
            print("The following Audit nodes are unresolved:")
            for n in failing_nodes:
                print(f"  - {n}")
            print("You are mechanically forbidden from transitioning the Frontier DAG until")
            print("the Audit DAG is physically cleared (all nodes DONE).")
            print("[STEERING VECTOR] The Audit DAG must be physically cleared (all nodes evaluated to DONE) before Frontier Execution can resume. The Agent must satisfy this invariant.")
            print("==========================================================================")
            sys.exit(1)

def session_start():
    print("[FLOW] Executing Session Start...")
    import yaml
    import fcntl
    os.makedirs("dyad-state", exist_ok=True)
    with open("dyad-state/fsm_state.yml", "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yaml.dump({"state": "session-start"}, f)
        fcntl.flock(f, fcntl.LOCK_UN)

def plan_node(node_id):
    print(f"[FLOW] Planning Node {node_id}...")
    print(f"[FLOW] Local DAG asserts planning. No remote issue required.")

def checkout_node(node_id):
    import os
    import sys
    sys.path.append('.')
    from skills.frontier_editor import load_state
    state = load_state()
    node = state.get("nodes", {}).get(node_id, {})
    requires = node.get("requires", [])
    
    if requires:
        print(f"[FLOW] Asserting Materialized Dependency Guard for {node_id}...")
        for req in requires:
            if not os.path.exists(req):
                print(f"🚨 CSI GUARD BLOCK: Pre-requisite '{req}' is missing from the physical substrate! 🚨")
                print(f"[FLOW] The DAG topological clearance is overridden. Execution is safely stalled.")
                sys.exit(1)
        print("[FLOW] Materialized Dependency Guard PASSED.")

    branch_name = f"active/{node_id}"
    print(f"[FLOW] Checking out branch and creating git worktree: {branch_name}")
    # Create the branch if it does not exist
    run_cmd(f"bin/git branch {branch_name} || true", allow_fail=True)
    worktree_path = f".worktrees/{branch_name.replace("/", "_")}"
    if not os.path.exists(worktree_path):
        run_cmd(f"bin/git worktree add {worktree_path} {branch_name}")
    else:
        print(f"[FLOW] Worktree {worktree_path} already exists. Skipping creation.")

def inject_node(node_id, title, goal, scope, bypass_review=False):
    print(f"[FLOW] Injecting Node {node_id} ({'AUTHORIZED' if bypass_review else 'IN_REVIEW'})...")
    sys.path.append('.')
    from skills.frontier_editor import load_state, save_state
    state = load_state()
    if node_id in state["nodes"]:
        print(f"ERROR: Node {node_id} already exists.")
        sys.exit(1)
        
    node_type = "PROBE" if "probe" in node_id else "PLAN"
    state["nodes"][node_id] = {
        "title": title,
        "goal": goal,
        "type": node_type,
        "scope": scope
    }
    
    gates = state.get("config", {}).get("gates", {})
    if bypass_review:
        state["nodes"][node_id]["status"] = "AUTHORIZED"
    elif gates.get("design_review", True):
        state["nodes"][node_id]["status"] = "IN_REVIEW"
    save_state(state)
    
    if state["nodes"][node_id].get("status") == "IN_REVIEW":
        print(f"[FLOW] Node {node_id} successfully injected and blocked at the Design-Review Gate.")
        sys.path.append('.')
        from skills.design_review_ui import present_design_review
        present_design_review(node_id, state)
    else:
        print(f"[FLOW] Node {node_id} successfully injected (Design-Review Gate bypassed/disabled).")

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
        
    state["nodes"][node_id]["status"] = "AUTHORIZED"
    save_state(state)
    print(f"[FLOW] Node {node_id} transitioned to AUTHORIZED. Added to Goal-Ready Queue.")
    checkout_node(node_id)

def reflect_node_red(node_id):
    print(f"[FLOW] Reflecting RED Phase (Intent Gate) for Node {node_id}...")
    print("[FLOW] Asserting Mechanical Gate (TDD must FAIL)...")
    sys.path.append('.')
    try:
        from skills.testing_harness import run_tests
        test_result = run_cmd("python3 skills/testing_harness.py", allow_fail=True)
    except Exception as e:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("TDD execution threw an unhandled exception. Fix syntax errors before reflecting red.")
        print("[STEERING VECTOR] The Testing Invariant requires valid, syntactically correct Python. Run 'python3 skills/testing_harness.py' to isolate and resolve compile-time and import errors.")
        sys.exit(1)
        
    if "🚨" in test_result:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("A structural CSI Guard was tripped during the Red Phase.")
        print("You are mechanically forbidden from generating an Intent PR until the substrate is physically unblocked.")
        print("[STEERING VECTOR] A structural CSI Guard remains actively tripped in the environment. Run 'python3 skills/testing_harness.py' to read the guard message and perform the required remediation.")
        sys.exit(1)
        
    if "FAIL" not in test_result:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("Tests PASSED in the Red phase. You must write failing tests that map to Operator intent before reflecting.")
        print("[STEERING VECTOR] The Intent Gate invariant requires the presence of at least one failing test. Run 'python3 skills/testing_harness.py' to verify the failure after writing it.")
        sys.exit(1)
        
    create_reflection_pr(node_id, is_green=False)

def reflect_node_green(node_id, retro_msg):
    print(f"[FLOW] Reflecting GREEN Phase (Mechanical Gate) for Node {node_id}...")
    print("[FLOW] Asserting Mechanical UI Gate (Dialect Linter)...")
    linter_result = subprocess.run("python3 skills/dialect_linter.py", shell=True, capture_output=True, text=True)
    if linter_result.returncode != 0:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("The Agent must physically run the UI presentation tools. You are blocked.")
        print("[STEERING VECTOR] The Mechanical UI Gate requires all files to pass the Dialect Linter. Run 'python3 skills/dialect_linter.py' to isolate and resolve all formatting violations.")
        sys.exit(1)
        
    if "_execute_" in node_id:
        rca_file = f"artifacts/rca_{node_id}.md"
        if not os.path.exists(rca_file):
            print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
            print(f"Missing RCA artifact. EXECUTE nodes must author an industry standard RCA at '{rca_file}'.")
            print(f"[STEERING VECTOR] Create the file `{rca_file}` detailing the Root Cause Analysis, then rerun.")
            sys.exit(1)

    print("[FLOW] Asserting Mechanical Gate (TDD must PASS)...")
    sys.path.append('.')
    try:
        from skills.testing_harness import run_tests
        test_result = run_cmd("python3 skills/testing_harness.py", allow_fail=True)
    except Exception as e:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("TDD execution failed. The PR Gate is mechanically sealed until tests pass.")
        print("[STEERING VECTOR] The PR Gate requires the test suite to execute successfully. Run 'python3 skills/testing_harness.py' to isolate syntax or runtime harness errors.")
        sys.exit(1)
        
    if "🚨" in test_result:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("A structural CSI Guard was tripped during the Green Phase.")
        print("You are mechanically forbidden from generating a Green PR until the substrate is physically unblocked.")
        print("[STEERING VECTOR] A structural CSI Guard is actively blocking the Green Phase. Run 'python3 skills/testing_harness.py' to read the guard message and satisfy the invariant.")
        sys.exit(1)
        
    if "FAIL" in test_result:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("Tests failed. You are mathematically forbidden from generating a Green PR.")
        print("[STEERING VECTOR] The Mechanical Gate invariant requires 100% test passage. Run 'python3 skills/testing_harness.py' to extract and fix all failing assertions.")
        sys.exit(1)
        
    print(f"[FLOW] Synthesis Invariant: Appending retro_msg to Ledger...")
    from skills import ledger_manager
    full_retro_msg = f"[{node_id}] {retro_msg}"
    ledger_manager.append_ledger("node-retro", full_retro_msg)
    
    # Commit the ledger before generating the PR so it's included in the execution payload
    run_cmd('bin/git add DYAD_LEDGER.md dyad-state/ledger.jsonl && bin/git commit -m "chore(ledger): retro synthesis for green phase"')
    
    create_reflection_pr(node_id, is_green=True)

def create_reflection_pr(node_id, is_green):
    # 1. Push branch to remote
    # Get current branch
    branch = run_cmd("bin/git rev-parse --abbrev-ref HEAD")
    print(f"[FLOW] Pushing branch {branch} to remote...")
    run_cmd(f"bin/git push -u origin {branch}")
    
    # 2. Open Pull Request
    print("[FLOW] Generating Pull Request...")
    
    # Extract Test Spec for PR Body
    test_spec_body = "### Operator Validation Spec (The Tests)\n\n"
    try:
        import ast
        import os
        # Find test files modified in this branch compared to main
        diff_files = run_cmd("bin/git diff --name-only main...HEAD").splitlines()
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
        
    try:
        from skills.frontier_editor import load_state
        from skills.frontier_reader import build_tree
        state = load_state()
        tree_lines = build_tree(state.get('nodes', {}))
        dag_tree = "### Computed Frontier DAG (Ephemeral Snapshot)\n```text\n" + "\n".join(tree_lines) + "\n```\n"
    except Exception as e:
        dag_tree = f"*Failed to compute DAG snapshot: {e}*\n"
        
    sys.path.append('.')
    from skills.github_client import create_pr
    
    body_appendix = f"\n{test_spec_body}\n{dag_tree}"
    if is_green:
        title = f"[GREEN Node] Complete {node_id}"
        body = f"Automated PR update for Node {node_id} GREEN completion.{body_appendix}"
    else:
        title = f"[RED Node] Intent Validation {node_id}"
        body = f"Automated PR for Node {node_id} RED Intent Validation.{body_appendix}"
    
    pr_url = create_pr(title, body)
    print(f"[FLOW] PR successfully opened/updated at: {pr_url}")
    
    print("[FLOW] Synchronizing with remote GitHub Actions Pipeline (GAP)...")
    import time
    time.sleep(15) # Allow GitHub to register the PR and start workflows
    
    for _ in range(6):
        gap_result = subprocess.run("bin/gh pr checks --watch", shell=True, capture_output=True, text=True)
        if gap_result.returncode != 0 and "no checks reported" in (gap_result.stdout + gap_result.stderr):
            print("[FLOW] GAP not yet registered by GitHub. Retrying in 10s...")
            time.sleep(10)
        else:
            break
    
    if gap_result.returncode != 0:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print(f"A structural CSI Guard was tripped: The remote GAP failed during the {'Green' if is_green else 'Red'} Phase!")
        print("Telemetry Exhaust:")
        print(gap_result.stdout)
        print(gap_result.stderr)
        print("This indicates a Survivor Bias split-brain (e.g. environmental drift).")
        print("[STEERING VECTOR] The Intent Gate requires the remote GAP environment to actively pass. The Agent must satisfy this invariant before advancing.")
        sys.exit(1)
    print("[FLOW] Remote GAP successfully passed. Split-brain falsified.")
    
    # 3. Transition DAG Status and Merge (if Green)
    if is_green:
        print(f"[FLOW] Executing Autonomous Merge for Green Phase...")
        run_cmd("bin/gh pr merge --merge --delete-branch", allow_fail=True)
        run_cmd(f"python3 skills/frontier_editor.py {node_id} DONE")
        print(f"[FLOW] Node {node_id} status transitioned to DONE. Execution completed.")
    else:
        run_cmd(f"python3 skills/frontier_editor.py {node_id} IN_REVIEW")
        print(f"[FLOW] Node {node_id} status transitioned to IN_REVIEW. Execution halted pending Operator Approval.")

def process_retro(summary, css_path=None):
    if not css_path:
        print("Usage: ./bin/retro <summary> <path/to/retro.md>")
        print("ERROR: CSS Template (path/to/retro.md) is strictly mandatory to fulfill the Cognitive State Synchronization invariant.")
        sys.exit(1)
        
    linter_result = subprocess.run(f"python3 skills/retro_linter.py \"{css_path}\"", shell=True, capture_output=False, text=False)
    if linter_result.returncode != 0:
        print("🚨 CSI GUARDRAIL BLOCK: Retro does not match CSS template.")
        print("[STEERING VECTOR] Format the retro message to exactly match the mechanical UI presentation template, then rerun.")
        sys.exit(1)
        
    subprocess.run(f"python3 skills/ledger_manager.py retro \"{summary}\" \"{css_path}\"", shell=True, capture_output=False, text=False)

def process_d_start():
    print("[FLOW] Executing Start-Session Discipline (d-start)...")
    import os
    import yaml
    
    cf_path = "dyad-state/carry-forward.md"
    if os.path.exists(cf_path):
        print("==========================================================================")
        print("📦 CARRY-FORWARD STATE DETECTED")
        with open(cf_path, "r") as f:
            print(f.read().strip())
        print("==========================================================================")
    else:
        print("[FLOW] No carry-forward state detected.")

    print("[FLOW] Pushing FSM into session-start state...")
    os.makedirs("dyad-state", exist_ok=True)
    with open("dyad-state/fsm_state.yml", "w") as f:
        yaml.dump({"state": "session-start"}, f)

def process_d_reflect(summary, css_path, carry_forward_note):
    """`d-reflect` — adopted from dyad-bond's CSS+OR discipline (github.com/pltrinh1122/dyad-bond,
    kb/reflection-discipline.md). One token doing two jobs, same reasoning bond collapsed
    `reflect`/`stand-down` into: every CSS retro here was already paired with a resume-prep note,
    so it's one job, not two. Fires the existing CSS retro flow, then updates
    dyad-state/carry-forward.md so the next SESSION_START has live in-flight state to read."""
    process_retro(summary, css_path)
    subprocess.run(f"python3 skills/ledger_manager.py carry-forward \"{carry_forward_note}\"", shell=True, capture_output=False, text=False)

def process_d_land(carry_forward_note):
    """`d-land` — serializes arc state without a full session retro.
    Used for intra-session state captures or transitions where a formal 
    retro isn't necessary, but state needs to be persisted to carry-forward."""
    print("[FLOW] Executing Arc Land Discipline (d-land)...")
    
    import os
    import yaml
    import subprocess
    
    todo_dir = "artifacts/todos"
    todo_list = ""
    if os.path.exists(todo_dir):
        todos = [f for f in sorted(os.listdir(todo_dir)) if f.endswith('.yml')]
        if todos:
            todo_list = "\n\n**Pending Todos (Handoff):**\n"
            for t in todos:
                try:
                    with open(os.path.join(todo_dir, t), "r") as f_todo:
                        data = yaml.safe_load(f_todo) or {}
                        todo_id = t.replace('.yml', '')
                        intent = data.get(todo_id, {}).get("raw_thought", data.get(todo_id, {}).get("intent", ""))
                        todo_list += f"- **{todo_id}**: {intent}\n"
                except Exception as e:
                    print(f"[FLOW] Warning: failed to parse todo {t}: {e}")
                    
    final_note = carry_forward_note + todo_list
    
    # Use list format to safely pass multiline/quoted strings
    subprocess.run(["python3", "skills/ledger_manager.py", "carry-forward", final_note], check=False)
    
    os.makedirs("dyad-state", exist_ok=True)
    with open("dyad-state/fsm_state.yml", "w") as f:
        yaml.dump({"state": "arc-land"}, f)
    print("[FLOW] Pushed FSM into 'arc-land' state.")

def complete_node(node_id, retro_msg):
    print(f"[FLOW] Executing CSI Guard (Test Suite) for Node {node_id} completion...")
    
    print("[FLOW] Asserting Physical Merge Invariant...")
    branch = run_cmd("bin/git rev-parse --abbrev-ref HEAD", allow_fail=True).strip()
    if branch != "main":
        import json
        pr_view = run_cmd("bin/gh pr view --json state", allow_fail=True)
        if "no pull requests found" in pr_view.lower():
            print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
            print("You cannot complete a node without an active Pull Request.")
            sys.exit(1)
        
        try:
            pr_view_clean = pr_view[pr_view.find("{"):] if "{" in pr_view else pr_view
            pr_data = json.loads(pr_view_clean)
            if pr_data.get("state") != "MERGED":
                print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
                print(f"PR is not MERGED (current state: {pr_data.get('state')}).")
                print("[STEERING VECTOR] Resolve merge conflicts or wait for CI to pass, then merge the PR before completing the node.")
                sys.exit(1)
        except Exception as e:
            print(f"🚨 CONSISTENCY GUARDRAIL FIRED 🚨\nFailed to parse PR state: {e}\nOutput was: {pr_view}")
            sys.exit(1)
            
        #checks_output = run_cmd("bin/gh pr checks", allow_fail=True)
        #if "fail" in checks_output.lower():
        #    print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        #    print("PR CI checks have failed. The state cannot advance.")
        #    sys.exit(1)
    
    print("[FLOW] Asserting Mechanical UI Gate (Dialect Linter)...")
    linter_result = subprocess.run("python3 skills/dialect_linter.py", shell=True, capture_output=True, text=True)
    if linter_result.returncode != 0:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("The Agent must physically run the UI presentation tools. You are blocked from Completion.")
        print("[STEERING VECTOR] The Mechanical UI Gate requires all files to pass the Dialect Linter. Run 'python3 skills/dialect_linter.py' to isolate and resolve all formatting violations.")
        sys.exit(1)
        
    if "_execute_" in node_id:
        rca_file = f"artifacts/rca_{node_id}.md"
        if not os.path.exists(rca_file):
            print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
            print(f"Missing RCA artifact. EXECUTE nodes must author an industry standard RCA at '{rca_file}'.")
            print(f"[STEERING VECTOR] Create the file `{rca_file}` detailing the Root Cause Analysis, then rerun.")
            sys.exit(1)

    # Enforce Testing Invariant
    sys.path.append('.')
    try:
        test_result = run_cmd("python3 skills/testing_harness.py", allow_fail=True)
    except Exception:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("TDD execution failed to run. You cannot complete an EXECUTE node without passing tests.")
        print("[STEERING VECTOR] The PR Gate requires the test suite to execute successfully. Run 'python3 skills/testing_harness.py' to isolate syntax or runtime harness errors.")
        sys.exit(1)
        
    if "🚨" in test_result:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("A structural CSI Guard was tripped. You cannot complete this node.")
        print("[STEERING VECTOR] A structural CSI Guard is actively blocking the Green Phase. Run 'python3 skills/testing_harness.py' to read the guard message and satisfy the invariant.")
        sys.exit(1)
        
    if "FAIL" in test_result or "ERROR" in test_result:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("Tests failed. The Testing Invariant is violated. You are mechanically forbidden from closing this node.")
        print("[STEERING VECTOR] The Mechanical Gate invariant requires 100% test passage. Run 'python3 skills/testing_harness.py' to extract and fix all failing assertions.")
        sys.exit(1)
        
    print(f"[FLOW] Synthesis Invariant: Appending retro_msg to Ledger...")
    from skills import ledger_manager
    full_retro_msg = f"[{node_id}] {retro_msg}"
    ledger_manager.append_ledger("node-retro", full_retro_msg)
    print(f"[FLOW] Tests passed mechanically. Transitioning Node {node_id} to DONE.")
    run_cmd(f"python3 skills/frontier_editor.py {node_id} DONE")
    
    if "node_todo_" in node_id:
        todo_id = node_id.replace("node_", "")
        todo_file = f"artifacts/todos/{todo_id}.yml"
        if os.path.exists(todo_file):
            os.remove(todo_file)
            print(f"[FLOW] Cleaned up completed todo file: {todo_file}")
    
    # 4. Automatic Decomposition for PROBE nodes
    if "_probe_" in node_id or node_id.endswith("_probe"):
        probe_file = f"artifacts/{node_id}.md"
        if os.path.exists(probe_file):
            with open(probe_file, "r") as f:
                content = f.read()
            import re
            decomp_match = re.search(r"(?im)^##\s+.*?Decomposition.*?\n(.*?)(?=\n##\s|\Z)", content, re.DOTALL)
            if decomp_match:
                print(f"[FLOW] Automatic Decomposition triggered for {node_id}...")
                sys.path.append('.')
                from skills.frontier_editor import load_state
                state = load_state()
                parent_scope = state.get("nodes", {}).get(node_id, {}).get("scope", "FRONTIER")
                lines = decomp_match.group(1).strip().split('\n')
                for line in lines:
                    m = re.match(r"^\-\s+\*\*(node_[0-9a-z_]+)\*\*\:\s+(.*)$", line.strip())
                    if m:
                        new_node_id = m.group(1)
                        goal = m.group(2).strip('"\'')
                        print(f"       -> Injecting {new_node_id} [{parent_scope}]")
                        inject_node(new_node_id, f"Decomposed from {node_id}", goal, parent_scope)
    
    # Finally, commit the ledger and any state file deletions (e.g. artifacts/)
    run_cmd('bin/git add -u artifacts/ && bin/git add DYAD_LEDGER.md dyad-state/ledger.jsonl && bin/git commit -m "chore(ledger): retro synthesis for completion"', allow_fail=True)

def trail_reflect(trail_id, retro_msg=None):
    print(f"[FLOW] Executing Trail Reflect for {trail_id}...")
    
    # 1. Synthesis Invariant
    sys.path.append('.')
    from skills import ledger_manager
    from skills.github_client import create_pr
    
    synthesis_file = f"artifacts/trail_synthesis_{trail_id}.md"
    if not os.path.exists(synthesis_file):
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print(f"Missing Trail Synthesis artifact. REFLECT nodes must author '{synthesis_file}'.")
        print(f"[STEERING VECTOR] Create the file `{synthesis_file}` with the required synthesis narrative, then rerun.")
        sys.exit(1)
        
    with open(synthesis_file, "r") as f:
        retro_msg = f.read()
        
    if "Probe Invariant" not in retro_msg or "Execution RCA" not in retro_msg:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("Trail Synthesis must contain a narrative summary for (1) positive assertion of the Probe Invariant and (2) reference to individual Execution RCA.")
        print("[STEERING VECTOR] Update the trail synthesis document to include both the Probe Invariant assertion and references to the Execution RCAs, then rerun.")
        sys.exit(1)
    
    branch_name = f"active/reflect_{trail_id}"
    run_cmd(f"bin/git checkout -b {branch_name} || bin/git checkout {branch_name}")
    
    full_retro_msg = retro_msg
    if f"[{trail_id}]" not in full_retro_msg:
        full_retro_msg = f"[{trail_id}]\n{retro_msg}"
    ledger_manager.append_ledger("trail-retro", full_retro_msg)
    
    # Commit and Push
    run_cmd("bin/git add dyad-state/ledger.jsonl DYAD_LEDGER.md")
    run_cmd(f'bin/git commit -m "docs(ledger): [REFLECT] trail synthesis for {trail_id}"')
    run_cmd(f"bin/git push origin {branch_name}")
    
    # 2. Reflection Review Gate
    title = f"[REFLECT] Trail Synthesis {trail_id}"
    body = f"Automated PR for Trail {trail_id} Synthesis.\n\n{retro_msg}\n\nReview this artifact. Run `./bin/node dispose {trail_id}` to merge and prune."
    pr_url = create_pr(title, body)
    
    print(f"[FLOW] PR successfully opened at: {pr_url}")
    print(f"[FLOW] Trail {trail_id} halted pending Reflection Review. Run `./bin/node dispose {trail_id}` to finalize.")

def trail_dispose(trail_id):
    print(f"[FLOW] Executing Trail Dispose for {trail_id}...")
    
    # 1. Merge PR
    run_cmd("bin/gh pr merge --merge --delete-branch", allow_fail=True)
    
    # 2. Issue Closure Invariant
    # This may fail if the node is a PROBE and was never synced to a GitHub issue.
    # We suppress the error to ensure the DAG is pruned correctly.
    run_cmd(f"bin/gh issue close {trail_id}", allow_fail=True)
    
    # 3. Trail Pruning Invariant
    run_cmd(f"python3 skills/frontier_editor.py {trail_id} PRUNE")
    
    print(f"[FLOW] Trail {trail_id} successfully disposed, merged, and pruned.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 skills/flow_state_manager.py <action> ...")
        sys.exit(1)
        
    action = sys.argv[1].lower()
    
    if action == "session-start":
        session_start()
        sys.exit(0)

    if action == "session-end":
        print("[FLOW] Pushing FSM into session-end state...")
        import yaml
        os.makedirs("dyad-state", exist_ok=True)
        with open("dyad-state/fsm_state.yml", "w") as f:
            yaml.dump({"state": "session-end"}, f)
        sys.exit(0)

    if action == "d-start":
        process_d_start()
        sys.exit(0)

    if action == "d-reflect":
        if len(sys.argv) < 5:
            print("Usage: python3 skills/flow_state_manager.py d-reflect <summary> <path/to/retro.md> <carry-forward-note>")
            sys.exit(1)
        process_d_reflect(sys.argv[2], sys.argv[3], sys.argv[4])
        sys.exit(0)

    if action == "d-land":
        if len(sys.argv) < 3:
            print("Usage: python3 skills/flow_state_manager.py d-land <carry-forward-note>")
            sys.exit(1)
        process_d_land(sys.argv[2])
        sys.exit(0)

    if len(sys.argv) < 3:
        print("Usage: python3 skills/flow_state_manager.py <action> <node_id> [args]")
        sys.exit(1)

    if action != "retro":
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
    node = sys.argv[2]
    
    if action == "plan":
        plan_node(node)
    elif action == "checkout":
        checkout_node(node)
    elif action == "convert-todo":
        if len(sys.argv) < 3:
            print("Usage: python3 skills/flow_state_manager.py convert-todo <todo_id>")
            sys.exit(1)
            
        # Convert a parked todo into an injected node
        import yaml
        todo_file = f"artifacts/todos/{node}.yml"
        if not os.path.exists(todo_file):
            print(f"ERROR: Todo ID {node} not found.")
            sys.exit(1)
            
        with open(todo_file, "r") as f:
            data = yaml.safe_load(f) or {}
            
        todo = data.get(node, {})
        if todo.get("status") != "RUBBED":
            print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
            print("The intent has not been fully refined.")
            print("[STEERING VECTOR] The Intent Gate requires the Rub Matrix to be fully populated. The Agent must complete the Rub phase with the Operator using `./bin/rub` before conversion.")
            sys.exit(1)
            
        intent = todo.get("raw_thought", todo.get("intent", ""))
        scope = todo["rub_matrix"]["scope"].upper()
        if scope not in ["FRONTIER", "INTEGRITY", "SUBSTRATE"]:
            print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
            print(f"Invalid scope '{scope}' in Rub Matrix.")
            print("[STEERING VECTOR] The Intent Gate requires the Scope to be one of FRONTIER, INTEGRITY, SUBSTRATE. Use `./bin/rub` to correct the scope.")
            sys.exit(1)
            
        goal = f"{intent}\n\nWHAT: {todo['rub_matrix']['what']}\nWHY: {todo['rub_matrix']['why']}"
        
        # Inject the node
        node_id = f"node_todo_{node.split('_')[1]}"
        node_title = todo['rub_matrix'].get('what') or intent
        inject_node(node_id, node_title, goal, scope, bypass_review=True)
        
        # Remove from backlog
        os.remove(todo_file)
            
        print(f"[TODO] Successfully converted {node} into {node_id} (AUTHORIZED) with scope [{scope}].")
    elif action == "inject":
        if len(sys.argv) < 6:
            print("Usage: python3 skills/flow_state_manager.py inject <node_id> \"<Title>\" \"<Goal>\" <SCOPE>")
            sys.exit(1)
        scope = sys.argv[5].upper()
        if scope not in ["FRONTIER", "INTEGRITY", "SUBSTRATE"]:
            print(f"ERROR: Invalid scope '{scope}'. Must be one of FRONTIER, INTEGRITY, SUBSTRATE.")
            sys.exit(1)
        inject_node(node, sys.argv[3], sys.argv[4], scope)
    elif action == "authorize":
        authorize_node(node)
    elif action == "reflect-red":
        reflect_node_red(node)
    elif action == "reflect-green":
        if len(sys.argv) < 4:
            print("Usage: python3 skills/flow_state_manager.py reflect-green <node_id> <retro_msg>")
            sys.exit(1)
        reflect_node_green(node, sys.argv[3])
    elif action == "complete":
        if len(sys.argv) < 4:
            print("Usage: python3 skills/flow_state_manager.py complete <node_id> <retro_msg>")
            sys.exit(1)
        complete_node(node, sys.argv[3])
    elif action == "trail-reflect":
        msg = sys.argv[3] if len(sys.argv) > 3 else None
        trail_reflect(node, msg)
    elif action == "design-review":
        sys.path.append('.')
        from skills.design_review_ui import present_design_review
        from skills.frontier_editor import load_state
        state = load_state()
        present_design_review(node, state)
    elif action == "dispose":
        trail_dispose(node)
    elif action == "retro":
        # retro doesn't use node_id, so sys.argv[2] is summary and sys.argv[3] is path
        if len(sys.argv) < 4:
            print("Usage: python3 skills/flow_state_manager.py retro <summary> <path/to/retro.md>")
            sys.exit(1)
        process_retro(sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

def set_active_anchor(state_name, anchor_path="dyad-state/active_anchor"):
    import os
    if os.path.lexists(anchor_path):
        os.remove(anchor_path)
    with open(anchor_path, "w") as f:
        f.write(state_name)
