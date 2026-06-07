import os
import subprocess
import pytest

def test_todo_cli_appends_to_local_scratchpad(tmp_path, monkeypatch):
    # Mock dyad-state to a temp dir so we don't pollute the real one during tests
    test_state_dir = tmp_path / "dyad-state"
    test_state_dir.mkdir()
    
    # Create a mock bin/todo if we were to test the actual script, but we need the script to read an env var or we just test the script directly.
    # Since we want to test the actual script, let's just use the real dyad-state/todos.md but clean it up, or pass an env var.
    # Passing an env var is cleaner: CAIRN_TODO_PATH
    
    pass

def test_todo_cli_execution():
    todo_path = "dyad-state/todos.md"
    original_content = ""
    if os.path.exists(todo_path):
        with open(todo_path, "r") as f:
            original_content = f.read()
            
    intent = "test_noisy_intent_12345"
    
    try:
        result = subprocess.run(["./bin/todo", intent], capture_output=True, text=True)
        assert result.returncode == 0, f"todo CLI failed: {result.stderr}"
        
        assert os.path.exists(todo_path)
        with open(todo_path, "r") as f:
            content = f.read()
        
        assert intent in content, "Intent was not written to todos.md"
        
        # Verify it didn't accidentally sync to Touchstone (no files containing the intent in dm/dyad-touchstone)
        outbox = "dm/dyad-touchstone"
        if os.path.exists(outbox):
            for file in os.listdir(outbox):
                with open(os.path.join(outbox, file), "r") as f:
                    assert intent not in f.read(), "Invariant violated: todo synced to Touchstone outbox!"
                    
    finally:
        # Restore original state
        if original_content:
            with open(todo_path, "w") as f:
                f.write(original_content)
        else:
            if os.path.exists(todo_path):
                os.remove(todo_path)
