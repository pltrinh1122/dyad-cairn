import os
import re

def replace_in_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex replacements preserving case where appropriate
    new_content = re.sub(r'\bretro\b', 'reflect', content)
    new_content = re.sub(r'\bRetro\b', 'Reflect', new_content)
    new_content = re.sub(r'\bRETRO\b', 'REFLECT', new_content)
    new_content = re.sub(r'retro_linter', 'reflect_linter', new_content)
    new_content = re.sub(r'retro_msg', 'reflect_msg', new_content)
    new_content = re.sub(r'retro\.md', 'reflect.md', new_content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, _, files in os.walk('.'):
    if '.git' in root or 'scratch' in root or '__pycache__' in root:
        continue
    for file in files:
        if file.endswith('.py') or file.endswith('.md') or file.endswith('.sh') or file.endswith('.jsonl') or file in ['retro', 'd-reflect', 'gh', 'd-rub', 'd-land']:
            replace_in_file(os.path.join(root, file))

# Rename files
renames = [
    ('bin/retro', 'bin/reflect'),
    ('skills/retro_linter.py', 'skills/reflect_linter.py'),
    ('kb/templates/retro.md', 'kb/templates/reflect.md'),
    ('dyad-state/retro.md', 'dyad-state/reflect.md'),
    ('tests/test_retro_cli.py', 'tests/test_reflect_cli.py')
]

for old, new in renames:
    if os.path.exists(old):
        os.rename(old, new)
        print(f"Renamed {old} -> {new}")
