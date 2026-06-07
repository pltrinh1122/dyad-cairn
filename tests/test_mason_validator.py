import pytest
import yaml
import tempfile
import os
from skills.mason_validator import validate_stone, install_stone, SecurityException

def test_validate_valid_stone():
    """Spec: A valid stone.yaml manifest must pass strict schema validation."""
    valid_yaml = """
    stone_id: hard-guardrails
    version: 1.0.0
    type: playbook
    assets:
      - source: payload.md
        destination: kb/HOW-0003-hard-guardrails.md
    invariants:
      - "No generative memory for structural constraints."
    """
    result = validate_stone(yaml.safe_load(valid_yaml))
    assert result.is_valid is True
    assert len(result.errors) == 0

def test_validate_missing_required_fields():
    """Spec: Manifest must contain stone_id, version, type, and assets."""
    invalid_yaml = """
    version: 1.0.0
    type: playbook
    """
    result = validate_stone(yaml.safe_load(invalid_yaml))
    assert result.is_valid is False
    assert any("Missing required field: stone_id" in e for e in result.errors)
    assert any("Missing required field: assets" in e for e in result.errors)

def test_install_stone_safe_destination_invariant():
    """Spec: The physical installation logic MUST resolve paths and violently halt if a destination escapes the allowed sandbox (kb/, skills/), even if path traversal (e.g., kb/../../.git) attempts to bypass string validation."""
    invalid_yaml = """
    stone_id: malicious-stone
    version: 1.0.0
    type: playbook
    assets:
      - source: script.sh
        destination: kb/../../.git/config
    """
    manifest = yaml.safe_load(invalid_yaml)
    with tempfile.TemporaryDirectory() as pkg_dir, tempfile.TemporaryDirectory() as target_dir:
        with pytest.raises(SecurityException) as excinfo:
            install_stone(pkg_dir, target_dir, manifest)
        assert "escapes the safe sandbox" in str(excinfo.value)

def test_install_stone_success():
    """Spec: The installation logic physically copies assets from the source package to the specified sandbox destinations."""
    valid_yaml = """
    stone_id: good-stone
    version: 1.0.0
    type: playbook
    assets:
      - source: script.py
        destination: skills/new_skill.py
    """
    manifest = yaml.safe_load(valid_yaml)
    with tempfile.TemporaryDirectory() as pkg_dir, tempfile.TemporaryDirectory() as target_dir:
        # Create the source file
        source_path = os.path.join(pkg_dir, "script.py")
        with open(source_path, "w") as f:
            f.write("print('hello')")
            
        install_stone(pkg_dir, target_dir, manifest)
        
        # Verify the destination file exists
        dest_path = os.path.join(target_dir, "skills/new_skill.py")
        assert os.path.exists(dest_path)
        with open(dest_path, "r") as f:
            assert f.read() == "print('hello')"
