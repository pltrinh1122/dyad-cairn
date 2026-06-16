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

def test_assert_batch_semantic_alignment_failure(monkeypatch):
    from skills.preflight_grounding import assert_batch_semantic_alignment
    batch_data = [
        {"goal": "Add a new button to the UI", "title": "Button UI"},
        {"goal": "Refactor database schema for user profiles", "title": "DB Schema"}
    ]
    # Mock the LLM check to return False
    monkeypatch.setattr("skills.preflight_grounding._call_llm_semantic_check", lambda b: False)
    with pytest.raises(SystemExit):
        assert_batch_semantic_alignment(batch_data)

def test_assert_batch_semantic_alignment_success(monkeypatch):
    from skills.preflight_grounding import assert_batch_semantic_alignment
    batch_data = [
        {"goal": "Add a new button to the UI", "title": "Button UI"},
        {"goal": "Style the new button", "title": "Button Style"}
    ]
    # Mock the LLM check to return True
    monkeypatch.setattr("skills.preflight_grounding._call_llm_semantic_check", lambda b: True)
    # Should not raise
    assert_batch_semantic_alignment(batch_data)
