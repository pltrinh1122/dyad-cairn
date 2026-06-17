import sys

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
