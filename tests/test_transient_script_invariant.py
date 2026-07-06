import os

def test_transient_script_invariant_present():
    with open("DYAD.md", "r") as f:
        content = f.read()
    
    assert "The Transient Script Invariant" in content, "DYAD.md must define 'The Transient Script Invariant'."
    assert "compound bash commands containing more than two commands chained together" in content, "DYAD.md must forbid compound bash commands."
