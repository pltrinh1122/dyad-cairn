import unittest
import subprocess
import os
import tempfile
import shutil

class TestShellHooks(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.bin_dir = os.path.join(self.test_dir, "bin")
        os.makedirs(self.bin_dir, exist_ok=True)
        
        # Copy the hooks script to temp bin directory
        shutil.copy("bin/dyad-shell-hooks.sh", self.bin_dir)
        
        # Create a mock bin/exit
        with open(os.path.join(self.bin_dir, "exit"), "w") as f:
            f.write("#!/bin/bash\necho 'bin_exit_executed'")
        os.chmod(os.path.join(self.bin_dir, "exit"), 0o755)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_agy_dyad_hook_executes_bin_exit(self):
        script = f"""
        cd {self.test_dir}
        source bin/dyad-shell-hooks.sh
        agy() {{
            echo "agy_mock_executed"
        }}
        agy_dyad
        """
        result = subprocess.run(["bash", "-c", script], capture_output=True, text=True)
        self.assertIn("agy_mock_executed", result.stdout)
        self.assertIn("bin_exit_executed", result.stdout)

    def test_claude_dyad_hook_executes_bin_exit(self):
        script = f"""
        cd {self.test_dir}
        source bin/dyad-shell-hooks.sh
        claude() {{
            echo "claude_mock_executed"
        }}
        claude_dyad
        """
        result = subprocess.run(["bash", "-c", script], capture_output=True, text=True)
        self.assertIn("claude_mock_executed", result.stdout)
        self.assertIn("bin_exit_executed", result.stdout)

if __name__ == '__main__':
    unittest.main()
