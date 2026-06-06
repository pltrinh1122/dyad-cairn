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
        # Setup a dummy directory and inbox
        with tempfile.TemporaryDirectory() as test_dir:
            directory_path = os.path.join(test_dir, "directory")
            inbox_path = os.path.join(test_dir, "inbox")
            os.makedirs(directory_path)
            
            # Create a mock yaml
            with open(os.path.join(directory_path, "dyad-mock.yaml"), "w") as f:
                f.write("name: dyad-mock\nlocator: github.com/mock/dyad-mock\n")
                
            # Mock subprocess.run to create expected files in clone_dir
            def side_effect(args, **kwargs):
                clone_dir = args[5]
                mail_dir = os.path.join(clone_dir, "dm", "dyad-cairn")
                os.makedirs(mail_dir)
                with open(os.path.join(mail_dir, "message.md"), "w") as f:
                    f.write("Hello from mock")
                class DummyResult:
                    returncode = 0
                    stderr = ""
                return DummyResult()
                
            mock_run.side_effect = side_effect
            
            # Execute
            poll_mail(directory_path, inbox_path, target_dyad="dyad-cairn")
            
            # Verify inbox
            expected_file = os.path.join(inbox_path, "dyad-mock_message.md")
            self.assertTrue(os.path.exists(expected_file))
            with open(expected_file, "r") as f:
                self.assertEqual(f.read(), "Hello from mock")

if __name__ == '__main__':
    unittest.main()
