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
        mock_run_cmd.assert_any_call("gh pr merge --merge --delete-branch", allow_fail=True)
        
        # Assert 2: Issue Closure
        mock_run_cmd.assert_any_call(f"gh issue close {trail_id}", allow_fail=True)
        
        # Assert 3: Trail Pruning
        mock_run_cmd.assert_any_call(f"python3 skills/frontier_editor.py {trail_id} PRUNE")

def test_trail_dispose_continues_on_merge_failure():
    with patch('skills.flow_state_manager.run_cmd') as mock_run_cmd:
        trail_id = "node_stale"
        
        def mock_run_cmd_side_effect(cmd, allow_fail=False):
            if "gh pr merge" in cmd:
                # We do not actually raise an exception because run_cmd catches it and returns output if allow_fail=True
                return "GraphQL: Pull request is in clean status (mergePullRequest)"
            return ""
            
        mock_run_cmd.side_effect = mock_run_cmd_side_effect
        
        fsm.trail_dispose(trail_id)
        
        # Verify PRUNE is still executed
        mock_run_cmd.assert_any_call(f"python3 skills/frontier_editor.py {trail_id} PRUNE")
