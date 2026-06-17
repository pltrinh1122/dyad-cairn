import pytest
import os
from skills import flow_state_manager as fsm

def test_get_active_anchor():
    """Verify that get_active_anchor returns the appropriate anchor file."""
    # Assuming the default anchor is GEMINI.md
    assert fsm.get_active_anchor() == "GEMINI.md"
