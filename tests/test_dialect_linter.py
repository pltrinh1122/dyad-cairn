import os
import pytest
import subprocess
import json

def test_dialect_linter_missing_env():
    # If ANTIGRAVITY_CONVERSATION_ID is missing, it should just return 0 and skip
    env = os.environ.copy()
    if "ANTIGRAVITY_CONVERSATION_ID" in env:
        del env["ANTIGRAVITY_CONVERSATION_ID"]
        
    result = subprocess.run(["python3", "skills/dialect_linter.py"], env=env, capture_output=True, text=True)
    assert result.returncode == 0
    assert "Skipping dialect audit" in result.stdout

def test_dialect_linter_with_mock_transcript(tmp_path):
    env = os.environ.copy()
    conv_id = "test_conv_id_123"
    env["ANTIGRAVITY_CONVERSATION_ID"] = conv_id
    
    # Create mock transcript
    brain_dir = tmp_path / ".gemini" / "antigravity-cli" / "brain" / conv_id / ".system_generated" / "logs"
    brain_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = brain_dir / "transcript.jsonl"
    
    # Mocking os.path.expanduser to point to our tmp_path
    mock_script = tmp_path / "mock_linter.py"
    with open("skills/dialect_linter.py", "r") as f:
        content = f.read()
        content = content.replace('~/.gemini', str(tmp_path / '.gemini'))
        
    with open(mock_script, "w") as f:
        f.write(content)
        
    # Scenario 1: No violations
    with open(transcript_path, "w") as f:
        f.write(json.dumps({"type": "USER_INPUT", "content": "hello\n"}) + "\n")
        f.write(json.dumps({"type": "PLANNER_RESPONSE", "tool_calls": []}) + "\n")
        
    result = subprocess.run(["python3", str(mock_script)], env=env, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed: {result.stdout}"
    
    # Scenario 2: User says `read: frontier`, Agent fails to invoke `bin/read`
    with open(transcript_path, "a") as f:
        f.write(json.dumps({"type": "USER_INPUT", "content": "read: frontier\n", "step_index": 5}) + "\n")
        f.write(json.dumps({"type": "PLANNER_RESPONSE", "tool_calls": [{"args": "something else"}]}) + "\n")
        
    result = subprocess.run(["python3", str(mock_script)], env=env, capture_output=True, text=True)
    assert result.returncode == 1
    assert "CSI GUARDRAIL BLOCK" in result.stdout
    assert "User issued 'read:' but Agent generated output without invoking 'bin/read'" in result.stdout
    
    # Scenario 3: User says `read: frontier`, Agent invokes `bin/read` correctly
    with open(transcript_path, "w") as f:
        f.write(json.dumps({"type": "USER_INPUT", "content": "read: frontier\n", "step_index": 5}) + "\n")
        f.write(json.dumps({"type": "PLANNER_RESPONSE", "tool_calls": [{"args": '{"CommandLine": "./bin/read frontier"}'}]}) + "\n")
        
    result = subprocess.run(["python3", str(mock_script)], env=env, capture_output=True, text=True)
    assert result.returncode == 0
    assert "No UI Dialect violations detected" in result.stdout
    
    # Scenario 4: User says `retro:`, Agent runs bin/retro but fails to print CSS template
    with open(transcript_path, "w") as f:
        f.write(json.dumps({"type": "USER_INPUT", "content": "retro: test\n", "step_index": 6}) + "\n")
        f.write(json.dumps({"type": "PLANNER_RESPONSE", "content": "Locked to ledger.", "tool_calls": [{"args": '{"CommandLine": "./bin/retro test test.md"}'}]}) + "\n")
        
    result = subprocess.run(["python3", str(mock_script)], env=env, capture_output=True, text=True)
    assert result.returncode == 1
    assert "failed to explicitly present the CSS template in the chat UI" in result.stdout
    
    # Scenario 5: User says `retro:`, Agent runs bin/retro and prints CSS template
    with open(transcript_path, "w") as f:
        f.write(json.dumps({"type": "USER_INPUT", "content": "retro: test\n", "step_index": 7}) + "\n")
        f.write(json.dumps({"type": "PLANNER_RESPONSE", "content": "📋 [MECHANICAL UI PRESENTATION: RETRO SUMMARY]\nIt worked.", "tool_calls": [{"args": '{"CommandLine": "./bin/retro test test.md"}'}]}) + "\n")
        
    result = subprocess.run(["python3", str(mock_script)], env=env, capture_output=True, text=True)
    assert result.returncode == 0

    # Scenario 6: User issues a pure command (no prefix), Agent executes a bash command.
    with open(transcript_path, "w") as f:
        f.write(json.dumps({"type": "USER_INPUT", "content": "git commit -m 'test'\n", "step_index": 8}) + "\n")
        f.write(json.dumps({"type": "PLANNER_RESPONSE", "content": "Doing it.", "tool_calls": [{"args": '{"CommandLine": "git commit -m test"}'}]}) + "\n")
        
    result = subprocess.run(["python3", str(mock_script)], env=env, capture_output=True, text=True)
    assert result.returncode == 1
    assert "CSI GUARDRAIL BLOCK" in result.stdout
    assert "Operator CTA" in result.stdout
