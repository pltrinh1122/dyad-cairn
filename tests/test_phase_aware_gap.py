import os

def test_validate_yml_has_phase_aware_logic():
    with open(".github/workflows/validate.yml", "r") as f:
        content = f.read()
    assert "PR_TITLE" in content, "validate.yml must read PR_TITLE"
    assert "[RED Node]" in content, "validate.yml must check for RED Node"
    assert "[GREEN Node]" in content, "validate.yml must check for GREEN Node"

def test_flow_state_manager_expects_gap_pass_for_red():
    with open("skills/flow_state_manager.py", "r") as f:
        content = f.read()
    # The old code had: "if gap_result.returncode == 0:" under the else branch for Red phase.
    # We want to ensure that block is removed or replaced.
    # Let's assert that we check gap_result.returncode != 0 universally or something.
    # A simple assert is that "The remote GAP PASSED during the Red Phase!" is no longer printed.
    assert "The remote GAP PASSED during the Red Phase!" not in content, "flow_state_manager should not fail if GAP passes in Red phase"
