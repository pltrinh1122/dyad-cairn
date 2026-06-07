import os
import yaml
import re

class MatrixValidationError(Exception):
    """Exception raised when dip_state.yml fails physical invariant validation."""
    pass

class ProvenanceExtractionError(Exception):
    """Exception raised when provenance extraction fails."""
    pass

def get_required_dimensions(provenance_path=None):
    """
    Dynamically extracts required dimensions from physical provenance.
    """
    if provenance_path is None:
        provenance_path = "commons/AGENT.md"
        
    if not os.path.exists(provenance_path):
        raise ProvenanceExtractionError("Provenance file not found")
        
    with open(provenance_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    dimensions = []
    pattern = re.compile(r"\|\s*(\d+)\s*\|\s*(?:\*\*)?([^|*]+?)(?:\*\*)?\s*\|")
    for line in content.splitlines():
        match = pattern.search(line)
        if match:
            idx = match.group(1).strip()
            raw_dim = match.group(2).strip()
            sanitized_dim = raw_dim.lower().replace(" ", "_").replace("-", "_")
            dimensions.append(f"{idx}_{sanitized_dim}")
            
    if not dimensions:
        raise ProvenanceExtractionError("Failed to extract dimension table from provenance")
        
    return dimensions

def validate_matrix(file_path):
    if not os.path.exists(file_path):
        raise MatrixValidationError("Matrix file not found")
        
    with open(file_path, "r") as f:
        data = yaml.safe_load(f) or {}
        
    dimensions = data.get("dimensions", {})
    required = get_required_dimensions()
    
    # Invariant: Completeness
    for req in required:
        if req not in dimensions:
            raise MatrixValidationError(f"Missing required dimension: {req}")
            
    # Invariant: Tripartite Structure
    required_keys = ["content", "status", "operator_signature"]
    for dim_name, dim_data in dimensions.items():
        if not isinstance(dim_data, dict):
            raise MatrixValidationError(f"Dimension {dim_name} must be a dictionary")
            
        for key in required_keys:
            if key not in dim_data:
                raise MatrixValidationError(f"Dimension {dim_name} is missing required tripartite key: {key}")
                
        status = dim_data["status"]
        sig = dim_data["operator_signature"]
        
        # Invariant: Status specific rules
        if status in ("APPROVED", "DEFERRED") and sig is None:
            raise MatrixValidationError(f"Dimension {dim_name} is {status} but lacks an operator_signature")
            
    return True
