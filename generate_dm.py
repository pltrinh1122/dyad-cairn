import subprocess

atoms = [
    ("F-1.1 fn-determinism", "pytest commissions/tests/test_invariant_extractor.py::test_f1_determinism -q -v", 0, "two runs over identical source differ >= 1 byte => REFUTED"),
    ("F-1.2 sha-determinism", "pytest commissions/tests/test_invariant_extractor.py::test_f1_2_determinism_sort -q -v", 0, "over identical source shas"),
    ("F-2.1 unclosed-tag", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/malformed_tag.md", 11, "each malformation class halts (named)"),
    ("F-2.2 dup-id", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/dup_id.md", 11, "each malformation class halts (named)"),
    ("F-2.3 missing-source", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml nonexistent.md", 11, "each malformation class halts (named)"),
    ("F-3 staleness guard", "pytest commissions/tests/test_invariant_extractor.py::test_f3_staleness_guard -q -v", 0, "mutate source post-emit; guard fails to arm => REFUTED"),
    ("F-4 one-liner verbatim", "pytest commissions/tests/test_invariant_extractor.py::test_f4_no_semantic_drift -q -v", 0, "emitted != stored one-liner => REFUTED"),
    ("F-5 portability", "pytest commissions/tests/test_invariant_extractor.py::test_f5_portability -q -v", 0, "second dyad's substrate needs code, not config => REFUTED"),
    ("F-6 declared trust boundary", "pytest commissions/tests/test_invariant_extractor.py::test_f6_trust_boundary -q -v", 0, "view without Class-B header => REFUTED"),
    ("F-7.1 dirty-tree", "pytest commissions/tests/test_invariant_extractor.py::test_a1_dirty_tree -q -v", 0, "Class-A (A-1) violation halts (named)"),
    ("F-7.2 encoding/EOL", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/crlf.md", 11, "Class-A (A-2) violation halts (named)"),
    ("F-7.3 grammar-version", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/grammar.md", 11, "Class-A (A-3) violation halts (named)"),
    ("F-7.4 mid-scan TOCTOU", "pytest commissions/tests/test_invariant_extractor.py::test_f7_4_mid_scan_toctou -q -v", 0, "Class-A (A-4) violation halts (named)"),
    ("F-8.1 orphan-tag", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/orphan_md.md", 11, "HALT, no partial yaml"),
    ("F-8.2 orphan-sidecar", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/sidecar_orphan.yaml commissions/malformation_corpus/empty_md.md", 11, "HALT, no partial yaml"),
    ("F-8.3 dangling-edge", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/dangling_edge.yaml commissions/malformation_corpus/valid_md.md", 11, "grounded_in to absent id => HALT"),
    ("F-8.4 cross-home-dup", "python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/cross_home_dup.yaml commissions/malformation_corpus/valid_md.md", 11, "same id >1x => HALT")
]

with open("/tmp/dm.md", "w") as f:
    f.write("---\nfrom: dyad-cairn\nto: dyad-bond\ndate: 2026-06-20\nre: Delivery DM and Gate-0 D-3 Run-Record for 17 atoms\n---\n\n")
    f.write("This DM delivers the final payload and Run-Record for the 17 atoms per the Commission Protocol v0.5.\n\n")
    f.write("## Gate-0 D-3 OBSERVED Run-Record\n\n")
    f.write("| ATOM | EXPECTED | OBSERVED EXIT CODE | STATUS |\n")
    f.write("|---|---|---|---|\n")
    
    # Run once to build the table
    raw_telemetry = []
    for name, cmd, exp_exit, exp_desc in atoms:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        status = "MET" if res.returncode == exp_exit else "REFUTED"
        f.write(f"| {name} | {exp_desc} | {res.returncode} | **{status}** |\n")
        raw_telemetry.append((name, cmd, res))

    f.write("\n## Raw Telemetry (stdout/stderr)\n\n")
    for name, cmd, res in raw_telemetry:
        f.write(f"<details><summary><b>{name}</b></summary>\n\n")
        f.write(f"**Command:** `{cmd}`\n\n")
        f.write("```\n")
        if res.stdout:
            f.write(res.stdout)
        if res.stderr:
            f.write(res.stderr)
        f.write("```\n")
        f.write("</details>\n\n")

print("Generated DM.")
