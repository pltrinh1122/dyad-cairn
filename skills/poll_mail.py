import os
import subprocess
import tempfile
import re
import json
import fcntl

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

    ledger_file = "dyad-state/ledger.jsonl"
    ledgered_intents = set()
    if os.path.exists(ledger_file):
        with open(ledger_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if "intent" in entry:
                        ledgered_intents.add(entry["intent"])
                except json.JSONDecodeError:
                    pass

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
                        # Build remote raw URL
                        if "github.com" in locator:
                            repo_path = locator.split("github.com/")[-1]
                            raw_url = f"https://raw.githubusercontent.com/{repo_path}/{commit_hash}/dm/{target_dyad}/{mail_file}"
                        else:
                            # Fallback
                            raw_url = f"{locator}/raw/{commit_hash}/dm/{target_dyad}/{mail_file}"
                            
                        intent = f"Process inbound mail from {raw_url}"
                        if intent in ledgered_intents:
                            print(f"Skipping already ledgered intent: {intent}")
                            continue

                        is_auto_reply = any(kw in mail_file.lower() for kw in ["retro", "sync", "audit", "ping"])
                        
                        queue_payload = {
                            "intent": intent,
                            "status": "AUTO-REPLY" if is_auto_reply else "UNRUBBED",
                            "source": name,
                            "file": mail_file
                        }
                        queue_file = "dyad-state/sync_queue.jsonl"
                        os.makedirs(os.path.dirname(queue_file), exist_ok=True)
                        with open(queue_file, "a") as f:
                            fcntl.flock(f, fcntl.LOCK_EX)
                            f.write(json.dumps(queue_payload) + "\n")
                            fcntl.flock(f, fcntl.LOCK_UN)
                            
                        print(f"Queued todo for mail from {name}: {raw_url}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", default="commons/directory")
    parser.add_argument("--target", default="dyad-cairn")
    args = parser.parse_args()
    
    poll_mail(args.directory, args.target)
