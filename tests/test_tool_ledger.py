import pytest
import os
import tempfile
import json
import skills.ledger_manager as lm

def test_append_ledger_default_cairn(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        state_dir = os.path.join(tmpdir, "dyad-state")
        jsonl = os.path.join(state_dir, "ledger.jsonl")
        md = os.path.join(tmpdir, "DYAD_LEDGER.md")
        
        monkeypatch.setattr(lm, "JSONL_FILE", jsonl)
        monkeypatch.setattr(lm, "MD_FILE", md)
        monkeypatch.setattr(lm, "get_state_dir", lambda tool: state_dir if not tool else os.path.join(tmpdir, f"{tool}-state"))
        monkeypatch.setattr(lm, "get_jsonl_file", lambda tool: jsonl if not tool else os.path.join(tmpdir, f"{tool}-state", "ledger.jsonl"))
        monkeypatch.setattr(lm, "get_md_file", lambda tool: md if not tool else os.path.join(tmpdir, f"{tool.upper()}_LEDGER.md"))
        
        lm.append_ledger("clip", "default test")
        
        assert os.path.exists(jsonl)
        assert os.path.exists(md)

def test_append_ledger_tool_context(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock the dynamic path generation
        monkeypatch.setattr(lm, "get_state_dir", lambda tool: os.path.join(tmpdir, f"{tool}-state") if tool else os.path.join(tmpdir, "dyad-state"))
        monkeypatch.setattr(lm, "get_jsonl_file", lambda tool: os.path.join(tmpdir, f"{tool}-state", "ledger.jsonl") if tool else os.path.join(tmpdir, "dyad-state", "ledger.jsonl"))
        monkeypatch.setattr(lm, "get_md_file", lambda tool: os.path.join(tmpdir, f"{tool.upper()}_LEDGER.md") if tool else os.path.join(tmpdir, "DYAD_LEDGER.md"))
        
        # Test calling append_ledger with tool_name="dip"
        lm.append_ledger("clip", "dip specific verdict", tool_name="dip")
        
        jsonl = os.path.join(tmpdir, "dip-state", "ledger.jsonl")
        md = os.path.join(tmpdir, "DIP_LEDGER.md")
        
        assert os.path.exists(jsonl), "Tool-specific state directory or JSONL file was not created"
        with open(jsonl) as f:
            data = json.loads(f.readline())
            assert data["message"] == "dip specific verdict"
            
        assert os.path.exists(md), "Tool-specific Markdown ledger was not created"
        with open(md) as f:
            content = f.read()
            assert "DIP_LEDGER.md" in content, "Header must reflect the tool ledger name"
            assert "dip specific verdict" in content
