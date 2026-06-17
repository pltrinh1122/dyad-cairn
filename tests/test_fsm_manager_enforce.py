import pytest
import sys
from skills.fsm_manager import enforce_guard

def test_enforce_guard_throws_csi_error_on_invalid_transition(capsys):
    with pytest.raises(SystemExit) as exc_info:
        enforce_guard("invalid_transition", is_valid=False)
    
    assert exc_info.value.code == 1
    
    captured = capsys.readouterr()
    assert "🚨 CONSISTENCY GUARDRAIL FIRED 🚨" in captured.out
    assert "Illegal state transition attempted" in captured.out
