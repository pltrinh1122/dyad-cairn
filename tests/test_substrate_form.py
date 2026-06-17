import os

def test_wip_invariant_substrate_form():
    with open("DYAD.md", "r") as f:
        content = f.read()

    assert "Substrate Execution is partitioned" in content, "DYAD.md must define Substrate Execution partitioning."
    assert "'Substrate Form' (mutating `DYAD.md`, `GEMINI.md`, or static rules) allows parallel concurrency" in content, "DYAD.md must explicitly allow parallel concurrency for orthogonal 'Substrate Form'."
