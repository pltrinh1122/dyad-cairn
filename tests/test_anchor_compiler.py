import pytest
import os
import sys
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from skills import anchor_compiler

def test_compile_anchor_symmetric_generation(tmp_path):
    dip_path = tmp_path / "artifacts" / "dip_state.yml"
    dip_path.parent.mkdir(parents=True)
    dip_path.write_text("dimensions:\n  1_identity:\n    status: APPROVED\n    content: 'test'")
    
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        # Mock validate_matrix to avoid needing real schema checks
        with patch("skills.anchor_compiler.validate_matrix", return_value=None):
            anchor_compiler.compile_anchor()
            
        assert os.path.exists("GEMINI.md"), "GEMINI.md was not generated"
        assert os.path.exists("CLAUDE.md"), "CLAUDE.md was not generated"
        
        gemini_content = open("GEMINI.md").read()
        claude_content = open("CLAUDE.md").read()
        
        assert "This is the platform shim for Gemini." in gemini_content
        assert "This is the platform shim for Claude." in claude_content
        assert "## 1. Identity" in gemini_content
        assert "## 1. Identity" in claude_content
    finally:
        os.chdir(original_cwd)
