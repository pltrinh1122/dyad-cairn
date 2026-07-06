import os
import sys
import yaml
import subprocess
import re

def get_current_branch():
    dyad_cairn_path = os.environ.get("DYAD_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        res = subprocess.run(["/usr/bin/git", "-C", dyad_cairn_path, "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
        return res.stdout.strip()
    except:
        return ""

def load_frontier_state():
    # Attempt to load frontier state if it exists
    dyad_cairn_path = os.environ.get("DYAD_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(dyad_cairn_path, "artifacts", "frontier_state.yml")
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return yaml.safe_load(f) or {}
        except:
            return {}
    return {}

def enforce_git_action(args):
    # If the user is trying to push or commit, we check permissions
    # We allow safe commands like status, log, diff, checkout.
    if len(args) == 0:
        return True

    command = args[0]
    if command not in ["commit", "push", "add", "rm"]:
        return True

    # Level 2 Context by State Injection
    # We read dyad-state/fsm_state.yml and active node to determine context.
    dyad_cairn_path = os.environ.get("DYAD_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fsm_state_path = os.path.join(dyad_cairn_path, "dyad-state", "fsm_state.yml")
    active_state = "unknown"
    if os.path.exists(fsm_state_path):
        try:
            with open(fsm_state_path, "r") as f:
                data = yaml.safe_load(f) or {}
                active_state = data.get("state", "unknown")
        except:
            pass

    # Determine if we are working on a frontier node
    branch = get_current_branch()
    is_frontier_node = False
    active_node_scope = None
    if branch.startswith("active/node_"):
        frontier_state = load_frontier_state()
        node_id = branch.split("/")[1]
        node_data = frontier_state.get("nodes", {}).get(node_id, {})
        active_node_scope = node_data.get("scope")
        if active_node_scope == "FRONTIER":
            is_frontier_node = True

    cwd = os.getcwd()

    if cwd.startswith(dyad_cairn_path):
        # Internal substrate: if scope is FRONTIER, warn them if they are modifying internal state?
        # For now, allow internal modifications if we are in internal repo, as it might be tooling updates.
        return True

    # If we are outside dyad-cairn, we are in a Neutral Quarry.
    if not is_frontier_node:
        print("🚨 DYAD SANDBOX GUARD (Context Mismatch):")
        print("You are attempting to modify an external Neutral Quarry, but your active state is not a FRONTIER node.")
        print(f"Current State: {active_state} | Active Branch: {branch} | Scope: {active_node_scope}")
        print("[STEERING VECTOR] Finish or park the active internal node first before working on external commissions.")
        return False
    # A Neutral Quarry has a README.md defining layout.
    readme_path = os.path.join(cwd, "README.md")
    if not os.path.exists(readme_path):
        # We might be in a subdirectory. Let's find the root.
        repo_root = cwd
        try:
            res = subprocess.run(["/usr/bin/git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
            if res.returncode == 0:
                repo_root = res.stdout.strip()
                readme_path = os.path.join(repo_root, "README.md")
        except:
            pass

    if not os.path.exists(readme_path):
        print("🚨 DYAD SANDBOX GUARD: You are executing outside dyad-cairn but no Neutral Quarry README.md was found.")
        return False

    # Parse README.md layout
    # Layout looks like:
    # | path | owner | holds |
    # |---|---|---|
    # | `REQUIREMENTS.md` | Commissioner / dyad-bond | ...
    # | `SPECIFICATION.md` | Prime-Commissionee / dyad-cairn | ...
    ownership = {}
    with open(readme_path, "r") as f:
        content = f.read()
        in_layout = False
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("| path | owner"):
                in_layout = True
                continue
            if in_layout and line.startswith("|---"):
                continue
            if in_layout and line.startswith("|"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 3:
                    path = parts[1].replace("`", "")
                    owner = parts[2]
                    ownership[path] = owner
            elif in_layout and not line.strip():
                in_layout = False

    # What files are being modified?
    # For 'add' or 'commit', we can check the git status or the specific files passed.
    modified_files = []
    if command == "add":
        modified_files = args[1:]
    elif command == "commit" or command == "push":
        # Check staged files
        try:
            res = subprocess.run(["/usr/bin/git", "diff", "--name-only", "--cached"], capture_output=True, text=True)
            if res.returncode == 0:
                modified_files = [f for f in res.stdout.strip().splitlines() if f]
        except:
            pass

    for f in modified_files:
        # Ignore arguments like -m, --all, etc.
        if f.startswith("-"):
            continue
        
        # Check ownership
        file_path_clean = f.lstrip("./")
        # Match against ownership rules
        allowed = False
        for rule_path, owner in ownership.items():
            if rule_path.endswith("/"):
                if file_path_clean.startswith(rule_path):
                    if "dyad-cairn" in owner:
                        allowed = True
                        break
            else:
                if file_path_clean == rule_path:
                    if "dyad-cairn" in owner:
                        allowed = True
                        break

        # By default, files not explicitly in layout are denied to enforce strict mapping, 
        # unless they are untracked scratch files not being committed. But if they are being added, deny.
        # Actually, let's just warn for now if it's not strictly allowed.
        if not allowed:
            print(f"🚨 DYAD SANDBOX GUARD (ABAC Policy Deny):")
            print(f"Context: External Commission Quarry")
            print(f"Resource: {file_path_clean}")
            print(f"Action: {command}")
            print(f"Reason: Ownership mapping in README.md does not grant dyad-cairn access to this path.")
            print(f"[STEERING VECTOR] Revert changes to unauthorized files. You may only modify files assigned to dyad-cairn.")
            return False

    return True

def enforce_gh_action(args):
    if not args:
        return True

    command = args[0]
    allowed_commands = ["issue", "comment", "pr", "auth"]
    
    if command in allowed_commands:
        print(f"[FLOW] Sandbox Guard: gh {command} formally allowed across repositories.")
        return True
        
    print(f"🚨 DYAD SANDBOX GUARD (Context Deny):")
    print(f"You are attempting to execute an unauthorized gh command '{command}'.")
    print("[STEERING VECTOR] Only gh-issue and gh-comment mutations are formally allowed across repository boundaries.")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(0)
    
    action_type = sys.argv[1]
    
    if action_type == "git":
        allowed = enforce_git_action(sys.argv[2:])
        if not allowed:
            sys.exit(1)
            
    if action_type == "gh":
        allowed = enforce_gh_action(sys.argv[2:])
        if not allowed:
            sys.exit(1)
    
    sys.exit(0)
