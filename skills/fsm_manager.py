import os
import sys
import yaml

class FSMManager:
    def __init__(self, state_file="artifacts/fsm_state.yml"):
        self.state_file = state_file
        self.state = {}
        
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                self.state = yaml.safe_load(f) or {}

def validate_transition(current_state, next_state, valid_transitions):
    if next_state not in valid_transitions.get(current_state, []):
        raise ValueError(f"Invalid transition from {current_state} to {next_state}")
    return True

def enforce_guard(transition_name: str, is_valid: bool = False):
    if not is_valid:
        print("==========================================================================")
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print(f"Illegal state transition attempted: {transition_name}")
        print("==========================================================================")
        sys.exit(1)

