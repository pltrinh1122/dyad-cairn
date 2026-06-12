import sys
import subprocess
from unittest.mock import patch, call
from skills.lean_dispatcher import main

def test_lean_dispatcher_isolates_failures_and_continues(capsys):
    # Setup args for 2 targets
    test_args = ["./bin/lean", "todo_111", "todo_222"]
    
    with patch.object(sys, "argv", test_args):
        with patch("subprocess.run") as mock_run:
            # We want todo_111 to fail on convert-todo, and todo_222 to succeed
            def side_effect(args, **kwargs):
                if args == ["./bin/node", "convert-todo", "todo_111"]:
                    raise subprocess.CalledProcessError(1, args)
                return subprocess.CompletedProcess(args, 0)
            mock_run.side_effect = side_effect
            
            main()
            
    out, err = capsys.readouterr()
    # It should have continued to process todo_222 despite todo_111 failing
    assert "--- Processing todo_222 ---" in out
    # It should only prompt to execute the successful node
    assert "execute: node_todo_222" in out
    assert "execute: node_todo_111" not in out
    # It should print a CSI guard warning
    assert "CSI GUARD" in out
