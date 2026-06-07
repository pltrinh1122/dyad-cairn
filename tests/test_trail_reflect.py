import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Ensure skills is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills import flow_state_manager as fsm

def test_trail_reflect_csi_guard():
    with patch('skills.flow_state_manager.run_cmd') as mock_run_cmd, \
         patch('skills.ledger_manager.append_ledger') as mock_append_ledger:
        
        # We need fsm.trail_reflect to exist
        trail_id = "node_4"
        retro_msg = "We learned X, Y, Z."
        
        fsm.trail_reflect(trail_id, retro_msg)
        
        # Assert 1: The Synthesis Invariant (Trail Retro logged to Ledger)
        mock_append_ledger.assert_called_once_with("trail-retro", retro_msg)
        
        # Assert 2: The Issue Closure Invariant
        # We expect a call to gh issue close
        mock_run_cmd.assert_any_call(f"gh issue close {trail_id}")
        
        # Assert 3: The Trail Pruning Invariant
        # We expect a call to frontier_editor to prune the trail
        mock_run_cmd.assert_any_call(f"python3 skills/frontier_editor.py {trail_id} PRUNE")
