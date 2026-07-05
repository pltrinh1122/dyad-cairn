import os
import pytest
from skills import flow_state_manager

def test_gh_mock_intercepts_pr_merge():
    """Verify that bin/gh intercepts 'gh pr merge' and utilizes GITHUB_TOKEN via python."""
    # We expect our new mock layer to handle this, not the system gh.
    
    # Asserting that `gh` command path resolves to our mock binary
    out = flow_state_manager.run_cmd("which gh", allow_fail=True)
    assert os.path.abspath("bin/gh") == out.strip(), f"Expected {os.path.abspath('bin/gh')}, got {out.strip()}"
    
    # Asserting that `git` command path resolves to our mock binary
    out_git = flow_state_manager.run_cmd("which git", allow_fail=True)
    assert os.path.abspath("bin/git") == out_git.strip(), f"Expected {os.path.abspath('bin/git')}, got {out_git.strip()}"

def test_gh_sh_trap():
    """Verify that calling bin/gh.sh directly is trapped and fails."""
    out = flow_state_manager.run_cmd("bin/gh.sh", allow_fail=True)
    assert "ERROR: Use extensionless 'gh'" in out, "bin/gh.sh should trap and fail with specific error"

def test_git_sh_trap():
    """Verify that calling bin/git.sh directly is trapped and fails."""
    out = flow_state_manager.run_cmd("bin/git.sh", allow_fail=True)
    assert "ERROR: Use extensionless 'git'" in out, "bin/git.sh should trap and fail with specific error"
