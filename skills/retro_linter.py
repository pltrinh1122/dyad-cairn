import sys
import os
import re

def lint_retro(file_path):
    if not os.path.exists(file_path):
        print(f"[ERROR] Retro file not found: {file_path}")
        return False
        
    with open(file_path, 'r') as f:
        content = f.read()
        
    required_sections = [
        r"^## Continue\s*$",
        r"^## Start\s*$",
        r"^## Stop\s*$"
    ]
    
    missing = []
    for section in required_sections:
        if not re.search(section, content, re.MULTILINE):
            missing.append(section)
            
    if missing:
        print(f"[ERROR] Retro file {file_path} violates CSS template.")
        print(f"Missing required sections:")
        for m in missing:
            print(f"  - {m}")
        print("Please use kb/templates/retro.md to ensure Orthogonality Invariant compliance.")
        return False
        
    print(f"[PASS] Retro file {file_path} strictly adheres to CSS template.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 skills/retro_linter.py <path/to/retro.md>")
        sys.exit(1)
        
    success = lint_retro(sys.argv[1])
    if not success:
        sys.exit(1)
    sys.exit(0)
