import pytest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills import flow_state_manager as fsm

def test_complete_node_success():
    with patch('skills.flow_state_manager.run_cmd') as mock_run_cmd, \
         patch('skills.ledger_manager.append_ledger') as mock_append:
        def side_effect(cmd, allow_fail=False):
            if "testing_harness.py" in cmd:
                return "[TEST HARNESS] PASS: All tests passed mechanically."
            return ""
        mock_run_cmd.side_effect = side_effect
        
        node_id = "node_123"
        retro_msg = "test retro"
        fsm.complete_node(node_id, retro_msg)
        
        mock_run_cmd.assert_any_call("python3 skills/testing_harness.py", allow_fail=True)
        mock_append.assert_called_once_with("node-retro", "[node_123] test retro")
        mock_run_cmd.assert_any_call(f"python3 skills/frontier_editor.py {node_id} DONE")

def test_complete_node_missing_rca():
    with patch('skills.flow_state_manager.run_cmd') as mock_run_cmd, \
         patch('sys.exit') as mock_exit, \
         patch('os.path.exists') as mock_exists:
        mock_exit.side_effect = SystemExit
        mock_exists.return_value = False
        
        node_id = "node_123_execute_feature"
        retro_msg = "test retro"
        try:
            fsm.complete_node(node_id, retro_msg)
        except SystemExit:
            pass
            
        mock_exit.assert_called_once_with(1)

def test_complete_node_failure():
    with patch('skills.flow_state_manager.run_cmd') as mock_run_cmd, \
         patch('sys.exit') as mock_exit, \
         patch('skills.ledger_manager.append_ledger') as mock_append:
        mock_exit.side_effect = SystemExit
        
        def side_effect(cmd, allow_fail=False):
            if "testing_harness.py" in cmd:
                return "[TEST HARNESS] FAIL: Tests did not pass."
            return ""
        mock_run_cmd.side_effect = side_effect
        
        node_id = "node_123"
        retro_msg = "test retro"
        try:
            fsm.complete_node(node_id, retro_msg)
        except SystemExit:
            pass
        
        mock_run_cmd.assert_any_call("python3 skills/testing_harness.py", allow_fail=True)
        mock_append.assert_not_called()
        assert not any("frontier_editor.py" in str(call) for call in mock_run_cmd.mock_calls)
        mock_exit.assert_called_once_with(1)
