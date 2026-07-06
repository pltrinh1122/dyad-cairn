import sys, os, json, urllib.request, urllib.error

def get_token():
    token = os.environ.get("GITHUB_TOKEN")
    if token: return token
    try:
        with open(os.path.expanduser("~/.git-credentials"), "r") as f:
            for line in f:
                if "github.com" in line:
                    return line.split(":")[2].split("@")[0]
    except: pass
    return None

def main():
    args = sys.argv[1:]
    issue_number = None
    repo = None
    body = None
    
    for i, arg in enumerate(args):
        if arg.isdigit() and issue_number is None: issue_number = arg
        if arg == "--repo": repo = args[i+1]
        elif arg == "-R": repo = args[i+1]
        elif arg == "--body": body = args[i+1]
        elif arg == "-b": body = args[i+1]
        
    token = get_token()
    if not token:
        print("GITHUB_TOKEN not found.", file=sys.stderr)
        sys.exit(1)
        
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    data = json.dumps({"body": body}).encode("utf-8")
    print(f"URL: {url}")
    print(f"Token length: {len(token)}")
    req = urllib.request.Request(url, data=data, method="POST", headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json", "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            print(f"Created comment on issue #{issue_number}")
    except urllib.error.HTTPError as e:
        print(f"GitHub API Error: {e.code} {e.reason}", file=sys.stderr)
        print(e.read().decode("utf-8"), file=sys.stderr)
        sys.exit(1)

main()
