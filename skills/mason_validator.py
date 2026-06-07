import os
import shutil
from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]

def validate_stone(manifest: Dict[str, Any]) -> ValidationResult:
    errors = []
    
    required_fields = ["stone_id", "version", "type", "assets"]
    for field in required_fields:
        if field not in manifest:
            errors.append(f"Missing required field: {field}")
            
    # If assets exist, validate their structure
    assets = manifest.get("assets", [])
    if isinstance(assets, list):
        for asset in assets:
            if not isinstance(asset, dict):
                errors.append("Asset must be a dictionary.")
                continue
            if "source" not in asset or "destination" not in asset:
                errors.append("Asset missing source or destination.")
    
    return ValidationResult(is_valid=len(errors) == 0, errors=errors)

class SecurityException(Exception):
    pass

def install_stone(pkg_dir: str, install_root_dir: str, manifest: Dict[str, Any]):
    # Ensure package is valid before installing
    result = validate_stone(manifest)
    if not result.is_valid:
        raise ValueError(f"Cannot install invalid stone: {result.errors}")
        
    allowed_dirs = [
        os.path.abspath(os.path.join(install_root_dir, "kb")),
        os.path.abspath(os.path.join(install_root_dir, "skills"))
    ]
    
    for asset in manifest["assets"]:
        dest_rel = asset["destination"]
        src_rel = asset["source"]
        
        dest_abs = os.path.abspath(os.path.join(install_root_dir, dest_rel))
        
        # Security: Physical Path Resolution Invariant
        is_safe = False
        for allowed in allowed_dirs:
            if dest_abs.startswith(allowed + os.sep) or dest_abs == allowed:
                is_safe = True
                break
                
        if not is_safe:
            raise SecurityException(f"Destination {dest_rel} escapes the safe sandbox.")
            
        src_abs = os.path.abspath(os.path.join(pkg_dir, src_rel))
        if not os.path.exists(src_abs):
            raise FileNotFoundError(f"Source asset {src_rel} not found in package.")
            
        # Create directories if needed
        os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
        shutil.copy2(src_abs, dest_abs)
