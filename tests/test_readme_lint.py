"""Deterministic V-pair for skills/readme_lint.py (No-Pure-G invariant).

All fixture READMEs are written to tmp_path — the suite never touches the
real README.md except read-only in the exemplar test, and never writes to
any substrate file (ledger-isolation lesson, DYAD_LEDGER.md REFLECT
2026-07-08 19:05:41 'Start').
"""

from pathlib import Path

from skills.readme_lint import claim_parity, knife_diff, lint

REPO_ROOT = Path(__file__).resolve().parent.parent

VALID_FRONTMATTER = """\
---
doc: "README.md — test manifesto"
kind: derived-view
genre: "falsifiable manifesto"
rule: "cite the source, never this lens"
belief:
  statement: "test belief"
  foundation: belief
  stance: thesis
  status: hypothesis
grade: "survives — intra-dyad"
coverage: "E0 — no outside attack yet."
dogma: false
caution: "status is the headline"
cta: "bring friction"
canonical_home:
  - "ANCHOR.md § Real Heading"
governed_by: [test:no-dogma]
updated: 2026-07-08
---
"""

VALID_BODY = """\

# Test manifesto

**Claim 1 — The belief.** Something falsifiable. → *Break it:* show the counterexample.

**Claim 2 — The invitation.** Tested in one dyad only; come attack it.
"""


def write_fixture(tmp_path, frontmatter=VALID_FRONTMATTER, body=VALID_BODY):
    (tmp_path / "ANCHOR.md").write_text("## Real Heading\ncanonical content\n")
    readme = tmp_path / "README.md"
    readme.write_text(frontmatter + body)
    return readme


def test_exemplar_readme_passes():
    """The repo's own README.md is the exemplar and must conform."""
    assert lint(REPO_ROOT / "README.md") == []


def test_formal_surface_passes():
    """FALSIFICATION.md (the formal sibling, HOW-0006 C24) must conform too."""
    assert lint(REPO_ROOT / "FALSIFICATION.md") == []


def test_sibling_registers_claim_parity():
    """C24: the plain lens and the formal surface carry the same claim set."""
    assert claim_parity(REPO_ROOT / "README.md", REPO_ROOT / "FALSIFICATION.md") == []


def test_valid_fixture_passes(tmp_path):
    assert lint(write_fixture(tmp_path)) == []


def test_missing_frontmatter_field_fails(tmp_path):
    broken = VALID_FRONTMATTER.replace('coverage: "E0 — no outside attack yet."\n', "")
    errors = lint(write_fixture(tmp_path, frontmatter=broken))
    assert any("coverage" in e for e in errors)


def test_dogma_true_fails(tmp_path):
    broken = VALID_FRONTMATTER.replace("dogma: false", "dogma: true")
    errors = lint(write_fixture(tmp_path, frontmatter=broken))
    assert any("dogma" in e for e in errors)


def test_settled_status_fails(tmp_path):
    broken = VALID_FRONTMATTER.replace("status: hypothesis", "status: settled")
    errors = lint(write_fixture(tmp_path, frontmatter=broken))
    assert any("belief.status" in e for e in errors)


def test_non_derived_view_kind_fails(tmp_path):
    broken = VALID_FRONTMATTER.replace("kind: derived-view", "kind: content-home")
    errors = lint(write_fixture(tmp_path, frontmatter=broken))
    assert any("derived-view" in e for e in errors)


def test_unresolvable_canonical_home_file_fails(tmp_path):
    broken = VALID_FRONTMATTER.replace("ANCHOR.md § Real Heading", "MISSING.md § Real Heading")
    errors = lint(write_fixture(tmp_path, frontmatter=broken))
    assert any("MISSING.md" in e for e in errors)


def test_unresolvable_canonical_home_heading_fails(tmp_path):
    broken = VALID_FRONTMATTER.replace("§ Real Heading", "§ Ghost Heading")
    errors = lint(write_fixture(tmp_path, frontmatter=broken))
    assert any("Ghost Heading" in e for e in errors)


def test_claim_without_falsifier_fails(tmp_path):
    body = VALID_BODY.replace(" → *Break it:* show the counterexample.", "")
    errors = lint(write_fixture(tmp_path, body=body))
    assert any("Claim 1" in e and "falsifier" in e for e in errors)


def test_final_invitation_claim_needs_no_falsifier(tmp_path):
    """The last claim may be the standing invitation (exemplar's Claim 6)."""
    assert lint(write_fixture(tmp_path)) == []


def test_no_claims_fails(tmp_path):
    errors = lint(write_fixture(tmp_path, body="\n# No claims here\n"))
    assert any("no numbered claims" in e for e in errors)


def test_missing_frontmatter_block_fails(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("# Just a plain readme\n")
    errors = lint(readme)
    assert any("frontmatter" in e for e in errors)


# --- Concision modes (HOW-0006 C22/C24, adopted from dyad-bond, falsified 2026-07-13) ---

KNIFE_A = "**Claim 1.** Thing. → *Break it:* show one counterexample.\n"
KNIFE_B = "**Falsifier** (formal): a generative edit lands unpaired.\n"


def write_pair(tmp_path, a_text, b_text):
    a, b = tmp_path / "before.md", tmp_path / "after.md"
    a.write_text(a_text)
    b.write_text(b_text)
    return a, b


def test_knife_diff_stable_prose_change_passes(tmp_path):
    """C22: cutting prose while knives stay byte-identical is a clean pass."""
    a, b = write_pair(tmp_path,
                      "long narrative prose\n" + KNIFE_A + KNIFE_B,
                      "short\n" + KNIFE_A + KNIFE_B)
    assert knife_diff(a, b) == []


def test_knife_diff_relocation_passes(tmp_path):
    """C22: relocation (reordering) is permitted; only rewording fails."""
    a, b = write_pair(tmp_path, KNIFE_A + KNIFE_B, KNIFE_B + KNIFE_A)
    assert knife_diff(a, b) == []


def test_knife_diff_reworded_knife_fails(tmp_path):
    reworded = KNIFE_A.replace("one counterexample", "counterexamples")
    a, b = write_pair(tmp_path, KNIFE_A + KNIFE_B, reworded + KNIFE_B)
    errors = knife_diff(a, b)
    assert any("lost or reworded" in e for e in errors)
    assert any("added or reworded" in e for e in errors)


def test_knife_diff_lost_knife_fails(tmp_path):
    a, b = write_pair(tmp_path, KNIFE_A + KNIFE_B, KNIFE_A)
    errors = knife_diff(a, b)
    assert any("lost or reworded" in e for e in errors)


def test_knife_diff_missing_file_fails(tmp_path):
    a, _ = write_pair(tmp_path, KNIFE_A, KNIFE_A)
    assert any("not found" in e for e in knife_diff(a, tmp_path / "ghost.md"))


def test_claim_parity_equal_sets_pass(tmp_path):
    a, b = write_pair(tmp_path,
                      "**Claim 1** x **Claim 2** y\n",
                      "**Claim 2** formal y\n\n**Claim 1** formal x\n")
    assert claim_parity(a, b) == []


def test_claim_parity_mismatch_fails(tmp_path):
    a, b = write_pair(tmp_path,
                      "**Claim 1** x **Claim 2** y **Claim 3** z\n",
                      "**Claim 1** x **Claim 4** w\n")
    errors = claim_parity(a, b)
    assert any("[2, 3]" in e for e in errors)
    assert any("[4]" in e for e in errors)
