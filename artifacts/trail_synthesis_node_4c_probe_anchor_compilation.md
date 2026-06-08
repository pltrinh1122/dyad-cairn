# Trail Synthesis: Anchor Compilation Probe

**Probe Invariant:** The gap between the structural YAML state and the Markdown anchor has been falsified. Hand-mutating `GEMINI.md` violates deterministic state progression and causes a split-brain.

**Execution RCA:**
- Systemic analysis found no mechanical sync between `dip_state.yml` and `GEMINI.md`.
- Designed the Anchor Compilation Invariant: `GEMINI.md` becomes a Materialized View physically projected from `dip_state.yml` using a new `anchor_compiler.py` skill.
- Injected downstream `PLAN` and `EXECUTE` nodes to implement this schema into the Frontier DAG.
