#!/bin/bash
set -e
TODO_OUT=$(./bin/todo "Formalize Transient Script Invariant for compound bash commands")
TODO_ID=$(echo "$TODO_OUT" | grep -o "todo_[0-9.]*_[a-z0-9]*" | head -n 1)
echo "Created TODO_ID: $TODO_ID"
./bin/rub "$TODO_ID" --what "Encode the Transient Script Invariant into DYAD.md to prevent execution of compound bash commands (>2 commands)" --why "To eliminate parsing fragility and prevent the silent masking of intermediate execution failures" --scope "FRONTIER"
