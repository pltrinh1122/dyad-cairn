import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Ensure skills is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills import flow_state_manager as fsm

def test_trail_reflect_csi_guard():
    with patch('skills.flow_state_manager.run_cmd') as mock_run_cmd, \
         patch('skills.ledger_manager.append_ledger') as mock_append_ledger, \
         patch('skills.github_client.create_pr', return_value="https://github.com/pr/1") as mock_create_pr:
        
        trail_id = "node_4"
        retro_msg = "We learned X, Y, Z."
        
        fsm.trail_reflect(trail_id, retro_msg)
        
        # Assert 1: The Synthesis Invariant (Trail Retro logged to Ledger)
        mock_append_ledger.assert_called_once_with("trail-retro", retro_msg)
        
        # Assert 2: The Reflection Review Gate (PR Created but not merged/pruned)
        mock_create_pr.assert_called_once()
        args, kwargs = mock_create_pr.call_args
        assert "[REFLECT]" in args[0]
        
        # Ensure it does NOT prune or close the issue (that belongs to dispose)
        for call in mock_run_cmd.call_args_list:
            cmd = call[0][0]
            assert "gh issue close" not in cmd
            assert "PRUNE" not in cmd
