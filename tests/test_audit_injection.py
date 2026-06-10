import pytest
import os
import sys
from unittest.mock import patch

# Ensure skills is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills import flow_state_manager as fsm

def test_audit_dag_injection_bypasses_in_review():
    mock_state = {
        "config": {"gates": {"design_review": False}},
        "nodes": {}
    }
    
    with patch('skills.frontier_editor.load_state', return_value=mock_state) as mock_load, \
         patch('skills.frontier_editor.save_state') as mock_save:
        
        fsm.inject_node("node_audit_999", "Audit Node", "Testing", "INTEGRITY")
        
        assert mock_save.called
        saved_state = mock_save.call_args[0][0]
        assert "status" not in saved_state["nodes"]["node_audit_999"]
        
def test_frontier_dag_injection_sets_in_review():
    mock_state = {
        "config": {"gates": {"design_review": True}},
        "nodes": {}
    }
    
    with patch('skills.frontier_editor.load_state', return_value=mock_state) as mock_load, \
         patch('skills.frontier_editor.save_state') as mock_save:
        
        fsm.inject_node("node_999", "Frontier Node", "Testing", "FRONTIER")
        
        assert mock_save.called
        saved_state = mock_save.call_args[0][0]
        assert saved_state["nodes"]["node_999"]["status"] == "IN_REVIEW"
