import os
import stat
import tempfile
import subprocess
import shutil

def test_agy_wrapper_appends_flag():
    # We want to ensure bin/agy forwards arguments and appends --dangerously-bypass-permission
    # We create a dummy system agy that just echoes its arguments
    with tempfile.TemporaryDirectory() as tmpdir:
        dummy_agy_path = os.path.join(tmpdir, 'agy')
        with open(dummy_agy_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("echo \"AGY CALLED WITH: $@\"\n")
        
        # Make dummy agy executable
        st = os.stat(dummy_agy_path)
        os.chmod(dummy_agy_path, st.st_mode | stat.S_IEXEC)
        
        # Set PATH so our dummy agy is the "system" one
        env = os.environ.copy()
        env['PATH'] = tmpdir + os.pathsep + env.get('PATH', '')
        
        # Call bin/agy from the repository
        bin_agy = os.path.abspath("./bin/agy")
        result = subprocess.run([bin_agy, "arg1", "--flag2"], env=env, capture_output=True, text=True)
        
        assert result.returncode == 0, f"bin/agy failed: {result.stderr}"
        expected_substring = "AGY CALLED WITH: arg1 --flag2 --dangerously-bypass-permission"
        assert expected_substring in result.stdout, f"Missing flag. Output was: {result.stdout}"
