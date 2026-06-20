import os
import json
import tempfile
import unittest
import subprocess
from unittest.mock import patch
from skills.poll_mail import poll_mail

class TestSyncLayer(unittest.TestCase):
    def setUp(self):
        self.queue_file = "dyad-state/sync_queue.jsonl"
        if os.path.exists(self.queue_file):
            os.remove(self.queue_file)

    def tearDown(self):
        if os.path.exists(self.queue_file):
            os.remove(self.queue_file)

    @patch("subprocess.run")
    def test_sync_layer_integration(self, mock_run):
        # Setup a dummy directory for poll_mail
        with tempfile.TemporaryDirectory() as test_dir:
            directory_path = os.path.join(test_dir, "directory")
            os.makedirs(directory_path)
            
            with open(os.path.join(directory_path, "dyad-mock.yaml"), "w") as f:
                f.write("name: dyad-mock\nlocator: github.com/mock/dyad-mock\n")
                
            def side_effect(args, **kwargs):
                if args[0] == "git" and args[1] == "clone":
                    clone_dir = args[5]
                    mail_dir = os.path.join(clone_dir, "dm", "dyad-cairn")
                    os.makedirs(mail_dir)
                    with open(os.path.join(mail_dir, "message.md"), "w") as f:
                        f.write("Hello from mock")
                    class DummyResult:
                        returncode = 0
                        stderr = ""
                    return DummyResult()
                elif args[0] == "git" and args[1] == "rev-parse":
                    class DummyResult:
                        returncode = 0
                        stdout = "dummy_hash\n"
                    return DummyResult()
                elif args[0] == "./bin/todo":
                    class DummyResult:
                        returncode = 0
                    return DummyResult()
                return None
                
            mock_run.side_effect = side_effect
            
            # Step 1: Prove poll_mail.py ONLY writes to the buffer
            poll_mail(directory_path, target_dyad="dyad-cairn")
            
            # Verify todo was NOT called during poll_mail
            todo_calls = [call_args for call_args in mock_run.call_args_list if call_args[0][0][0] == "./bin/todo"]
            self.assertEqual(len(todo_calls), 0, "poll_mail must not call todo directly")
            
            # Verify buffer has data
            self.assertTrue(os.path.exists(self.queue_file), "Queue file must be created")
            with open(self.queue_file, "r") as f:
                lines = f.readlines()
            self.assertEqual(len(lines), 1)
            
            # Step 2: Prove sync-state tool properly consumes it and invokes the todo process
            # Execute the sync-state tool
            import runpy
            import sys
            
            # Mock subprocess in sync-state
            original_argv = sys.argv
            sys.argv = ["bin/sync-state"]
            
            with patch("subprocess.run") as mock_sync_run:
                class DummyResult:
                    returncode = 0
                    stderr = ""
                mock_sync_run.returncode = 0
                mock_sync_run.return_value = DummyResult()
                runpy.run_path("bin/sync-state", run_name="__main__")
                
                # Verify todo WAS called by sync-state
                self.assertEqual(mock_sync_run.call_count, 1)
                cmd_called = mock_sync_run.call_args[0][0]
                self.assertEqual(cmd_called[0], "./bin/todo")
                expected_intent = "Process inbound mail from https://raw.githubusercontent.com/mock/dyad-mock/dummy_hash/dm/dyad-cairn/message.md"
                self.assertEqual(cmd_called[1], expected_intent)
                
            sys.argv = original_argv
            
            # Step 3: Verify the buffer is cleared atomically
            with open(self.queue_file, "r") as f:
                content = f.read()
            self.assertEqual(content, "", "Queue file must be cleared after sync-state consumes it")

if __name__ == "__main__":
    unittest.main()
