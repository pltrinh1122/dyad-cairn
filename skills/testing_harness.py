import sys
import subprocess
import os

def run_tests(args):
    # Pure stateless wrapper over pytest.
    # Enforces the Testing Invariant by acting as the only path to execution.
    if not os.path.exists("tests"):
        print("[TEST HARNESS] No 'tests/' directory found. Nothing to run.")
        sys.exit(0)
        
    cmd = ["python3", "-m", "pytest", "tests/"] + args
    print(f"[TEST HARNESS] Executing: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
        
    if result.returncode != 0:
        print("[TEST HARNESS] FAIL: Tests did not pass.")
        sys.exit(1)
    else:
        print("[TEST HARNESS] PASS: All tests passed mechanically.")
        sys.exit(0)

if __name__ == "__main__":
    run_tests(sys.argv[1:])
