import subprocess
import os
import pytest

def test_commission_script_usage():
    result = subprocess.run(['./bin/commission'], capture_output=True, text=True)
    assert result.returncode == 1
    assert "Usage: ./bin/commission <repo> <commit_sha> <file_path>" in result.stdout

def test_commission_script_success(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    
    curl_mock = bin_dir / "curl"
    curl_mock.write_text("#!/bin/bash\n"
                         "if [[ \"$*\" == *\"https://raw.githubusercontent.com/fake/repo/abcdef/commissions/test.md\"* ]]; then\n"
                         "  while [[ $# -gt 0 ]]; do\n"
                         "    if [[ \"$1\" == \"-o\" ]]; then\n"
                         "      echo 'mocked content' > \"$2\"\n"
                         "      exit 0\n"
                         "    fi\n"
                         "    shift\n"
                         "  done\n"
                         "else\n"
                         "  echo \"Unexpected curl arguments: $*\" >&2\n"
                         "  exit 1\n"
                         "fi\n"
                         "exit 0\n")
    curl_mock.chmod(0o755)
    
    monkeypatch.setenv("PATH", str(bin_dir) + ":" + os.environ["PATH"])
    
    real_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bin', 'commission'))
    
    result = subprocess.run([real_script_path, 'fake/repo', 'abcdef', 'commissions/test.md'], capture_output=True, text=True)
    
    assert result.returncode == 0
    assert "[MECHANICAL UI PRESENTATION]" in result.stdout
    assert "Successfully ingested commissions/test.md from fake/repo@abcdef" in result.stdout
    
    assert os.path.exists('commissions/test.md')
    with open('commissions/test.md', 'r') as f:
        content = f.read()
    assert "mocked content\n" in content
