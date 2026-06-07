import pytest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills import ontological_binder

def test_verify_and_bind_success():
    with patch('skills.ontological_binder.run_cmd') as mock_run_cmd, \
         patch('subprocess.run') as mock_sub_run, \
         patch('skills.ledger_manager.append_ledger') as mock_append:
        
        mock_run_cmd.return_value = "AGENT.md\nskills/flow_state_manager.py\n"
        
        mock_sub_run.return_value = MagicMock(returncode=0)
        
        ontological_binder.verify_and_bind("Testing bond")
        
        mock_append.assert_called_once_with("ontological-bond", "Testing bond")
        mock_sub_run.assert_any_call("git add DYAD_LEDGER.md dyad-state/ledger.jsonl", shell=True)
        # Verify commit command was called
        commit_called = False
        for call in mock_sub_run.mock_calls:
            name, args, kwargs = call
            if len(args) > 0 and isinstance(args[0], list) and args[0][0] == "git" and args[0][1] == "commit":
                commit_called = True
                assert "bind: Testing bond" in args[0]
        assert commit_called

def test_verify_and_bind_missing_theory():
    with patch('skills.ontological_binder.run_cmd') as mock_run_cmd, \
         patch('sys.exit') as mock_exit:
        mock_exit.side_effect = SystemExit
        
        mock_run_cmd.return_value = "skills/flow_state_manager.py\n"
        
        try:
            ontological_binder.verify_and_bind("Testing bond")
        except SystemExit:
            pass
            
        mock_exit.assert_called_once_with(1)

def test_verify_and_bind_missing_mechanics():
    with patch('skills.ontological_binder.run_cmd') as mock_run_cmd, \
         patch('sys.exit') as mock_exit:
        mock_exit.side_effect = SystemExit
        
        mock_run_cmd.return_value = "AGENT.md\n"
        
        try:
            ontological_binder.verify_and_bind("Testing bond")
        except SystemExit:
            pass
            
        mock_exit.assert_called_once_with(1)
