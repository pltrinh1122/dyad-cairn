import subprocess

def test_start_cli_wired_to_fsm():
    cmd = ["./bin/start"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Expected 0, got {result.returncode}. Stderr: {result.stderr}"
    assert "[FLOW] Executing Session Start" in result.stdout
