import os

def test_state_arc_start_anchor_exists():
    anchor_path = "kb/templates/state_arc_start.md"
    assert os.path.exists(anchor_path), "state_arc_start.md anchor is missing"
    with open(anchor_path, "r") as f:
        content = f.read()
    assert "# State Arc Start" in content
