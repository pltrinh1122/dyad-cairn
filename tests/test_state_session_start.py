import os

def test_state_session_start_anchor():
    anchor_path = "kb/state_session_start.md"
    assert os.path.exists(anchor_path), f"Anchor {anchor_path} must exist."
    with open(anchor_path, "r") as f:
        content = f.read()
    
    assert "State: [SESSION_START]" in content, "Must define the State: [SESSION_START]"
    assert "Pre-conditions" in content, "Must define Pre-conditions"
    
    # Failing test to force Red Phase authorization
    assert False, "Structural Spec is written. Awaiting Red Phase design review authorization."
