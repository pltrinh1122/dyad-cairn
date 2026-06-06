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
        
        # Patch the file paths
        patcher_jsonl = patch("skills.ledger_manager.JSONL_FILE", self.jsonl_path)
        patcher_md = patch("skills.ledger_manager.MD_FILE", self.md_path)
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

if __name__ == "__main__":
    unittest.main()
