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
    # Since we lack a robust boundary marker, we limit the lookback to avoid 
    # soft-bricking on historical violations.
    steps = []
    with open(transcript_path, "r") as f:
        for line in f:
            if line.strip():
                try:
                    steps.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    steps = steps[-5:]
    
    for i, step in enumerate(steps):
        if step.get("type") == "USER_INPUT":
            content = step.get("content", "").strip()
            
            # Remove <USER_REQUEST> wrappers for parsing
            parsed_content = content.replace("<USER_REQUEST>", "").replace("</USER_REQUEST>", "").strip()
            
            # Check for `read:` naked defaults
            if parsed_content in ("read:", "read", "read."):
                used_read = False
                for j in range(i+1, len(steps)):
                    next_step = steps[j]
                    if next_step.get("type") == "USER_INPUT":
                        break
                    if next_step.get("type") == "PLANNER_RESPONSE":
                        tool_calls = next_step.get("tool_calls", [])
                        for tc in tool_calls:
                            if "bin/read quarries" in str(tc.get("args", "")):
                                used_read = True
                
                if not used_read:
                    violations.append(f"Violation at step {step.get('step_index')}: Operator issued a naked '{parsed_content}', but Agent failed to mechanically invoke './bin/read quarries'.")
            elif parsed_content.startswith("read:"):
                pass
                    
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
                        
            # CSI GUARD: The Batch Elicitation (/rub-all)
            if parsed_content.startswith("/rub all") or parsed_content.startswith("/rub-all"):
                for j in range(i+1, len(steps)):
                    next_step = steps[j]
                    if next_step.get("type") == "USER_INPUT":
                        break
                    if next_step.get("type") == "PLANNER_RESPONSE":
                        tool_calls = next_step.get("tool_calls", [])
                        for tc in tool_calls:
                            if tc.get("function", {}).get("name") == "default_api:ask_question":
                                try:
                                    args = json.loads(tc.get("function", {}).get("arguments", "{}"))
                                    if len(args.get("questions", [])) > 1:
                                        violations.append(f"Violation at step {step.get('step_index')}: Operator issued '/rub-all', but Agent batched multiple questions in ask_question. Agent must recursively invoke the individual /rub flow (WHY first) and not batch prompts.")
                                except:
                                    pass

            # CSI GUARD: Prevent Auto-Rub of Todos
            if parsed_content.startswith("todo:"):
                for j in range(i+1, len(steps)):
                    next_step = steps[j]
                    if next_step.get("type") == "USER_INPUT":
                        break
                    if next_step.get("type") == "PLANNER_RESPONSE":
                        tool_calls = next_step.get("tool_calls", [])
                        for tc in tool_calls:
                            if tc.get("function", {}).get("name") == "default_api:ask_question":
                                violations.append(f"Violation at step {step.get('step_index')}: Operator issued 'todo:', but Agent auto-invoked ask_question (Auto-Rub). Agent must quietly park the intent in the backlog without friction.")

            # Check for `reflect:`
            if parsed_content.startswith("reflect:"):
                used_retro = False
                ui_presented = False
                for j in range(i+1, len(steps)):
                    next_step = steps[j]
                    if next_step.get("type") == "USER_INPUT":
                        break
                    if next_step.get("type") == "PLANNER_RESPONSE":
                        tool_calls = next_step.get("tool_calls", [])
                        for tc in tool_calls:
                            if "bin/reflect" in str(tc.get("args", "")):
                                used_retro = True
                                
                        response_text = next_step.get("content", "")
                        if "📋 [MECHANICAL UI PRESENTATION: REFLECT SUMMARY]" in response_text:
                            ui_presented = True
                            
                if not used_retro:
                    violations.append(f"Violation at step {step.get('step_index')}: User issued 'reflect:' but Agent failed to mechanically invoke 'bin/reflect'.")
                if not ui_presented:
                    violations.append(f"Violation at step {step.get('step_index')}: Agent invoked 'bin/reflect' but failed to explicitly present the CSS template in the chat UI.")
                    
            # CSI GUARD: Operator CTA for Pure Commands
            # If Operator uses a raw command without a dialect prefix, the Agent must NOT silently execute it.
            # It must convert it to an Operator CTA.
            known_prefixes = ["read:", "read", "read.", "clip:", "clip", "clip.", "audit:", "rub:", "rub?", "reflect:", "lean:", "lean?", "lean", "lean.", "riff:", "execute:", "plan:", "probe:", "todo:", "report:", "/", "diff:", "fb:", "Y", "N", "yes", "no"]
            has_prefix = any(parsed_content.startswith(p) for p in known_prefixes)
            if not has_prefix and parsed_content:
                for j in range(i+1, len(steps)):
                    next_step = steps[j]
                    if next_step.get("type") == "USER_INPUT":
                        break
                    if next_step.get("type") == "PLANNER_RESPONSE":
                        tool_calls = next_step.get("tool_calls", [])
                        for tc in tool_calls:
                            # If the Agent uses `run_command` (CommandLine) directly, it's a violation.
                            if "CommandLine" in str(tc.get("args", "")) or "run_command" in tc.get("name", ""):
                                violations.append(f"Violation at step {step.get('step_index')}: Operator issued a pure command without a dialect prefix. Agent executed a raw command. Agent must convert this into an Operator CTA.")
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
