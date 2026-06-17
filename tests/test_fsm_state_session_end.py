import os
import unittest

class TestFsmStateSessionEnd(unittest.TestCase):
    def test_state_session_end_template_exists_and_valid(self):
        """Assert that kb/templates/state_session_end.md exists and has the correct schema"""
        template_path = "kb/templates/state_session_end.md"
        
        # 1. Assert existence
        self.assertTrue(os.path.exists(template_path), f"Missing template: {template_path}")
        
        # 2. Assert schema structural integrity
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        self.assertIn("# State Session End", content, "Template is missing the required schema heading")

if __name__ == '__main__':
    unittest.main()
