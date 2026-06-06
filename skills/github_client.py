import subprocess
import sys

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
    import argparse
    parser = argparse.ArgumentParser(description="GitHub client wrapper")
    parser.add_argument("action", choices=["create"], help="Action to perform")
    parser.add_argument("--name", required=True, help="Repository name")
    args = parser.parse_args()
    
    if args.action == "create":
        success = create_repo(args.name)
        sys.exit(0 if success else 1)
