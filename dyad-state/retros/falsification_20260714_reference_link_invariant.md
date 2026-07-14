# Falsification Record: "README References Must Be Easy-Access Links" (2026-07-14)

**Operator's proposed invariant:** when referencing material, `README.md` should
provide an easy-access link to the reader.

**Method:** measure link coverage of in-repo document references across both of cairn's
live registers and bond's plain lens; probe the edges where the invariant would be
wrong or unenforceable.

## Measurements

| Document | Linked .md refs | Bare .md refs (body prose) |
|---|---|---|
| cairn `README.md` | 0 | 2 (`DYAD.md`, `FALSIFICATION.md`, closing line) |
| cairn `FALSIFICATION.md` | 0 | 8 (`DYAD.md` ×6, `README.md` ×2) |
| bond `README.md` (post-split) | 1 | ~12 (incl. `dialectic/relationship-craft.md` ×7) |

## Survives (the core)

The violation is lived in the exemplar itself: every material reference in both of
cairn's registers was a bare backtick — a stranger on GitHub must hand-navigate to
`DYAD.md` from the very sentence that says "quote that, not this page." GitHub renders
relative links, so the reader-cost is pure waste. The invariant is also
**cairn-original, not inherited**: bond's plain lens fails it ~12:1. Charter precedent
exists — the UI Presentation Invariant (`DYAD.md § 5. NON-NEGOTIABLE`) grants the
Operator a one-action right to any referenced artifact in chat; the proposed invariant
extends the same right to the README's outward reader. And it is mechanically
decidable: strip markdown links from the body, flag any remaining mention of an .md
file that exists relative to the document.

## Refuted / narrowed (the edges)

1. **Frontmatter is exempt.** `canonical_home` entries are machine schema read by the
   linter (C13), not reader prose; markdown links inside YAML strings would corrupt the
   schema. The invariant binds body prose only.
2. **Heading anchors are not required.** File-level links suffice: GitHub heading slugs
   for `§`-decorated headings ("§ Craft (Dimension 1 & 6)") are fragile and unlintable
   against rot; the file link is one click and robust.
3. **Nonexistent files are out of scope.** A reference to a missing document is a
   grounding defect (C14), not a linking defect; the lint flags only files that exist.

## Disposition

Adopted as **C25 — Link what you cite** (`kb/HOW-0006`), verifier LINT: the check is
part of the standard `readme_lint` pass (`lint_reference_links`), paired with tests
(No-Pure-G), so C17 now enforces it on both siblings in CI. Red confirmed on the live
defects (2 + 2 violations), then both documents repaired: all 10 bare references are
now relative links. Knife-freeze empty on both documents; claim parity 6 = 6; both
lints green. Offerable back to bond, whose plain lens currently fails it.
