import os
import subprocess
import tempfile
import re

def parse_locator(yaml_content):
    name_match = re.search(r'^name:\s*(.+)$', yaml_content, re.MULTILINE)
    locator_match = re.search(r'^locator:\s*(.+)$', yaml_content, re.MULTILINE)
    
    if name_match and locator_match:
        return name_match.group(1).strip().strip('"\''), locator_match.group(1).strip().strip('"\'')
    return None, None

def poll_mail(directory_path, target_dyad="dyad-cairn"):
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist.")
        return

    for filename in os.listdir(directory_path):
        if not filename.endswith('.yaml'):
            continue
            
        filepath = os.path.join(directory_path, filename)
        with open(filepath, 'r') as f:
            content = f.read()
            
        name, locator = parse_locator(content)
        if not name or not locator:
            continue
            
        # Format the locator
        if not locator.startswith("http"):
            locator = f"https://{locator}"
            
        # Clone into a temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            clone_dir = os.path.join(tmpdir, name)
            
            # Shallow clone
            print(f"Polling {name} from {locator}...")
            result = subprocess.run(
                ["git", "clone", "--depth", "1", locator, clone_dir],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"Failed to clone {name}: {result.stderr}")
                continue
                
            # Check for mail addressed to us
            mail_dir = os.path.join(clone_dir, "dm", target_dyad)
            if os.path.exists(mail_dir) and os.path.isdir(mail_dir):
                # Get the commit hash
                hash_result = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    cwd=clone_dir,
                    capture_output=True,
                    text=True
                )
                commit_hash = hash_result.stdout.strip()

                for mail_file in os.listdir(mail_dir):
                    if mail_file.endswith(".md"):
                        intent = f"Process inbound mail from {locator} at commit {commit_hash} (file: dm/{target_dyad}/{mail_file})"
                        is_auto_reply = any(kw in mail_file.lower() for kw in ["retro", "sync", "audit", "ping"])
                        cmd = ["./bin/todo", intent]
                        if is_auto_reply:
                            cmd.extend(["--status", "AUTO-REPLY"])
                        subprocess.run(cmd)
                        print(f"Added todo for mail from {name}: {mail_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", default="commons/directory")
    parser.add_argument("--target", default="dyad-cairn")
    args = parser.parse_args()
    
    poll_mail(args.directory, args.target)
