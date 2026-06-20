import os
import subprocess
import pytest
import yaml

SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'commissions', 'invariant_extractor.py'))

@pytest.fixture
def run_cli():
    def _run(args, env=None):
        cmd = ["python3", SCRIPT_PATH] + args
        return subprocess.run(cmd, capture_output=True, text=True, env=env)
    return _run

@pytest.fixture
def mock_git_clean(monkeypatch):
    # Instead of patching in the test process, we should probably mock it for the subprocess.
    # We can do this by setting an environment variable and modifying invariant_extractor.py to respect it,
    # OR we can just run the function directly for some tests.
    pass

# We will run the tests via subprocess, so mocking needs to be either via python -c or we just test the python functions directly for some.
import importlib.util
spec = importlib.util.spec_from_file_location("invariant_extractor", SCRIPT_PATH)
extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extractor)

def test_fn_determinism(tmp_path):
    md = tmp_path / "source.md"
    md.write_text("<!-- INV@v1 bond:123 | hello -->\n", encoding="utf-8")
    sidecar = tmp_path / "sidecar.yaml"
    sidecar.write_text("bond:123: { status: ratified }\n", encoding="utf-8")
    
    # Mock git so it passes dirty tree check when run via subprocess
    # Or just test the function directly
    contents, shas = extractor.read_sources([str(md)])
    shas[str(sidecar)] = "fake"
    
    with open(sidecar, "rb") as f:
        sidecar_content = f.read()
        
    out1 = extractor.run_extraction(contents, shas, sidecar_content, "bond")
    out2 = extractor.run_extraction(contents, shas, sidecar_content, "bond")
    assert out1 == out2
    
def test_sha_determinism(tmp_path):
    md = tmp_path / "source.md"
    md.write_text("<!-- INV@v1 bond:123 | hello -->\n", encoding="utf-8")
    sidecar = tmp_path / "sidecar.yaml"
    sidecar.write_text("bond:123: { status: ratified }\n", encoding="utf-8")
    
    contents, shas = extractor.read_sources([str(md)])
    shas[str(sidecar)] = "fake_sha"
    
    with open(sidecar, "rb") as f:
        sidecar_content = f.read()
    
    out = extractor.run_extraction(contents, shas, sidecar_content, "bond")
    parsed = yaml.safe_load(out)
    assert "_staleness_guard" in parsed
    assert "source_shas" in parsed["_staleness_guard"]

def test_unclosed_tag(tmp_path):
    md = tmp_path / "source.md"
    md.write_text("<!-- INV@v1 bond:123 | hello \n", encoding="utf-8")
    sidecar = tmp_path / "sidecar.yaml"
    sidecar.write_text("bond:123: {}\n", encoding="utf-8")
    
    contents, shas = extractor.read_sources([str(md)])
    with pytest.raises(SystemExit) as e:
        extractor.run_extraction(contents, shas, b"", "bond")
    assert e.value.code == extractor.HALT_MALFORMED_TAG

def test_dup_id(tmp_path):
    md = tmp_path / "source.md"
    md.write_text("<!-- INV@v1 bond:123 | a --><!-- INV@v1 bond:123 | b -->\n", encoding="utf-8")
    contents, shas = extractor.read_sources([str(md)])
    with pytest.raises(SystemExit) as e:
        extractor.run_extraction(contents, shas, b"", "bond")
    assert e.value.code == extractor.HALT_DUPLICATE_ID

def test_missing_source():
    with pytest.raises(SystemExit) as e:
        extractor.read_sources(["nonexistent.md"])
    assert e.value.code == extractor.HALT_MISSING_SOURCE

def test_one_liner_verbatim(tmp_path):
    md = tmp_path / "source.md"
    md.write_text("<!-- INV@v1 bond:123 | hello world -->\n", encoding="utf-8")
    sidecar = tmp_path / "sidecar.yaml"
    sidecar.write_text("bond:123: {}\n", encoding="utf-8")
    
    contents, shas = extractor.read_sources([str(md)])
    out = extractor.run_extraction(contents, shas, b"bond:123: {}\n", "bond")
    parsed = yaml.safe_load(out)
    assert parsed["bond:123"]["one_liner"] == "hello world"

def test_portability(tmp_path):
    md = tmp_path / "source.md"
    md.write_text("<!-- INV@v1 cairn:456 | hello -->\n", encoding="utf-8")
    contents, shas = extractor.read_sources([str(md)])
    out = extractor.run_extraction(contents, shas, b"cairn:456: {}\n", "cairn")
    parsed = yaml.safe_load(out)
    assert "cairn:456" in parsed

def test_declared_trust_boundary(tmp_path):
    md = tmp_path / "source.md"
    md.write_text("<!-- INV@v1 bond:123 | hello -->\n", encoding="utf-8")
    contents, shas = extractor.read_sources([str(md)])
    out = extractor.run_extraction(contents, shas, b"bond:123: {}\n", "bond")
    parsed = yaml.safe_load(out)
    assert "_class_b_assumptions" in parsed

def test_encoding_eol(tmp_path):
    md = tmp_path / "source.md"
    with open(md, "wb") as f:
        f.write(b"<!-- INV@v1 bond:123 | a -->\r\n")
    with pytest.raises(SystemExit) as e:
        extractor.read_sources([str(md)])
    assert e.value.code == extractor.HALT_ENCODING_EOL

def test_grammar_version(tmp_path):
    md = tmp_path / "source.md"
    md.write_text("<!-- INV bond:123 | hello -->\n", encoding="utf-8")
    contents, shas = extractor.read_sources([str(md)])
    with pytest.raises(SystemExit) as e:
        extractor.run_extraction(contents, shas, b"", "bond")
    assert e.value.code == extractor.HALT_GRAMMAR_VERSION

def test_orphan_tag(tmp_path):
    md = tmp_path / "source.md"
    md.write_text("<!-- INV@v1 bond:123 | hello -->\n", encoding="utf-8")
    contents, shas = extractor.read_sources([str(md)])
    with pytest.raises(SystemExit) as e:
        extractor.run_extraction(contents, shas, b"", "bond")
    assert e.value.code == extractor.HALT_ORPHAN_TAG

def test_orphan_sidecar(tmp_path):
    md = tmp_path / "source.md"
    md.write_text("", encoding="utf-8")
    contents, shas = extractor.read_sources([str(md)])
    with pytest.raises(SystemExit) as e:
        extractor.run_extraction(contents, shas, b"bond:123: {}\n", "bond")
    assert e.value.code == extractor.HALT_ORPHAN_SIDECAR

def test_dangling_edge(tmp_path):
    md = tmp_path / "source.md"
    md.write_text("<!-- INV@v1 bond:123 | hello -->\n", encoding="utf-8")
    contents, shas = extractor.read_sources([str(md)])
    sidecar = b"bond:123:\n  grounded_in: [bond:999]\n"
    with pytest.raises(SystemExit) as e:
        extractor.run_extraction(contents, shas, sidecar, "bond")
    assert e.value.code == extractor.HALT_DANGLING_EDGE

def test_cross_home_dup_sidecar(tmp_path):
    md = tmp_path / "source.md"
    md.write_text("<!-- INV@v1 bond:123 | hello -->\n", encoding="utf-8")
    contents, shas = extractor.read_sources([str(md)])
    sidecar = b"bond:123: {}\nbond:123: {}\n"
    with pytest.raises(SystemExit) as e:
        extractor.run_extraction(contents, shas, sidecar, "bond")
    assert e.value.code == extractor.HALT_CROSS_HOME_DUP
