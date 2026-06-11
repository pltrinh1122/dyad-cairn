import os
import pytest
from skills.preflight_grounding import assert_grounding

def test_assert_grounding_missing_field():
    node_data = {"goal": "test"}
    with pytest.raises(SystemExit):
        assert_grounding("node_test", node_data)

def test_assert_grounding_missing_file():
    node_data = {
        "goal": "test",
        "prerequisites": ["nonexistent_file_12345.txt"]
    }
    with pytest.raises(SystemExit):
        assert_grounding("node_test", node_data)

def test_assert_grounding_success():
    node_data = {
        "goal": "test",
        "prerequisites": ["skills/preflight_grounding.py"]
    }
    # Should not raise
    assert_grounding("node_test", node_data)
