import os

def test_state_arc_end_anchor_exists_and_structured():
    anchor_path = "kb/state_arc_end.md"
    assert os.path.exists(anchor_path), f"Anchor file {anchor_path} must exist to achieve form-state separation."
    
    with open(anchor_path, "r") as f:
        content = f.read()
        
    assert "# STATE: ARC-END" in content, "Anchor must define the ARC-END state."
    assert "Reflect & Synthesis" in content, "Anchor must explicitly mention the Reflect & Synthesis phase."
    assert "Invariants" in content, "Anchor must define physical invariants for the arc-end phase."
    assert "Transitions" in content, "Anchor must define allowable FSM transitions (e.g. session-end)."
