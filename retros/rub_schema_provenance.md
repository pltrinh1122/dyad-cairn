# Retro: Schema Provenance and Hardcoding Invariants

## Continue
We must continue attacking hardcoded assumptions in our `[PLAN]` phase. The Operator's rub exposed a lethal hallucination: I hardcoded "7 dimensions" into the execution tests without linking them to their physical provenance.

## Start
We must start physically binding our constraints to their provenance. The rules for instantiation live exclusively in `commons/AGENT.md`. Therefore, `dip.py` (and its TDD tests) must not hardcode dimensions. The Sonar must dynamically parse the current `commons/AGENT.md` to extract the required dimensions. If the Commons form evolves to 8 dimensions, our `dip.py` must automatically enforce 8 without changing our code. This is a true Ontological Bond.

## Stop
We must stop hardcoding external constraints into our test suites. Hardcoding a rule that belongs to an external submodule creates a silent fault line that will fracture the moment the upstream changes.
