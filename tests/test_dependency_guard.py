import os
import ast
import sys
import pytest

def get_stdlib_modules():
    return sys.stdlib_module_names

def parse_requirements():
    if not os.path.exists("requirements.txt"):
        return []
    reqs = []
    with open("requirements.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                # strip versions e.g., pyyaml==6.0 -> pyyaml
                pkg = line.split("=")[0].split(">")[0].split("<")[0]
                reqs.append(pkg.lower())
    return reqs

# Map of import names to package names if they differ
IMPORT_TO_PKG = {
    "yaml": "pyyaml"
}

def test_dependency_guard():
    """CSI Guard: Prevents Environmental Drift by asserting all non-stdlib imports are declared in requirements.txt"""
    stdlib = get_stdlib_modules()
    declared_reqs = parse_requirements()
    
    # Also add current dyad-cairn local packages
    local_pkgs = ["skills", "bin", "tests"]
    
    missing_declarations = set()
    
    for root_dir in ["skills", "bin", "tests"]:
        if not os.path.exists(root_dir):
            continue
        for subdir, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".py") or (root_dir == "bin" and not "." in file):
                    file_path = os.path.join(subdir, file)
                    with open(file_path, "r") as f:
                        try:
                            content = f.read()
                            tree = ast.parse(content)
                        except Exception:
                            continue # skip unparseable or non-python files
                            
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                base_mod = alias.name.split(".")[0]
                                if base_mod not in stdlib and base_mod not in local_pkgs:
                                    pkg_name = IMPORT_TO_PKG.get(base_mod, base_mod.lower())
                                    if pkg_name not in declared_reqs:
                                        missing_declarations.add((file_path, pkg_name))
                                        
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                base_mod = node.module.split(".")[0]
                                if base_mod not in stdlib and base_mod not in local_pkgs:
                                    pkg_name = IMPORT_TO_PKG.get(base_mod, base_mod.lower())
                                    if pkg_name not in declared_reqs:
                                        missing_declarations.add((file_path, pkg_name))

    if missing_declarations:
        err_msg = "🚨 DEPENDENCY DRIFT DETECTED 🚨\n"
        err_msg += "The following imports are missing from requirements.txt:\n"
        for file_path, pkg in missing_declarations:
            err_msg += f"  - {pkg} (imported in {file_path})\n"
        err_msg += "To DISARM this trap, add the missing packages to requirements.txt."
        pytest.fail(err_msg)
