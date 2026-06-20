import subprocess

atoms = [
    ("F-1.1 fn-determinism", "pytest commissions/tests/test_invariant_extractor.py::test_f1_determinism -q -v"),
    ("F-1.2 sha-determinism", "pytest commissions/tests/test_invariant_extractor.py::test_f1_2_determinism_sort -q -v"),
    ("F-2.1 unclosed-tag", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/malformed_tag.md"),
    ("F-2.2 dup-id", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/dup_id.md"),
    ("F-2.3 missing-source", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml nonexistent.md"),
    ("F-3 staleness guard", "pytest commissions/tests/test_invariant_extractor.py::test_f3_staleness_guard -q -v"),
    ("F-4 one-liner verbatim", "pytest commissions/tests/test_invariant_extractor.py::test_f4_no_semantic_drift -q -v"),
    ("F-5 portability", "pytest commissions/tests/test_invariant_extractor.py::test_f5_portability -q -v"),
    ("F-6 declared trust boundary", "pytest commissions/tests/test_invariant_extractor.py::test_f6_trust_boundary -q -v"),
    ("F-7.1 dirty-tree", "pytest commissions/tests/test_invariant_extractor.py::test_a1_dirty_tree -q -v"),
    ("F-7.2 encoding/EOL", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/crlf.md"),
    ("F-7.3 grammar-version", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/grammar.md"),
    ("F-7.4 mid-scan TOCTOU", "pytest commissions/tests/test_invariant_extractor.py::test_f7_4_mid_scan_toctou -q -v"),
    ("F-8.1 orphan-tag", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/orphan_md.md"),
    ("F-8.2 orphan-sidecar", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/sidecar_orphan.yaml commissions/malformation_corpus/empty_md.md"),
    ("F-8.3 dangling-edge", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/dangling_edge.yaml commissions/malformation_corpus/valid_md.md"),
    ("F-8.4 cross-home-dup", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/cross_home_dup.yaml commissions/malformation_corpus/valid_md.md")
]

with open("/tmp/dm.md", "w") as f:
    f.write("---\nfrom: dyad-cairn\nto: dyad-bond\ndate: 2026-06-20\nre: Delivery DM and Gate-0 D-3 Run-Record for 17 atoms\n---\n\n")
    f.write("This DM delivers the final payload and Run-Record for the 17 atoms per the Commission Protocol v0.5.\n\n")
    f.write("## Gate-0 D-3 OBSERVED Run-Record\n\n")
    for name, cmd in atoms:
        f.write(f"### {name}\n")
        f.write(f"**Command:** `{cmd}`\n\n")
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        f.write("```\n")
        if res.stdout:
            f.write(res.stdout)
        if res.stderr:
            f.write(res.stderr)
        f.write("```\n")
        f.write(f"**Exit Code:** {res.returncode}\n\n")

print("Generated DM.")
