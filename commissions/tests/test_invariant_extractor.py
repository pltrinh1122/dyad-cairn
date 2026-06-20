import pytest
import os
import sys
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from commissions import invariant_extractor

def test_f1_determinism():
    """F-1: Two consecutive runs over identical sources differ by >=1 byte => REFUTED."""
    md_content = "<!-- INV bond:123 | test invariant -->\n"
    sidecar_content = "bond:123:\n  root_kind: constraint\n"
    
    with patch("commissions.invariant_extractor.get_git_sha", return_value="fake_sha"):
        out1 = invariant_extractor.run_extraction([md_content], sidecar_content)
        out2 = invariant_extractor.run_extraction([md_content], sidecar_content)
        assert out1 == out2

def test_f2_fail_closed_malformed_tag():
    """F-2: Malformed tag => halt with named state."""
    md_content = "<!-- INV bond:123 | test invariant " # unclosed tag
    with pytest.raises(SystemExit) as exc_info:
        invariant_extractor.run_extraction([md_content], "")
    assert exc_info.value.code == invariant_extractor.HALT_MALFORMED_TAG

def test_f4_no_semantic_drift():
    """F-4: Emitted one-liner must exactly match stored source one-liner."""
    md_content = "<!-- INV bond:abc |  My exact text   -->\n"
    sidecar_content = "bond:abc:\n  root_kind: constraint\n"
    out = invariant_extractor.run_extraction([md_content], sidecar_content)
    assert "My exact text" in out

def test_f8_merge_id_integrity_orphan_md():
    """F-8: Orphan tag (md id with no sidecar entry) => HALT."""
    md_content = "<!-- INV bond:orphan | test -->\n"
    sidecar_content = "bond:other:\n  root_kind: val\n"
    with pytest.raises(SystemExit) as exc_info:
        invariant_extractor.run_extraction([md_content], sidecar_content)
    assert exc_info.value.code == invariant_extractor.HALT_ORPHAN_TAG

def test_f8_merge_id_integrity_orphan_sidecar():
    """F-8: Orphan sidecar (sidecar id with no md tag) => HALT."""
    md_content = "<!-- INV bond:123 | test -->\n"
    sidecar_content = "bond:123:\n  root_kind: val\nbond:orphan:\n  root_kind: val\n"
    with pytest.raises(SystemExit) as exc_info:
        invariant_extractor.run_extraction([md_content], sidecar_content)
    assert exc_info.value.code == invariant_extractor.HALT_ORPHAN_SIDECAR

def test_a1_dirty_tree():
    """A-1: Dirty tree run => HALT."""
    with patch("commissions.invariant_extractor.is_git_clean", return_value=False):
        with pytest.raises(SystemExit) as exc_info:
            invariant_extractor.validate_preconditions()
        assert exc_info.value.code == invariant_extractor.HALT_DIRTY_TREE

def test_f1_2_determinism_sort():
    """F-1.2: Deterministic sort of dictionary keys."""
    md_content = "<!-- INV bond:123 | test -->\n"
    sidecar_content = "bond:123:\n  z: 1\n  a: 2\n"
    out = invariant_extractor.run_extraction([md_content], sidecar_content)
    # a should appear before z in the output
    assert out.find("a: 2") < out.find("z: 1")

def test_f2_2_fail_closed_dup_id():
    """F-2.2: Duplicate ID => HALT."""
    md_content = "<!-- INV bond:123 | test -->\n<!-- INV bond:123 | test2 -->\n"
    sidecar_content = "bond:123:\n  root_kind: constraint\n"
    with pytest.raises(SystemExit) as exc_info:
        invariant_extractor.run_extraction([md_content], sidecar_content)
    assert exc_info.value.code == invariant_extractor.HALT_DUPLICATE_ID

def test_f2_3_fail_closed_missing_source():
    """F-2.3: Missing source => HALT."""
    with pytest.raises(SystemExit) as exc_info:
        invariant_extractor.read_sources(["nonexistent_file.md"])
    assert exc_info.value.code == invariant_extractor.HALT_MISSING_SOURCE

def test_f3_staleness_guard():
    """F-3: Staleness guard exists in output."""
    md_content = "<!-- INV bond:123 | test -->\n"
    sidecar_content = "bond:123:\n  root_kind: constraint\n"
    with patch("commissions.invariant_extractor.get_git_sha", return_value="fake_sha"):
        out = invariant_extractor.run_extraction([md_content], sidecar_content)
    assert "_staleness_guard" in out
    assert "fake_sha" in out
