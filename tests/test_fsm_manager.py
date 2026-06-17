import os
import yaml
import pytest

from skills.fsm_manager import FSMManager, validate_transition

def test_fsm_manager_init_creates_default_state():
    test_file = "artifacts/test_fsm_init.yml"
    if os.path.exists(test_file):
        os.remove(test_file)
        
    # Execute
    manager = FSMManager(state_file=test_file)
    
    # Assert
    assert manager.state_file == test_file
    assert isinstance(manager.state, dict)
    assert manager.state == {}
    
def test_fsm_manager_init_loads_existing_state():
    test_file = "artifacts/test_fsm_init_existing.yml"
    os.makedirs("artifacts", exist_ok=True)
    with open(test_file, "w") as f:
        yaml.dump({"current_state": "SESSION_ACTIVE"}, f)
        
    # Execute
    manager = FSMManager(state_file=test_file)
    
    # Assert
    assert manager.state_file == test_file
    assert manager.state == {"current_state": "SESSION_ACTIVE"}
    
    if os.path.exists(test_file):
        os.remove(test_file)

def test_validate_transition_allowed():
    # Assume a simple valid transition dictionary for the test
    transitions = {
        "PLANNED": ["IN_REVIEW"],
        "IN_REVIEW": ["AUTHORIZED", "RED"]
    }
    assert validate_transition("PLANNED", "IN_REVIEW", transitions) is True

def test_validate_transition_denied():
    transitions = {
        "PLANNED": ["IN_REVIEW"]
    }
    with pytest.raises(ValueError, match="Invalid transition from PLANNED to AUTHORIZED"):
        validate_transition("PLANNED", "AUTHORIZED", transitions)

