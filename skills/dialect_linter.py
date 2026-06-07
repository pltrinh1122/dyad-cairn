import os
import json
import sys

def audit_dialect():
    conv_id = os.environ.get("ANTIGRAVITY_CONVERSATION_ID")
    if not conv_id:
        print("[LINTER] No ANTIGRAVITY_CONVERSATION_ID found. Skipping dialect audit.")
        return 0
        
    transcript_path = os.path.expanduser(f"~/.gemini/antigravity-cli/brain/{conv_id}/.system_generated/logs/transcript.jsonl")
    
    if not os.path.exists(transcript_path):
        print(f"[LINTER] Transcript not found at {transcript_path}. Skipping.")
        return 0
        
    violations = []
    
    # We want to audit the transcript for the current node. 
    # For simplicity, we just audit the last 50 steps.
    steps = []
    with open(transcript_path, "r") as f:
        for line in f:
            if line.strip():
                steps.append(json.loads(line))
                
    steps = steps[-50:]
    
    for i, step in enumerate(steps):
        if step.get("type") == "USER_INPUT":
            content = step.get("content", "").strip()
            
            # Check for `read:`
            if content.startswith("read:"):
                # The next PLANNER_RESPONSE should contain a tool call to bin/read
                # Find the next PLANNER_RESPONSE
                for j in range(i+1, len(steps)):
                    next_step = steps[j]
                    if next_step.get("type") == "PLANNER_RESPONSE":
                        # Check tool calls
                        tool_calls = next_step.get("tool_calls", [])
                        used_read = False
                        for tc in tool_calls:
                            # Look for 'bin/read' in the arguments
                            args = str(tc.get("argumentsJson", ""))
                            if "bin/read" in args:
                                used_read = True
                                break
                                
                        if not used_read:
                            violations.append(f"Violation at step {step.get('step_index')}: User issued 'read:' but Agent generated output without invoking 'bin/read'.")
                        break
                        
    if violations:
        print("🚨 CSI GUARDRAIL BLOCK: UI Invariant Violation 🚨")
        for v in violations:
            print(f"- {v}")
        print("The Agent generated raw markdown instead of physically invoking the mechanical UI tools.")
        return 1
        
    print("[PASS] No UI Dialect violations detected.")
    return 0

if __name__ == "__main__":
    sys.exit(audit_dialect())
