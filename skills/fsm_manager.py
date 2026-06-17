import sys

def enforce_guard(transition_name: str, is_valid: bool = False):
    if not is_valid:
        print("==========================================================================")
        print("🚨 CONSISTENCY GUARDRAIL FIRED 🚨")
        print(f"Illegal state transition attempted: {transition_name}")
        print("==========================================================================")
        sys.exit(1)
