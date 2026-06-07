import sys
import subprocess
import json

def run_gh_cmd(args):
    cmd = ["gh"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: GitHub API failed: {result.stderr}")
        sys.exit(1)
    return result.stdout

def fetch_open_issues():
    out = run_gh_cmd(["issue", "list", "--state", "open", "--json", "number,title,state,url"])
    return json.loads(out)

def create_issue(title, body):
    out = run_gh_cmd(["issue", "create", "--title", title, "--body", body])
    return out.strip()

def view_issue(issue_id):
    out = run_gh_cmd(["issue", "view", str(issue_id)])
    return out

def create_pr(title, body):
    cmd = ["gh", "pr", "create", "--title", title, "--body", body]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        if "already exists" in result.stderr:
            # Extract the URL from stderr
            lines = result.stderr.strip().split('\n')
            return lines[-1]
        print(f"ERROR: GitHub API failed: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def create_repo(repo_name, public=True, push=True):
    cmd = ["gh", "repo", "create", repo_name]
    if public:
        cmd.append("--public")
    else:
        cmd.append("--private")
    cmd.append("--source=.")
    cmd.append("--remote=origin")
    if push:
        cmd.append("--push")
        
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to create repo: {result.stderr}", file=sys.stderr)
        return False
    print(f"Success: {result.stdout}")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        import argparse
        parser = argparse.ArgumentParser(description="GitHub client wrapper")
        parser.add_argument("action", choices=["create"], help="Action to perform")
        parser.add_argument("--name", required=True, help="Repository name")
        args = parser.parse_args()
        
        if args.action == "create":
            success = create_repo(args.name)
            sys.exit(0 if success else 1)
    else:
        print("This is a stateless skill module for GitHub API. Do not run directly without arguments.")
