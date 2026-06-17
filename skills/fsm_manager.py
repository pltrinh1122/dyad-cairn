def validate_transition(current_state, next_state, valid_transitions):
    if next_state not in valid_transitions.get(current_state, []):
        raise ValueError(f"Invalid transition from {current_state} to {next_state}")
    return True
