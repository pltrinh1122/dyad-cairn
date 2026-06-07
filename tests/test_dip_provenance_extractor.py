import pytest
import tempfile
import os
from skills.dip_sonar import get_required_dimensions, ProvenanceExtractionError

def create_temp_md(content):
    fd, path = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, 'w') as f:
        f.write(content)
    return path

def test_missing_provenance_file_halts():
    with pytest.raises(ProvenanceExtractionError, match="Provenance file not found"):
        get_required_dimensions(provenance_path="nonexistent_agent.md")

def test_successful_extraction():
    md_content = """
Some text
| # | Dimension | What it establishes |
|---|---|---|
| 1 | **Identity** | foo |
| 2 | **Externality** | bar |
| 3 | **Form-grounding** | baz |
| 4 | **Channel discipline** | qux |
    """
    path = create_temp_md(md_content)
    try:
        dims = get_required_dimensions(provenance_path=path)
        assert dims == ["1_identity", "2_externality", "3_form_grounding", "4_channel_discipline"]
    finally:
        os.remove(path)

def test_missing_table_halts():
    md_content = """
    No table here. Just some text.
    """
    path = create_temp_md(md_content)
    try:
        with pytest.raises(ProvenanceExtractionError, match="Failed to extract dimension table from provenance"):
            get_required_dimensions(provenance_path=path)
    finally:
        os.remove(path)
