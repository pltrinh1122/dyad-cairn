#!/bin/bash
# Dyad shell hooks to enforce mechanical closure when exiting CLI platforms.
# Source this file in your ~/.bashrc or ~/.zshrc:
# source /path/to/dyad-cairn/bin/dyad-shell-hooks.sh

agy_dyad() {
    agy "$@"
    
    # Mechanical closure hook: Ensure the FSM transitions correctly on exit
    if [ -f "./bin/exit" ]; then
        echo "[DYAD] Mechanical closure triggered via shell hook."
        ./bin/exit
    fi
}

claude_dyad() {
    claude "$@"
    
    if [ -f "./bin/exit" ]; then
        echo "[DYAD] Mechanical closure triggered via shell hook."
        ./bin/exit
    fi
}

# Optional: Set default aliases if desired.
# alias agy="agy_dyad"
# alias claude="claude_dyad"
