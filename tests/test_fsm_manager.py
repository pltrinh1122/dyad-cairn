import pytest
from skills.fsm_manager import validate_transition

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
