import os
import stat
import tempfile
import subprocess

def test_claude_wrapper_appends_flag():
    # We want to ensure bin/claude forwards arguments and prepends --dangerously-skip-permissions
    # We create a dummy system claude that just echoes its arguments
    with tempfile.TemporaryDirectory() as tmpdir:
        dummy_claude_path = os.path.join(tmpdir, 'claude')
        with open(dummy_claude_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("echo \"CLAUDE CALLED WITH: $@\"\n")
        
        # Make dummy claude executable
        st = os.stat(dummy_claude_path)
        os.chmod(dummy_claude_path, st.st_mode | stat.S_IEXEC)
        
        # Set PATH so our dummy claude is the "system" one
        env = os.environ.copy()
        env['PATH'] = tmpdir + os.pathsep + env.get('PATH', '')
        
        # Call bin/claude from the repository
        bin_claude = os.path.abspath("./bin/claude")
        result = subprocess.run([bin_claude, "arg1", "--flag2"], env=env, capture_output=True, text=True)
        
        assert result.returncode == 0, f"bin/claude failed: {result.stderr}"
        expected_substring = "CLAUDE CALLED WITH: --dangerously-skip-permissions arg1 --flag2"
        assert expected_substring in result.stdout, f"Missing flag. Output was: {result.stdout}"

def test_claude_wrapper_dry_run():
    # Test that CLAUDE_SH_DRY_RUN=1 prints the command without executing it
    with tempfile.TemporaryDirectory() as tmpdir:
        dummy_claude_path = os.path.join(tmpdir, 'claude')
        with open(dummy_claude_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("echo \"CLAUDE EXECUTED\"\n")
        
        st = os.stat(dummy_claude_path)
        os.chmod(dummy_claude_path, st.st_mode | stat.S_IEXEC)
        
        env = os.environ.copy()
        env['PATH'] = tmpdir + os.pathsep + env.get('PATH', '')
        env['CLAUDE_SH_DRY_RUN'] = '1'
        
        bin_claude = os.path.abspath("./bin/claude")
        result = subprocess.run([bin_claude, "arg1", "--flag2"], env=env, capture_output=True, text=True)
        
        assert result.returncode == 0, f"bin/claude failed: {result.stderr}"
        assert "CLAUDE EXECUTED" not in result.stdout, "claude was actually executed during dry-run"
        assert "(dry-run) would exec" in result.stderr
