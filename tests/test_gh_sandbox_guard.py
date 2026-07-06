import subprocess
import os

def test_gh_sandbox_guard_allows_issue():
    res = subprocess.run(["python3", "skills/sandbox_enforcer.py", "gh", "issue", "create"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "formally allowed" in res.stdout.lower() or "formally allowed" in res.stderr.lower()

def test_gh_sandbox_guard_blocks_destructive():
    res = subprocess.run(["python3", "skills/sandbox_enforcer.py", "gh", "repo", "delete"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "sandbox guard" in res.stdout.lower() or "sandbox guard" in res.stderr.lower()
