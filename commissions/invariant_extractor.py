import sys
import yaml
import re
import subprocess
import os

HALT_MALFORMED_TAG = 2
HALT_DUPLICATE_ID = 3
HALT_MISSING_SOURCE = 4
HALT_ORPHAN_TAG = 81
HALT_ORPHAN_SIDECAR = 82
HALT_DIRTY_TREE = 11

def is_git_clean():
    try:
        res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        return len(res.stdout.strip()) == 0
    except Exception:
        return False

def get_git_sha():
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
        return res.stdout.strip()
    except Exception:
        return "unknown"

def validate_preconditions():
    if not is_git_clean():
        sys.exit(HALT_DIRTY_TREE)

def read_sources(file_paths):
    contents = []
    for path in file_paths:
        if not os.path.exists(path):
            sys.exit(HALT_MISSING_SOURCE)
        with open(path, "r", encoding="utf-8") as f:
            contents.append(f.read())
    return contents

def run_extraction(md_contents, sidecar_content):
    try:
        sidecar = yaml.safe_load(sidecar_content) or {}
    except yaml.YAMLError:
        sidecar = {}

    tags = {}
    for content in md_contents:
        idx = 0
        while True:
            idx = content.find("<!-- INV", idx)
            if idx == -1:
                break
            
            end_idx = content.find("-->", idx)
            if end_idx == -1:
                sys.exit(HALT_MALFORMED_TAG)
                
            tag_text = content[idx:end_idx+3]
            m = re.match(r"<!--\s*INV\s+(bond:[^\s|]+)\s*\|\s*(.*?)\s*-->", tag_text)
            if not m:
                sys.exit(HALT_MALFORMED_TAG)
                
            tag_id = m.group(1)
            if tag_id in tags:
                sys.exit(HALT_DUPLICATE_ID)
                
            one_liner = m.group(2)
            tags[tag_id] = one_liner
            idx = end_idx + 3

    md_ids = set(tags.keys())
    sidecar_ids = set([k for k in sidecar.keys() if k != "_staleness_guard"])
    
    orphan_md = md_ids - sidecar_ids
    if orphan_md:
        sys.exit(HALT_ORPHAN_TAG)
        
    orphan_sidecar = sidecar_ids - md_ids
    if orphan_sidecar:
        sys.exit(HALT_ORPHAN_SIDECAR)
        
    output = {}
    output["_staleness_guard"] = {"pinned_sha": get_git_sha()}
    
    for tag_id in sorted(md_ids):
        item = dict(sidecar[tag_id])
        item["one_liner"] = tags[tag_id]
        sorted_item = {k: item[k] for k in sorted(item.keys())}
        output[tag_id] = sorted_item
        
    return yaml.dump(output, default_flow_style=False, sort_keys=False)

if __name__ == "__main__":
    pass
