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
            
            # Remove <USER_REQUEST> wrappers for parsing
            parsed_content = content.replace("<USER_REQUEST>", "").replace("</USER_REQUEST>", "").strip()
            
            # Check for `read:`
            if parsed_content.startswith("read:"):
                used_read = False
                for j in range(i+1, len(steps)):
                    next_step = steps[j]
                    if next_step.get("type") == "USER_INPUT":
                        break
                    if next_step.get("type") == "PLANNER_RESPONSE":
                        tool_calls = next_step.get("tool_calls", [])
                        for tc in tool_calls:
                            if "bin/read" in str(tc.get("args", "")):
                                used_read = True
                                
                if not used_read:
                    violations.append(f"Violation at step {step.get('step_index')}: User issued 'read:' but Agent generated output without invoking 'bin/read'.")
                    
            # CSI GUARD: The Asymmetric Downgrade Invariant
            # If Operator explicitly asserts `audit:`, the Agent is mechanically forbidden
            # from silently downgrading it to a passive `todo:`.
            if parsed_content.startswith("audit:"):
                for j in range(i+1, len(steps)):
                    next_step = steps[j]
                    if next_step.get("type") == "USER_INPUT":
                        break
                    if next_step.get("type") == "PLANNER_RESPONSE":
                        tool_calls = next_step.get("tool_calls", [])
                        for tc in tool_calls:
                            if "bin/todo" in str(tc.get("args", "")):
                                violations.append(f"Violation at step {step.get('step_index')}: CSI Downgrade Guard Tripped. Operator issued 'audit:', but Agent attempted to execute 'bin/todo'. Agent must execute 'bin/audit' or issue a conversational Rub-Back.")

            # CSI GUARD: The Disambiguation of Rub (Interrogation)
            if parsed_content.startswith("rub?"):
                for j in range(i+1, len(steps)):
                    next_step = steps[j]
                    if next_step.get("type") == "USER_INPUT":
                        break
                    if next_step.get("type") == "PLANNER_RESPONSE":
                        tool_calls = next_step.get("tool_calls", [])
                        for tc in tool_calls:
                            if "bin/" in str(tc.get("args", "")):
                                violations.append(f"Violation at step {step.get('step_index')}: Operator issued 'rub?' requesting a Conversational Rub-Back, but Agent executed a script. Agent must not execute scripts when 'rub?' is used.")
                        
            # Check for `retro:`
            if parsed_content.startswith("retro:"):
                used_retro = False
                ui_presented = False
                for j in range(i+1, len(steps)):
                    next_step = steps[j]
                    if next_step.get("type") == "USER_INPUT":
                        break
                    if next_step.get("type") == "PLANNER_RESPONSE":
                        tool_calls = next_step.get("tool_calls", [])
                        for tc in tool_calls:
                            if "bin/retro" in str(tc.get("args", "")):
                                used_retro = True
                                
                        response_text = next_step.get("content", "")
                        if "📋 [MECHANICAL UI PRESENTATION: RETRO SUMMARY]" in response_text:
                            ui_presented = True
                            
                if not used_retro:
                    violations.append(f"Violation at step {step.get('step_index')}: User issued 'retro:' but Agent failed to mechanically invoke 'bin/retro'.")
                if not ui_presented:
                    violations.append(f"Violation at step {step.get('step_index')}: Agent invoked 'bin/retro' but failed to explicitly present the CSS template in the chat UI.")
                        
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
