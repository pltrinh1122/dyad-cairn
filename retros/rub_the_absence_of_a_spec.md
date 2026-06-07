# Retro: The Absence of a Spec is the Specification

## Continue
We must continue avoiding traditional SDLC "spec" documents (e.g. Jira epics, Confluence pages). The Operator observed that the translation from intent -> invariants -> TDD tests feels "strangely simple." This simplicity is the defining characteristic of a low-friction (wu-wei) architecture. 

## Start
We must start recognizing that the "Spec" in `dyad-cairn` is not missing; it is strictly partitioned across the **Ontological Bond**:
1. **The Why (The Ledger & Retros):** Future dyads will map intent by reading the immutable `DYAD_LEDGER.md` and the `retros/` directory. This is where the structural friction and architectural decisions are permanently stored.
2. **The How (The Tests):** The execution tests (`tests/test_*.py`) are the physical, executable specification. They are the only form of specification that mathematically guarantees the code matches the intent.

## Stop
We must stop worrying about "how future dyads will maintain the code" under traditional paradigms. Future dyads will not read static specs; they will execute `[PROBE]` nodes to attack the tests (The How) and falsify the Retros (The Why). If the tests pass, the invariant holds. If they want to change the system, they must first rewrite the test.
