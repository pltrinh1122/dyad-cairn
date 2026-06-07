import os
import yaml

class MatrixValidationError(Exception):
    """Exception raised when dip_state.yml fails physical invariant validation."""
    pass

def get_required_dimensions():
    """
    Dynamically extracts required dimensions from physical provenance (commons/AGENT.md).
    For now, returns an empty list or parses a file. The full implementation of this
    will be done by sibling probe (node_4b or a parser probe). 
    This function is explicitly mocked in the schema tests.
    """
    return []

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
