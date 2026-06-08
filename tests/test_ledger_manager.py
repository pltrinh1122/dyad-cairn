import os
import json
import unittest
import tempfile
import shutil
import sys
from unittest.mock import patch

from skills import ledger_manager

class TestLedgerManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.jsonl_path = os.path.join(self.test_dir, "ledger.jsonl")
        self.md_path = os.path.join(self.test_dir, "LEDGER.md")
        
        # Patch the dynamic path functions
        patcher_jsonl = patch("skills.ledger_manager.get_jsonl_file", return_value=self.jsonl_path)
        patcher_md = patch("skills.ledger_manager.get_md_file", return_value=self.md_path)
        patcher_mkdir = patch("os.makedirs", lambda name, exist_ok: None)
        
        self.addCleanup(patcher_jsonl.stop)
        self.addCleanup(patcher_md.stop)
        self.addCleanup(patcher_mkdir.stop)
        
        patcher_jsonl.start()
        patcher_md.start()
        patcher_mkdir.start()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_ledger_append(self):
        ledger_manager.append_ledger("pin", "Test message")
        
        # Verify JSONL
        self.assertTrue(os.path.exists(self.jsonl_path))
        with open(self.jsonl_path, "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            data = json.loads(lines[0])
            self.assertEqual(data["action"], "PIN")
            self.assertEqual(data["message"], "Test message")
            
        # Verify MD
        self.assertTrue(os.path.exists(self.md_path))
        with open(self.md_path, "r") as f:
            md_content = f.read()
            self.assertIn("PIN", md_content)
            self.assertIn("Test message", md_content)
            
        # Second append
        ledger_manager.append_ledger("clip", "Another test")
        
        with open(self.jsonl_path, "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)
            data = json.loads(lines[1])
            self.assertEqual(data["action"], "CLIP")
            self.assertEqual(data["message"], "Another test")
            
        # Third append (RETRO)
        ledger_manager.append_ledger("retro", "Harvesting retro")
        
        with open(self.jsonl_path, "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 3)
            data = json.loads(lines[2])
            self.assertEqual(data["action"], "RETRO")
            self.assertEqual(data["message"], "Harvesting retro")

    @patch("skills.ledger_manager.append_ledger")
    def test_process_retro_persists_payload(self, mock_append):
        def mock_exists(path):
            if path == "dummy.md": return True
            if path == "dyad-state/RETRO_ACTIVE.lock": return False
            return False

        with patch("os.path.exists", side_effect=mock_exists):
            m_open = unittest.mock.mock_open(read_data="CSS\nPayload")
            with patch("builtins.open", m_open):
                ledger_manager.process_retro("Summary", "dummy.md")
            
        expected_message = "Summary\n\n<details><summary>View Retro Payload</summary>\n\nCSS\nPayload\n</details>"
        mock_append.assert_called_with("retro", expected_message)

    def test_append_ledger_multiline_formatting(self):
        multiline_msg = "Line 1\nLine 2\nLine 3"
        ledger_manager.append_ledger("retro", multiline_msg)
        
        with open(self.md_path, "r") as f:
            md_content = f.read()
            self.assertIn("Line 1\n  Line 2\n  Line 3", md_content)

if __name__ == "__main__":
    unittest.main()
