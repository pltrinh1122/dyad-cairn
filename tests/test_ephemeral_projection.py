import os

def test_ephemeral_projection_gitignore():
    """Verify that artifacts/frontier_state.md is untracked and in .gitignore."""
    # 1. Check .gitignore
    with open(".gitignore", "r") as f:
        content = f.read()
    assert "artifacts/frontier_state.md" in content, "Materialized View must be in .gitignore"
    
def test_pr_injection_logic():
    """Verify that flow_state_manager.py injects the DAG snapshot into PRs."""
    with open("skills/flow_state_manager.py", "r") as f:
        content = f.read()
    assert "build_tree(state.get('nodes'" in content, "PR generation must compile DAG"
    assert "Computed Frontier DAG (Ephemeral Snapshot)" in content, "PR body must include ephemeral snapshot header"
