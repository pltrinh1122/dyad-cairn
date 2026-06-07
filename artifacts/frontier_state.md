# The Frontier State (DAG)

> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**
> Source of truth is `artifacts/frontier_state.yml`.
> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.


## 🟢 ACTIVE NODES
- **node_4b_probe_sonar_halting** [PROBE]: Probe Sonar Halting Conditions
  - *Goal:* Investigate the mechanical halting conditions for dip.py. Discover the exact physical rules that trigger sys.exit(1) (e.g. missing signature, empty dimension).

## 🔴 BLOCKED NODES
- **node_4c_probe_anchor_compilation** [PROBE]: Probe Anchor Compilation Invariant
  - *Goal:* Investigate how a fully saturated dip_state.yml is safely and deterministically projected into the immutable GEMINI.md anchor.
- **node_5_probe_reflect_phase** [PROBE]: Probe the [REFLECT] Phase Requirement
  - *Goal:* Rub the necessity of an explicit [REFLECT] node-type or phase following [EXECUTE] to capture execution-level learnings (best practices, pitfalls) before closing the trail.
