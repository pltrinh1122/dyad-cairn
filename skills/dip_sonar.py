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
        
    raise NotImplementedError("Executioner must implement the parser to extract dimensions from markdown.")

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
