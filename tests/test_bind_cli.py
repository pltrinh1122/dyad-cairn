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
        
        mock_run_cmd.return_value = "DYAD.md\nskills/flow_state_manager.py\n"
        
        mock_sub_run.return_value = MagicMock(returncode=0)
        
        ontological_binder.verify_and_bind("Testing bond")
        
        mock_append.assert_called_once_with("ontological-bond", "Testing bond")
        mock_sub_run.assert_any_call("bin/git add DYAD_LEDGER.md dyad-state/ledger.jsonl", shell=True)
        # Verify commit command was called
        commit_called = False
        for call in mock_sub_run.mock_calls:
            name, args, kwargs = call
            if len(args) > 0 and isinstance(args[0], list) and args[0][0].endswith("git") and args[0][1] == "commit":
                commit_called = True
                assert "bind: Testing bond" in args[0]
        assert commit_called

def test_verify_and_bind_missing_theory(capsys):
    with patch('skills.ontological_binder.run_cmd') as mock_run_cmd, \
         patch('sys.exit') as mock_exit:
        mock_exit.side_effect = SystemExit
        
        mock_run_cmd.return_value = "skills/flow_state_manager.py\n"
        
        try:
            ontological_binder.verify_and_bind("Testing bond")
        except SystemExit:
            pass
            
        mock_exit.assert_called_once_with(1)
        captured = capsys.readouterr()
        assert "[STEERING VECTOR] Stage at least one Theory file" in captured.out

def test_verify_and_bind_missing_mechanics(capsys):
    with patch('skills.ontological_binder.run_cmd') as mock_run_cmd, \
         patch('sys.exit') as mock_exit:
        mock_exit.side_effect = SystemExit
        
        mock_run_cmd.return_value = "DYAD.md\n"
        
        try:
            ontological_binder.verify_and_bind("Testing bond")
        except SystemExit:
            pass
            
        mock_exit.assert_called_once_with(1)
        captured = capsys.readouterr()
        assert "[STEERING VECTOR] Stage at least one Mechanics file" in captured.out
