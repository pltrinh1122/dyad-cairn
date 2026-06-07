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

def test_missing_dimension_raises_error():
    # Construct a payload missing '2_externality'
    data = {
        "dimensions": {
            "1_identity": {"content": "foo", "status": "APPROVED", "operator_signature": "timestamp"},
            "3_form_grounding": {"content": None, "status": "EMPTY", "operator_signature": None},
            "4_channel_discipline": {"content": None, "status": "EMPTY", "operator_signature": None},
            "5_non_negotiable": {"content": None, "status": "EMPTY", "operator_signature": None},
            "6_ontology_starter": {"content": None, "status": "EMPTY", "operator_signature": None},
            "7_vocabulary_stub": {"content": None, "status": "EMPTY", "operator_signature": None},
        }
    }
    path = create_temp_yaml(data)
    try:
        with pytest.raises(MatrixValidationError, match="Missing required dimension: 2_externality"):
            validate_matrix(path)
    finally:
        os.remove(path)

def test_approved_requires_signature():
    # If status is APPROVED, signature cannot be None
    data = {
        "dimensions": {
            "1_identity": {"content": "foo", "status": "APPROVED", "operator_signature": None}, # Invalid!
            "2_externality": {"content": None, "status": "EMPTY", "operator_signature": None},
            "3_form_grounding": {"content": None, "status": "EMPTY", "operator_signature": None},
            "4_channel_discipline": {"content": None, "status": "EMPTY", "operator_signature": None},
            "5_non_negotiable": {"content": None, "status": "EMPTY", "operator_signature": None},
            "6_ontology_starter": {"content": None, "status": "EMPTY", "operator_signature": None},
            "7_vocabulary_stub": {"content": None, "status": "EMPTY", "operator_signature": None},
        }
    }
    path = create_temp_yaml(data)
    try:
        with pytest.raises(MatrixValidationError, match="Dimension 1_identity is APPROVED but lacks an operator_signature"):
            validate_matrix(path)
    finally:
        os.remove(path)

def test_tripartite_structure_enforced():
    # Dimension missing 'status' entirely
    data = {
        "dimensions": {
            "1_identity": {"content": "foo", "operator_signature": None}, # missing status
            "2_externality": {"content": None, "status": "EMPTY", "operator_signature": None},
            "3_form_grounding": {"content": None, "status": "EMPTY", "operator_signature": None},
            "4_channel_discipline": {"content": None, "status": "EMPTY", "operator_signature": None},
            "5_non_negotiable": {"content": None, "status": "EMPTY", "operator_signature": None},
            "6_ontology_starter": {"content": None, "status": "EMPTY", "operator_signature": None},
            "7_vocabulary_stub": {"content": None, "status": "EMPTY", "operator_signature": None},
        }
    }
    path = create_temp_yaml(data)
    try:
        with pytest.raises(MatrixValidationError, match="Dimension 1_identity is missing required tripartite key: status"):
            validate_matrix(path)
    finally:
        os.remove(path)

def test_valid_matrix_passes():
    # Fully saturated, valid matrix
    data = {
        "dimensions": {
            "1_identity": {"content": "foo", "status": "APPROVED", "operator_signature": "2026-06"},
            "2_externality": {"content": "bar", "status": "APPROVED", "operator_signature": "2026-06"},
            "3_form_grounding": {"content": "baz", "status": "APPROVED", "operator_signature": "2026-06"},
            "4_channel_discipline": {"content": "qux", "status": "APPROVED", "operator_signature": "2026-06"},
            "5_non_negotiable": {"content": "norf", "status": "APPROVED", "operator_signature": "2026-06"},
            "6_ontology_starter": {"content": "corge", "status": "APPROVED", "operator_signature": "2026-06"},
            "7_vocabulary_stub": {"content": "grault", "status": "APPROVED", "operator_signature": "2026-06"},
        }
    }
    path = create_temp_yaml(data)
    try:
        # Should return True, no exception
        result = validate_matrix(path)
        assert result is True
    finally:
        os.remove(path)
