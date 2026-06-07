import os
import subprocess
import shutil

def test_mason_installs_stone_safely():
    """
    RED PHASE SPEC for node_3.
    Asserts that `mason install` correctly extracts a physical stone payload 
    and writes it to BOTH the kb/ and bin/ directories (the Generative Why and the Deterministic How).
    """
    pkg_path = "commons/library/hard-guardrails"
    kb_dest = "kb/HOW-0002-hard-guardrails.md"
    bin_dest = "bin/hard-guardrails"
    
    # 1. Clean up substrate before test
    if os.path.exists(kb_dest):
        os.remove(kb_dest)
    if os.path.exists(bin_dest):
        os.remove(bin_dest)
        
    # 2. Execute installation
    cmd = ["./bin/mason", "install", pkg_path + "/stone.yaml"]
    env = dict(os.environ, PYTHONPATH=os.getcwd())
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    
    # 3. Falsification: If it fails, print stderr to help debug
    assert result.returncode == 0, f"Mason install failed: {result.stderr}"
    
    # 4. Assert Physical Payload Transfer
    assert os.path.exists(kb_dest), "Generative KB asset was not installed."
    assert os.path.exists(bin_dest), "Deterministic BIN asset was not installed."
    
    # 5. Assert Executable Permission was Preserved
    assert os.access(bin_dest, os.X_OK), "Executable permission was stripped during installation."
