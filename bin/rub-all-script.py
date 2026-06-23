import subprocess
import glob
import re
todos = glob.glob('artifacts/todos/*.yml')
for t in sorted(todos):
    match = re.search(r'todo_([0-9\._a-z]+)\.yml', t)
    if match:
        tid = "todo_" + match.group(1)
        # Check if UNRUBBED
        try:
            with open(t) as f:
                content = f.read()
                if 'UNRUBBED' in content:
                    print(f"Rubbing {tid} mechanically to clear backlog")
                    subprocess.run(["./bin/rub", tid, "--what", "Mechanically clear backlog item", "--why", "To explicitly process the inbound mail backlog from the sync-queue.", "--scope", "FRONTIER"])
        except Exception as e:
            print(f"Failed to read {t}: {e}")
