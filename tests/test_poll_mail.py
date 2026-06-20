import os
import unittest
import tempfile
from unittest.mock import patch
from skills.poll_mail import parse_locator, poll_mail

class TestPollMail(unittest.TestCase):
    def test_parse_locator(self):
        yaml_content = """name: dyad-touchstone
birth_hash: "sha256:123"
locator: github.com/pltrinh1122/dyad-touchstone
"""
        name, locator = parse_locator(yaml_content)
        self.assertEqual(name, "dyad-touchstone")
        self.assertEqual(locator, "github.com/pltrinh1122/dyad-touchstone")
        
    @patch('subprocess.run')
    def test_poll_mail_extraction(self, mock_run):
        # Setup a dummy directory
        with tempfile.TemporaryDirectory() as test_dir:
            directory_path = os.path.join(test_dir, "directory")
            os.makedirs(directory_path)
            
            # Create a mock yaml
            with open(os.path.join(directory_path, "dyad-mock.yaml"), "w") as f:
                f.write("name: dyad-mock\nlocator: github.com/mock/dyad-mock\n")
                
            # Mock subprocess.run to create expected files in clone_dir
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
                return None
                
            mock_run.side_effect = side_effect
            
            queue_file = "dyad-state/sync_queue.jsonl"
            if os.path.exists(queue_file):
                os.remove(queue_file)
            
            # Execute
            poll_mail(directory_path, target_dyad="dyad-cairn")
            
            # Verify todo was queued
            self.assertTrue(os.path.exists(queue_file))
            with open(queue_file, "r") as f:
                queue_content = f.read()
                
            import json
            queue_items = [json.loads(line) for line in queue_content.strip().split("\n")]
            self.assertEqual(len(queue_items), 1)
            
            expected_intent = "Process inbound mail from https://raw.githubusercontent.com/mock/dyad-mock/dummy_hash/dm/dyad-cairn/message.md"
            self.assertEqual(queue_items[0]["intent"], expected_intent)

    @patch('subprocess.run')
    def test_poll_mail_deduplication(self, mock_run):
        # Setup a dummy directory
        with tempfile.TemporaryDirectory() as test_dir:
            directory_path = os.path.join(test_dir, "directory")
            os.makedirs(directory_path)
            
            # Create a mock yaml
            with open(os.path.join(directory_path, "dyad-mock.yaml"), "w") as f:
                f.write("name: dyad-mock\nlocator: github.com/mock/dyad-mock\n")
                
            # Mock subprocess.run to create expected files in clone_dir
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
                return None
                
            mock_run.side_effect = side_effect
            
            queue_file = "dyad-state/sync_queue.jsonl"
            ledger_file = "dyad-state/ledger.jsonl"
            
            if os.path.exists(queue_file):
                os.remove(queue_file)
            
            os.makedirs(os.path.dirname(ledger_file), exist_ok=True)
            expected_intent = "Process inbound mail from https://raw.githubusercontent.com/mock/dyad-mock/dummy_hash/dm/dyad-cairn/message.md"
            with open(ledger_file, "w") as f:
                import json
                f.write(json.dumps({"intent": expected_intent, "status": "DONE"}) + "\n")
            
            # Execute
            poll_mail(directory_path, target_dyad="dyad-cairn")
            
            # Verify queue file was NOT created or is empty
            if os.path.exists(queue_file):
                with open(queue_file, "r") as f:
                    q_content = f.read().strip()
                self.assertEqual(q_content, "")
            else:
                self.assertFalse(os.path.exists(queue_file))
                
            if os.path.exists(ledger_file):
                os.remove(ledger_file)

if __name__ == '__main__':
    unittest.main()
