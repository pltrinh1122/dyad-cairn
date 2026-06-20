import subprocess
todos = [
    "todo_1781982663.178791_f63393c2",
    "todo_1781982663.209401_eb18d0da",
    "todo_1781982663.238387_1071baa2",
    "todo_1781982663.265664_f4ecc98d",
    "todo_1782001242",
    "todo_1782001245"
]
for t in todos:
    out = subprocess.check_output(["./bin/rub", t, "--what", "Evaluate and prune legacy mail.", "--why", "Message is functionally obsolete.", "--scope", "FRONTIER"]).decode()
    node_id = None
    for line in out.splitlines():
        if "Successfully converted" in line and "(AUTHORIZED)" in line:
            parts = line.split()
            for p in parts:
                if p.startswith("node_todo"):
                    node_id = p
                    break
    if node_id:
        subprocess.check_call(["./bin/node", "complete", node_id, "Pruned structurally obsolete legacy mail."])
