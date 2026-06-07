import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Ensure skills is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills import flow_state_manager as fsm

def test_trail_dispose_csi_guard():
    with patch('skills.flow_state_manager.run_cmd') as mock_run_cmd:
        trail_id = "node_4"
        
        fsm.trail_dispose(trail_id)
        
        # Assert 1: PR is merged
        mock_run_cmd.assert_any_call("gh pr merge --merge --delete-branch")
        
        # Assert 2: Issue Closure
        mock_run_cmd.assert_any_call(f"gh issue close {trail_id}")
        
        # Assert 3: Trail Pruning
        mock_run_cmd.assert_any_call(f"python3 skills/frontier_editor.py {trail_id} PRUNE")
