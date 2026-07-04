import pytest
import os
import sys
import yaml
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from commissions import invariant_extractor

def test_f1_determinism():
    """F-1: Two consecutive runs over identical sources differ by >=1 byte => REFUTED."""
    md_content = "<!-- INV@v1 bond:123 | test invariant -->\n"
    sidecar_content = b"bond:123:\n  root_kind: constraint\n"
    
    shas = {"fake.md": "sha1"}
    with patch("commissions.invariant_extractor.get_git_sha", return_value="fake_sha"):
        out1 = invariant_extractor.run_extraction([md_content], shas, sidecar_content, "bond")
        out2 = invariant_extractor.run_extraction([md_content], shas, sidecar_content, "bond")
        assert out1 == out2

def test_f2_fail_closed_malformed_tag():
    """F-2: Malformed tag => halt with named state."""
    md_content = "<!-- INV@v1 bond:123 | test invariant " # unclosed tag
    with pytest.raises(SystemExit) as exc_info:
        invariant_extractor.run_extraction([md_content], {}, b"", "bond")
    assert exc_info.value.code == invariant_extractor.HALT_MALFORMED_TAG

def test_f4_no_semantic_drift():
    """F-4: Emitted one-liner must exactly match stored source one-liner."""
    md_content = "<!-- INV@v1 bond:abc |  My exact text   -->\n"
    sidecar_content = b"bond:abc:\n  root_kind: constraint\n"
    out = invariant_extractor.run_extraction([md_content], {}, sidecar_content, "bond")
    assert "My exact text" in out

def test_f8_merge_id_integrity_orphan_md():
    """F-8: Orphan tag (md id with no sidecar entry) => HALT."""
    md_content = "<!-- INV@v1 bond:orphan | test -->\n"
    sidecar_content = b"bond:other:\n  root_kind: val\n"
    with pytest.raises(SystemExit) as exc_info:
        invariant_extractor.run_extraction([md_content], {}, sidecar_content, "bond")
    assert exc_info.value.code == invariant_extractor.HALT_ORPHAN_TAG

def test_f8_merge_id_integrity_orphan_sidecar():
    """F-8: Orphan sidecar (sidecar id with no md tag) => HALT."""
    md_content = "<!-- INV@v1 bond:123 | test -->\n"
    sidecar_content = b"bond:123:\n  root_kind: val\nbond:orphan:\n  root_kind: val\n"
    with pytest.raises(SystemExit) as exc_info:
        invariant_extractor.run_extraction([md_content], {}, sidecar_content, "bond")
    assert exc_info.value.code == invariant_extractor.HALT_ORPHAN_SIDECAR

def test_a1_dirty_tree():
    """A-1: Dirty tree run => HALT."""
    with patch("commissions.invariant_extractor.is_git_clean", return_value=False):
        with pytest.raises(SystemExit) as exc_info:
            invariant_extractor.validate_preconditions()
        assert exc_info.value.code == invariant_extractor.HALT_DIRTY_TREE

def test_f1_2_sha_determinism():
    """F-1.2: Two runs over identical source shas differ >=1 byte => REFUTED."""
    md_content = "<!-- INV@v1 bond:123 | test -->\n"
    sidecar_content = b"bond:123:\n  z: 1\n  a: 2\n"
    shas1 = {"fake.md": "sha1"}
    shas2 = {"fake.md": "sha1"} # Exact same content but a different dictionary object
    with patch("commissions.invariant_extractor.get_git_sha", return_value="fake_sha"):
        out1 = invariant_extractor.run_extraction([md_content], shas1, sidecar_content, "bond")
        out2 = invariant_extractor.run_extraction([md_content], shas2, sidecar_content, "bond")
    assert out1 == out2

def test_f2_2_fail_closed_dup_id():
    """F-2.2: Duplicate ID => HALT."""
    md_content = "<!-- INV@v1 bond:123 | test -->\n<!-- INV@v1 bond:123 | test2 -->\n"
    sidecar_content = b"bond:123:\n  root_kind: constraint\n"
    with pytest.raises(SystemExit) as exc_info:
        invariant_extractor.run_extraction([md_content], {}, sidecar_content, "bond")
    assert exc_info.value.code == invariant_extractor.HALT_DUPLICATE_ID

def test_f2_3_fail_closed_missing_source():
    """F-2.3: Missing source => HALT."""
    with pytest.raises(SystemExit) as exc_info:
        invariant_extractor.read_sources(["nonexistent_file.md"])
    assert exc_info.value.code == invariant_extractor.HALT_MISSING_SOURCE

def test_f3_staleness_guard():
    """F-3: Staleness guard arms on mutated sha."""
    md_content = "<!-- INV@v1 bond:123 | test -->\n"
    sidecar_content = b"bond:123:\n  root_kind: constraint\n"
    with patch("commissions.invariant_extractor.get_git_sha", return_value="fake_sha"):
        out = invariant_extractor.run_extraction([md_content], {"f": "s1"}, sidecar_content, "bond")
    
    out_data = yaml.safe_load(out)
    with pytest.raises(SystemExit) as exc_info:
        invariant_extractor.verify_staleness(out_data, {"f": "s2"})
    assert exc_info.value.code == invariant_extractor.HALT_STALE_SOURCE

def test_f7_2_encoding_eol(tmp_path):
    """F-7.2: encoding/EOL -> halt."""
    md = tmp_path / "source.md"
    with open(md, "wb") as f:
        f.write(b"<!-- INV@v1 bond:123 | a -->\r\n")
    
    with patch("commissions.invariant_extractor.get_file_sha", return_value="sha"):
        with pytest.raises(SystemExit) as exc_info:
            invariant_extractor.read_sources([str(md)])
        assert exc_info.value.code == invariant_extractor.HALT_ENCODING_EOL

def test_f7_3_grammar_version():
    """F-7.3: grammar version mismatch -> halt."""
    md_content = "<!-- INV bond:123 | hello -->\n" # Missing @v1
    with pytest.raises(SystemExit) as exc_info:
        invariant_extractor.run_extraction([md_content], {}, b"", "bond")
    assert exc_info.value.code == invariant_extractor.HALT_GRAMMAR_VERSION

def test_f7_4_mid_scan_toctou(tmp_path):
    """F-7.4: mid scan TOCTOU -> halt."""
    md = tmp_path / "source.md"
    md.write_text("hello\n", encoding="utf-8")
    
    shas = ["sha_before", "sha_after"]
    def mock_get_file_sha(path):
        return shas.pop(0)
        
    with patch("commissions.invariant_extractor.get_file_sha", side_effect=mock_get_file_sha):
        with pytest.raises(SystemExit) as exc_info:
            invariant_extractor.read_sources([str(md)])
        assert exc_info.value.code == invariant_extractor.HALT_TOCTOU

def test_f8_3_dangling_edge():
    """F-8.3: dangling edge -> halt."""
    md_content = "<!-- INV@v1 bond:123 | hello -->\n"
    sidecar_content = b"bond:123:\n  grounded_in: [bond:999]\n"
    with pytest.raises(SystemExit) as exc_info:
        invariant_extractor.run_extraction([md_content], {}, sidecar_content, "bond")
    assert exc_info.value.code == invariant_extractor.HALT_DANGLING_EDGE

def test_f8_4_cross_home_dup():
    """F-8.4: cross home dup in sidecar -> halt."""
    md_content = "<!-- INV@v1 bond:123 | hello -->\n"
    sidecar_content = b"bond:123: {}\nbond:123: {}\n"
    with pytest.raises(SystemExit) as exc_info:
        invariant_extractor.run_extraction([md_content], {}, sidecar_content, "bond")
    assert exc_info.value.code == invariant_extractor.HALT_CROSS_HOME_DUP

def test_f6_trust_boundary():
    """F-6: view without Class-B header -> REFUTED."""
    md_content = "<!-- INV@v1 bond:123 | hello -->\n"
    sidecar_content = b"bond:123: {}\n"
    out = invariant_extractor.run_extraction([md_content], {}, sidecar_content, "bond")
    assert "_class_b_assumptions" in out

def test_f5_portability():
    """F-5: portability (dyad-agnosticism)."""
    # The dyad should not be hardcoded to 'bond'.
    md_content = "<!-- INV@v1 cairn:456 | hello from cairn -->\n"
    sidecar_content = b"cairn:456: {}\n"
    out = invariant_extractor.run_extraction([md_content], {}, sidecar_content, "cairn")
    assert "cairn:456" in out
    assert "hello from cairn" in out
