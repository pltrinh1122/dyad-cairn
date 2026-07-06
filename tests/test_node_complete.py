import pytest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills import flow_state_manager as fsm

def test_complete_node_success():
    with patch('skills.flow_state_manager.run_cmd') as mock_run_cmd, \
         patch('subprocess.run') as mock_subrun, \
         patch('skills.ledger_manager.append_ledger') as mock_append:
        mock_subrun.return_value.returncode = 0
        def side_effect(cmd, allow_fail=False):
            if "testing_harness.py" in cmd:
                return "[TEST HARNESS] PASS: All tests passed mechanically."
            if "git rev-parse" in cmd:
                return "main"
            return ""
        mock_run_cmd.side_effect = side_effect
        
        node_id = "node_123"
        reflect_msg = "test reflect"
        fsm.complete_node(node_id, reflect_msg)
        
        mock_subrun.assert_any_call("python3 skills/dialect_linter.py", shell=True, capture_output=True, text=True)
        mock_run_cmd.assert_any_call("python3 skills/testing_harness.py", allow_fail=True)
        mock_append.assert_called_with("node-reflect", "[node_123] test reflect")
        mock_run_cmd.assert_any_call("python3 skills/frontier_editor.py node_123 DONE")

def test_complete_node_missing_rca():
    with patch('skills.flow_state_manager.run_cmd') as mock_run_cmd, \
         patch('subprocess.run') as mock_subrun, \
         patch('sys.exit') as mock_exit, \
         patch('os.path.exists') as mock_exists:
        mock_subrun.return_value.returncode = 0
        mock_exit.side_effect = SystemExit
        mock_exists.return_value = False
        
        node_id = "node_123_execute_feature"
        reflect_msg = "test reflect"
        try:
            fsm.complete_node(node_id, reflect_msg)
        except SystemExit:
            pass
            
        mock_exit.assert_called_once_with(1)

def test_complete_node_failure():
    with patch('skills.flow_state_manager.run_cmd') as mock_run_cmd, \
         patch('subprocess.run') as mock_subrun, \
         patch('sys.exit') as mock_exit, \
         patch('skills.ledger_manager.append_ledger') as mock_append:
        mock_subrun.return_value.returncode = 0
        mock_exit.side_effect = SystemExit
        
        def side_effect(cmd, allow_fail=False):
            if "testing_harness.py" in cmd:
                return "[TEST HARNESS] FAIL: Tests did not pass."
            if "git rev-parse" in cmd:
                return "main"
            return ""
        mock_run_cmd.side_effect = side_effect
        
        node_id = "node_123"
        reflect_msg = "test reflect"
        try:
            fsm.complete_node(node_id, reflect_msg)
        except SystemExit:
            pass
        
        mock_run_cmd.assert_any_call("python3 skills/testing_harness.py", allow_fail=True)
        mock_append.assert_not_called()
        assert not any("frontier_editor.py" in str(call) for call in mock_run_cmd.mock_calls)
        mock_exit.assert_called_once_with(1)
