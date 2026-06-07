import pytest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills import flow_state_manager as fsm

def test_complete_node_success():
    with patch('skills.flow_state_manager.run_cmd') as mock_run_cmd:
        def side_effect(cmd, allow_fail=False):
            if "testing_harness.py" in cmd:
                return "[TEST HARNESS] PASS: All tests passed mechanically."
            return ""
        mock_run_cmd.side_effect = side_effect
        
        node_id = "node_123"
        fsm.complete_node(node_id)
        
        mock_run_cmd.assert_any_call("python3 skills/testing_harness.py", allow_fail=True)
        mock_run_cmd.assert_any_call(f"python3 skills/frontier_editor.py {node_id} DONE")

def test_complete_node_failure():
    with patch('skills.flow_state_manager.run_cmd') as mock_run_cmd, \
         patch('sys.exit') as mock_exit:
        mock_exit.side_effect = SystemExit
        
        def side_effect(cmd, allow_fail=False):
            if "testing_harness.py" in cmd:
                return "[TEST HARNESS] FAIL: Tests did not pass."
            return ""
        mock_run_cmd.side_effect = side_effect
        
        node_id = "node_123"
        try:
            fsm.complete_node(node_id)
        except SystemExit:
            pass
        
        mock_run_cmd.assert_any_call("python3 skills/testing_harness.py", allow_fail=True)
        assert not any("frontier_editor.py" in str(call) for call in mock_run_cmd.mock_calls)
        mock_exit.assert_called_once_with(1)
