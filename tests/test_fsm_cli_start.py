import os
import subprocess
import yaml
import shutil

def test_start_cli_pushes_session_start():
    state_file = "dyad-state/fsm_state.yml"

    # Backup
    if os.path.exists(state_file):
        shutil.move(state_file, state_file + ".bak")

    try:
        # Run bin/start
        result = subprocess.run(["./bin/start"], capture_output=True, text=True)
        assert result.returncode == 0, f"start CLI failed: {result.stderr}"

        # Verify state
        assert os.path.exists(state_file), "FSM state file was not created"
        with open(state_file, "r") as f:
            data = yaml.safe_load(f)

        assert data.get("state") == "session-start", "FSM did not transition to session-start"

    finally:
        if os.path.exists(state_file + ".bak"):
            shutil.move(state_file + ".bak", state_file)
        elif os.path.exists(state_file):
            os.remove(state_file)
