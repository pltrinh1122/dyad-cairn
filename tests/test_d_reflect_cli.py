import os
import sys
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills import flow_state_manager as fsm


def test_fsm_process_d_reflect_delegates_to_retro_then_carry_forward():
    with patch("skills.flow_state_manager.process_retro") as mock_retro, \
         patch("subprocess.run") as mock_sub_run:
        mock_sub_run.return_value = MagicMock(returncode=0)

        fsm.process_d_reflect("summary", "fake_path.md", "carry-forward note")

        mock_retro.assert_called_once_with("summary", "fake_path.md")
        mock_sub_run.assert_any_call(
            "python3 skills/ledger_manager.py carry-forward \"carry-forward note\"",
            shell=True, capture_output=False, text=False,
        )


def test_bin_d_reflect_delegates_to_fsm():
    with open("bin/d-reflect", "r") as f:
        content = f.read()
        assert "python3 skills/flow_state_manager.py d-reflect" in content, \
            "bin/d-reflect must delegate to flow_state_manager.py"


def test_ledger_manager_cli_dispatches_carry_forward():
    with open("skills/ledger_manager.py", "r") as f:
        content = f.read()
        assert 'args.action.lower() == "carry-forward"' in content, \
            "ledger_manager.py's CLI must dispatch the carry-forward action"
