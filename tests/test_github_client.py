import unittest
from unittest.mock import patch
from skills.github_client import create_repo

class TestGithubClient(unittest.TestCase):
    @patch('subprocess.run')
    def test_create_repo(self, mock_run):
        class DummyResult:
            returncode = 0
            stdout = "Created repo"
            stderr = ""
        mock_run.return_value = DummyResult()
        
        result = create_repo("test-repo", public=True, push=False)
        self.assertTrue(result)
        mock_run.assert_called_once_with(
            ["gh", "repo", "create", "test-repo", "--public", "--source=.", "--remote=origin"],
            capture_output=True,
            text=True
        )

if __name__ == '__main__':
    unittest.main()
