import os

file_path = "skills/flow_state_manager.py"
with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    
    # 1. Sovereignty
    if "Any mutations to the mason schema must now be treated as external blockers." in line:
        new_lines.append('        print("[STEERING VECTOR] Synchronize with the Commons using `./bin/sync-commons` or pull upstream changes to resolve this blockage.")\n')
        
    # 2. Audit Lock
    if "the Audit DAG is physically cleared (all nodes DONE)." in line:
        new_lines.append('                print("[STEERING VECTOR] Execute the Audit DAG. Run `python3 skills/quarry_reader.py` to identify failing audits and resolve them.")\n')
        
    # 3. reflect_node_red unhandled exception
    if "TDD execution threw an unhandled exception. Fix syntax errors before reflecting red." in line:
        new_lines.append('        print("[STEERING VECTOR] Inspect the traceback above, correct the syntax or import errors in your test file, and rerun the command.")\n')
        
    # 4. reflect_node_red structural guard
    if "You are mechanically forbidden from generating an Intent PR until the substrate is physically unblocked." in line:
        new_lines.append('        print("[STEERING VECTOR] Read the specific CSI Guard message above, perform the required remediation, and rerun.")\n')
        
    # 5. reflect_node_red tests passed
    if "Tests PASSED in the Red phase. You must write failing tests that map to Operator intent before reflecting." in line:
        new_lines.append('        print("[STEERING VECTOR] Write at least one failing test in `tests/` that asserts the new behavior, then rerun this command.")\n')
        
    # 6. dialect linter
    if "The Agent must physically run the UI presentation tools. You are blocked." in line or "The Agent must physically run the UI presentation tools. You are blocked from Completion." in line:
        new_lines.append('        print("[STEERING VECTOR] Fix the formatting or dialect issues flagged by the linter above, then rerun.")\n')
        
    # 7. missing RCA
    if "Missing RCA artifact. EXECUTE nodes must author an industry standard RCA at" in line:
        new_lines.append('            print(f"[STEERING VECTOR] Create the file `{rca_file}` detailing the Root Cause Analysis, then rerun.")\n')
        
    # 8. reflect_node_green TDD failed to run
    if "TDD execution failed. The PR Gate is mechanically sealed until tests pass." in line or "TDD execution failed to run. You cannot complete an EXECUTE node without passing tests." in line:
        new_lines.append('        print("[STEERING VECTOR] Inspect the test traceback, fix the syntax or import errors, and rerun.")\n')
        
    # 9. reflect_node_green structural guard
    if "You are mechanically forbidden from generating a Green PR until the substrate is physically unblocked." in line or "A structural CSI Guard was tripped. You cannot complete this node." in line:
        new_lines.append('        print("[STEERING VECTOR] Read the specific CSI Guard message above, perform the required remediation, and rerun.")\n')
        
    # 10. reflect_node_green tests failed
    if "Tests failed. You are mathematically forbidden from generating a Green PR." in line or "Tests failed. The Testing Invariant is violated. You are mechanically forbidden from closing this node." in line:
        new_lines.append('        print("[STEERING VECTOR] Inspect the failing test output, fix the implementation so the tests pass, and rerun.")\n')
        
    # 11. remote GAP failed Green
    if "This indicates a Survivor Bias split-brain (e.g. environmental drift)." in line:
        new_lines.append('            print("[STEERING VECTOR] Run `gh pr checks` to identify the failing remote job. Fix the environmental mismatch, push the commit, and rerun.")\n')
        
    # 12. remote GAP passed Red
    if "Tests must fail in the remote environment to validate the Intent Gate." in line:
        new_lines.append('            print("[STEERING VECTOR] Write failing tests, push them to the branch, ensure GAP fails, and rerun.")\n')
        
    # 13. Missing trail synthesis
    if "Missing Trail Synthesis artifact. REFLECT nodes must author" in line:
        new_lines.append('        print(f"[STEERING VECTOR] Create the file `{synthesis_file}` with the required synthesis narrative, then rerun.")\n')
        
    # 14. Trail Synthesis validation
    if "Trail Synthesis must contain a narrative summary for (1) positive assertion of the Probe Invariant and (2) reference to individual Execution RCA." in line:
        new_lines.append('        print("[STEERING VECTOR] Update the trail synthesis document to include both the Probe Invariant assertion and references to the Execution RCAs, then rerun.")\n')

with open(file_path, "w") as f:
    f.writelines(new_lines)
