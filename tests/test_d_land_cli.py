import os
import subprocess
import yaml

def test_d_land_exists_and_executable():
    assert os.path.exists("bin/d-land"), "bin/d-land must exist"
    assert os.access("bin/d-land", os.X_OK), "bin/d-land must be executable"

def test_d_land_cli_wired_to_fsm():
    if not os.path.exists("bin/d-land"):
        assert False, "bin/d-land does not exist yet"
        
    cmd = ["./bin/d-land", "test arc note"]
    env = os.environ.copy()
    env["DYAD_TEST_ENV"] = "1"
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    assert result.returncode == 0, f"Expected 0, got {result.returncode}\n{result.stdout}\n{result.stderr}"
    assert "Executing Arc Land Discipline" in result.stdout
    assert "Pushed FSM into 'arc-land' state" in result.stdout
    
    # Check that fsm_state.yml was updated
    with open("dyad-state/fsm_state.yml", "r") as f:
        data = yaml.safe_load(f)
    assert data.get("state") == "arc-land"
