import os
import subprocess
import shutil

def test_mason_installs_stone_safely(tmp_path):
    """
    RED PHASE SPEC for node_3.
    Asserts that `mason install` correctly extracts a physical stone payload 
    and writes it to BOTH the kb/ and bin/ directories (the Generative Why and the Deterministic How).
    """
    # Create a dummy stone.yaml in a temporary directory to ensure determinism
    pkg_path = tmp_path / "dummy-package"
    pkg_path.mkdir()
    stone_file = pkg_path / "stone.yaml"
    
    # Create the physical source assets in the dummy package
    src_dir = pkg_path / "src"
    src_dir.mkdir()
    
    kb_src = src_dir / "HOW-0002.md"
    kb_src.write_text("# Dummy KB")
    
    bin_src = src_dir / "script.sh"
    bin_src.write_text("#!/bin/bash\necho test")
    os.chmod(bin_src, 0o755)  # Set executable permissions on source file
    
    dummy_yaml = """
stone_id: hard-guardrails
version: 1.0.0
type: CLI
assets:
  - source: "src/HOW-0002.md"
    destination: "kb/HOW-0002-hard-guardrails.md"
  - source: "src/script.sh"
    destination: "bin/hard-guardrails"
"""
    stone_file.write_text(dummy_yaml)
    
    kb_dest = "kb/HOW-0002-hard-guardrails.md"
    bin_dest = "bin/hard-guardrails"
    
    # 1. Clean up substrate before test
    if os.path.exists(kb_dest):
        os.remove(kb_dest)
    if os.path.exists(bin_dest):
        os.remove(bin_dest)
        
    # 2. Execute installation
    cmd = ["./bin/mason", "install", str(stone_file)]
    env = dict(os.environ, PYTHONPATH=os.getcwd())
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    
    # 3. Falsification: If it fails, print stderr to help debug
    assert result.returncode == 0, f"Mason install failed: {result.stderr}"
    assert os.path.exists(kb_dest), "Generative KB asset was not installed."
    assert os.path.exists(bin_dest), "Deterministic BIN asset was not installed."
    
    # 5. Assert Executable Permission was Preserved
    assert os.access(bin_dest, os.X_OK), "Executable permission was stripped during installation."
