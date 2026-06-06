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

if __name__ == "__main__":
    print("This is a stateless skill module for GitHub API. Do not run directly.")
