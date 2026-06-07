import pytest
import tempfile
import yaml
import os
from skills.dip_sonar import validate_matrix, MatrixValidationError

def create_temp_yaml(data):
    fd, path = tempfile.mkstemp(suffix=".yml")
    with os.fdopen(fd, 'w') as f:
        yaml.dump(data, f)
    return path

def test_missing_file_raises_error():
    with pytest.raises(MatrixValidationError, match="Matrix file not found"):
        validate_matrix("nonexistent.yml")

def test_missing_dimension_raises_error(monkeypatch):
    # Mock provenance extraction: the required dimensions are dynamic
    monkeypatch.setattr("skills.dip_sonar.get_required_dimensions", lambda: ["1_identity", "2_externality"])
    data = {
        "dimensions": {
            "1_identity": {"content": "foo", "status": "APPROVED", "operator_signature": "timestamp"}
            # missing 2_externality
        }
    }
    path = create_temp_yaml(data)
    try:
        with pytest.raises(MatrixValidationError, match="Missing required dimension: 2_externality"):
            validate_matrix(path)
    finally:
        os.remove(path)

def test_approved_requires_signature(monkeypatch):
    monkeypatch.setattr("skills.dip_sonar.get_required_dimensions", lambda: ["1_identity"])
    data = {
        "dimensions": {
            "1_identity": {"content": "foo", "status": "APPROVED", "operator_signature": None} # Invalid!
        }
    }
    path = create_temp_yaml(data)
    try:
        with pytest.raises(MatrixValidationError, match="Dimension 1_identity is APPROVED but lacks an operator_signature"):
            validate_matrix(path)
    finally:
        os.remove(path)

def test_deferred_status_is_valid(monkeypatch):
    monkeypatch.setattr("skills.dip_sonar.get_required_dimensions", lambda: ["1_identity"])
    data = {
        "dimensions": {
            "1_identity": {"content": "Not ready yet", "status": "DEFERRED", "operator_signature": "timestamp"} 
        }
    }
    path = create_temp_yaml(data)
    try:
        # DEFERRED is structurally valid for instantiation
        result = validate_matrix(path)
        assert result is True
    finally:
        os.remove(path)

def test_tripartite_structure_enforced(monkeypatch):
    monkeypatch.setattr("skills.dip_sonar.get_required_dimensions", lambda: ["1_identity"])
    data = {
        "dimensions": {
            "1_identity": {"content": "foo", "operator_signature": None} # missing status
        }
    }
    path = create_temp_yaml(data)
    try:
        with pytest.raises(MatrixValidationError, match="Dimension 1_identity is missing required tripartite key: status"):
            validate_matrix(path)
    finally:
        os.remove(path)

def test_valid_matrix_passes(monkeypatch):
    monkeypatch.setattr("skills.dip_sonar.get_required_dimensions", lambda: ["1_identity", "2_externality"])
    # Fully saturated, valid matrix
    data = {
        "dimensions": {
            "1_identity": {"content": "foo", "status": "APPROVED", "operator_signature": "2026-06"},
            "2_externality": {"content": "bar", "status": "APPROVED", "operator_signature": "2026-06"},
        }
    }
    path = create_temp_yaml(data)
    try:
        # Should return True, no exception
        result = validate_matrix(path)
        assert result is True
    finally:
        os.remove(path)
