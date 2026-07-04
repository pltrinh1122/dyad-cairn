import subprocess
import os

def test_d_start_exists_and_executable():
    assert os.path.exists("bin/d-start"), "bin/d-start must exist"
    assert os.access("bin/d-start", os.X_OK), "bin/d-start must be executable"

def test_legacy_hooks_removed():
    assert not os.path.exists("bin/dyad-shell-hooks.sh"), "Legacy hook bin/dyad-shell-hooks.sh should be removed"
    assert not os.path.exists("bin/start"), "Legacy hook bin/start should be removed, replaced by d-start"
    assert not os.path.exists("tests/test_shell_hooks.py"), "Legacy tests for shell hooks should be removed"
    assert not os.path.exists("tests/test_start_cli.py"), "Legacy tests for start cli should be removed"

def test_d_start_cli_wired_to_fsm():
    if not os.path.exists("bin/d-start"):
        assert False, "bin/d-start does not exist yet"
        
    cmd = ["./bin/d-start"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, "Expected 0"
    assert "No carry-forward state detected" in result.stdout or "CARRY-FORWARD STATE DETECTED" in result.stdout
