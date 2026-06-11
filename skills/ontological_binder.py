import sys
import subprocess

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()

def verify_and_bind(message):
    staged_files = run_cmd("git diff --cached --name-only").splitlines()
    
    theory_files = [f for f in staged_files if f in ["DYAD.md", "GEMINI.md"] or f.startswith("kb/WHY-")]
    mechanics_files = [f for f in staged_files if f.startswith("skills/") or f.startswith("bin/") or f.startswith("tests/") or f.startswith("commons/")]
    
    if not theory_files:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("Ontological Bond Failed: The Theory Plane (DYAD.md, GEMINI.md, or kb/WHY-*) is missing from the staged files.")
        print("You must permanently codify the generative intent of this change.")
        print("[STEERING VECTOR] Stage at least one Theory file (e.g., DYAD.md or kb/WHY-*) that documents the intent of this change, then rerun.")
        sys.exit(1)
        
    if not mechanics_files:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print("Ontological Bond Failed: The Mechanics Plane (skills/, bin/, tests/, commons/) is missing from the staged files.")
        print("Philosophical intent cannot exist without mechanical enforcement.")
        print("[STEERING VECTOR] Stage at least one Mechanics file (skills/, bin/, tests/, commons/) that physically enforces the intent, then rerun.")
        sys.exit(1)
        
    # Append to ledger and stage it
    sys.path.append('.')
    from skills import ledger_manager
    ledger_manager.append_ledger("ontological-bond", message)
    subprocess.run("git add DYAD_LEDGER.md dyad-state/ledger.jsonl", shell=True)
    
    # Execute the bind commit
    commit_cmd = ["git", "commit", "-m", f"bind: {message}"]
    result = subprocess.run(commit_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print(f"Failed to commit Ontological Bond: {result.stderr}")
        print("[STEERING VECTOR] Inspect the git error above, resolve the underlying repository conflict, and rerun.")
        sys.exit(1)
        
    print(f"[BIND] Ontological Bond successfully forged: {message}")
    print("[BIND] The planes of Theory, Mechanics, and State are now synchronized.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 skills/ontological_binder.py \"<Message>\"")
        sys.exit(1)
    verify_and_bind(sys.argv[1])
