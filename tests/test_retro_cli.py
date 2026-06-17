import pytest
import os
import sys
from unittest.mock import patch, MagicMock
import subprocess

# Ensure skills is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills import flow_state_manager as fsm

def test_fsm_process_retro_success():
    with patch('subprocess.run') as mock_sub_run:
        # Mock success for linter and ledger manager
        mock_sub_run.return_value = MagicMock(returncode=0)
        
        fsm.process_retro("test summary", "fake_path.md")
        
        # Assert Linter is called
        mock_sub_run.assert_any_call("python3 skills/retro_linter.py \"fake_path.md\"", shell=True, capture_output=False, text=False)
        
        # Assert Ledger Manager is called
        mock_sub_run.assert_any_call("python3 skills/ledger_manager.py retro \"test summary\" \"fake_path.md\"", shell=True, capture_output=False, text=False)

def test_fsm_process_retro_linter_failure():
    with patch('subprocess.run') as mock_sub_run, patch('sys.exit') as mock_exit, patch('builtins.print') as mock_print:
        # Mock failure for linter
        mock_sub_run.return_value = MagicMock(returncode=1)
        
        fsm.process_retro("test summary", "fake_path.md")
        
        # Linter is called
        mock_sub_run.assert_any_call("python3 skills/retro_linter.py \"fake_path.md\"", shell=True, capture_output=False, text=False)
        
        # Print failure and exit
        mock_print.assert_any_call("🚨 CSI GUARDRAIL BLOCK: Retro does not match CSS template.")
        mock_exit.assert_called_once_with(1)

def test_bin_retro_delegates_to_fsm():
    with open("bin/retro", "r") as f:
        content = f.read()
        assert "python3 skills/flow_state_manager.py retro" in content, "bin/retro must delegate to flow_state_manager.py"
