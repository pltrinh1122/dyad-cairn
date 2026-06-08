import pytest
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Ensure skills is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills import flow_state_manager as fsm

def test_trail_reflect_missing_synthesis():
    with patch('skills.flow_state_manager.run_cmd'), \
         patch('sys.exit') as mock_exit, \
         patch('os.path.exists', return_value=False):
        mock_exit.side_effect = SystemExit
        try:
            fsm.trail_reflect("node_4")
        except SystemExit:
            pass
        mock_exit.assert_called_once_with(1)

def test_trail_reflect_missing_narrative_keywords():
    with patch('skills.flow_state_manager.run_cmd'), \
         patch('sys.exit') as mock_exit, \
         patch('os.path.exists', return_value=True), \
         patch('builtins.open', unittest.mock.mock_open(read_data="Just a plain summary")):
        mock_exit.side_effect = SystemExit
        try:
            fsm.trail_reflect("node_4")
        except SystemExit:
            pass
        mock_exit.assert_called_once_with(1)

def test_trail_reflect_csi_guard():
    with patch('skills.flow_state_manager.run_cmd') as mock_run_cmd, \
         patch('skills.ledger_manager.append_ledger') as mock_append_ledger, \
         patch('skills.github_client.create_pr', return_value="https://github.com/pr/1") as mock_create_pr, \
         patch('os.path.exists', return_value=True), \
         patch('builtins.open', unittest.mock.mock_open(read_data="Probe Invariant: verified. Execution RCA: see details.")):
        
        trail_id = "node_4"
        
        fsm.trail_reflect(trail_id)
        
        retro_msg = "Probe Invariant: verified. Execution RCA: see details."
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
