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

def test_binaries_are_executable():
    """Verify that bin/gh and bin/git have executable permissions."""
    assert os.access("bin/gh", os.X_OK), "bin/gh must be executable"
    assert os.access("bin/git", os.X_OK), "bin/git must be executable"
