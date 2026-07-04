import sys
import yaml
import re
import subprocess
import os
import argparse

HALT_MALFORMED_TAG = 2
HALT_DUPLICATE_ID = 3
HALT_MISSING_SOURCE = 4
HALT_DIRTY_TREE = 11
HALT_ENCODING_EOL = 12
HALT_GRAMMAR_VERSION = 13
HALT_TOCTOU = 14
HALT_ORPHAN_TAG = 81
HALT_ORPHAN_SIDECAR = 82
HALT_DANGLING_EDGE = 83
HALT_CROSS_HOME_DUP = 84
HALT_STALE_SOURCE = 15

class UniqueKeyLoader(yaml.SafeLoader):
    pass

def construct_mapping(loader, node):
    loader.flatten_mapping(node)
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=False)
        if key in mapping:
            sys.exit(HALT_CROSS_HOME_DUP)
        mapping[key] = loader.construct_object(value_node, deep=False)
    return mapping

UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)

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

def get_file_sha(path):
    try:
        res = subprocess.run(["git", "hash-object", path], capture_output=True, text=True)
        return res.stdout.strip()
    except Exception:
        return "unknown"

def verify_staleness(yaml_data, current_shas):
    guard = yaml_data.get("_staleness_guard")
    if not guard:
        return
    source_shas = guard.get("source_shas", {})
    for path, sha in source_shas.items():
        if path in current_shas and current_shas[path] != sha:
            import sys
            sys.exit(15)

def validate_preconditions():
    if not is_git_clean():
        sys.exit(HALT_DIRTY_TREE)

def read_sources(file_paths):
    contents = []
    shas = {}
    for path in file_paths:
        if not os.path.exists(path):
            sys.exit(HALT_MISSING_SOURCE)
        
        sha_before = get_file_sha(path)
        
        with open(path, "rb") as f:
            raw = f.read()
            if b"\r\n" in raw:
                sys.exit(HALT_ENCODING_EOL)
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                sys.exit(HALT_ENCODING_EOL)
                
        sha_after = get_file_sha(path)
        if sha_before != sha_after:
            sys.exit(HALT_TOCTOU)
            
        contents.append(text)
        shas[path] = sha_after
    return contents, shas

def run_extraction(md_contents, shas, sidecar_content, dyad_prefix):
    try:
        sidecar = yaml.load(sidecar_content, Loader=UniqueKeyLoader) or {}
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
            
            if not tag_text.startswith("<!-- INV@v1 "):
                sys.exit(HALT_GRAMMAR_VERSION)
                
            escaped_prefix = re.escape(dyad_prefix)
            pattern = r"<!--\s*INV@v1\s+(" + escaped_prefix + r":[^\s|]+)\s*\|\s*(.*?)\s*-->"
            m = re.match(pattern, tag_text)
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
        
    for tag_id, attrs in sidecar.items():
        if tag_id == "_staleness_guard":
            continue
        if "grounded_in" in attrs:
            grounded = attrs["grounded_in"]
            if isinstance(grounded, list):
                for ref in grounded:
                    if ref not in md_ids:
                        sys.exit(HALT_DANGLING_EDGE)
            elif isinstance(grounded, str):
                if grounded not in md_ids:
                    sys.exit(HALT_DANGLING_EDGE)
    
    output = {}
    
    class_b_header = {
        "B-1": "tagging-completeness (tagged = the whole invariant class)",
        "B-2": "one-liner fidelity (stored one-liner faithfully compresses its full text)",
        "B-3": "single-home integrity (no untagged paraphrase drifting elsewhere)",
        "B-4": "status truthfulness (status=ratified reflects a real ratification)"
    }
    
    output["_class_b_assumptions"] = class_b_header
    output["_staleness_guard"] = {
        "pinned_commit_sha": get_git_sha(),
        "source_shas": shas
    }
    
    for tag_id in sorted(md_ids):
        item = dict(sidecar[tag_id])
        item["one_liner"] = tags[tag_id]
        sorted_item = {k: item[k] for k in sorted(item.keys())}
        output[tag_id] = sorted_item
        
    return yaml.dump(output, default_flow_style=False, sort_keys=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract invariants from markdown and merge with sidecar yaml.")
    parser.add_argument("--dyad", type=str, required=True, help="The dyad prefix for the invariant IDs (e.g., 'bond').")
    parser.add_argument("--sidecar", type=str, required=True, help="Path to the structure sidecar yaml file.")
    parser.add_argument("sources", nargs="+", help="Paths to markdown source files.")
    
    args = parser.parse_args()
    
    validate_preconditions()
    
    if not os.path.exists(args.sidecar):
        sys.exit(HALT_MISSING_SOURCE)
        
    with open(args.sidecar, "rb") as f:
        sidecar_content = f.read()
        
    contents, shas = read_sources(args.sources)
    shas[args.sidecar] = get_file_sha(args.sidecar)
    
    out_yaml = run_extraction(contents, shas, sidecar_content, args.dyad)
    print(out_yaml)
