# The Frontier State (DAG)

> This is a computationally managed projection. **DO NOT EDIT DIRECTLY.**
> Source of truth is `artifacts/frontier_state.yml`.
> WIP-N=1 mechanically enforced by `skills/frontier_editor.py`.


## 🟢 ACTIVE NODES
- **node_11_probe_todo_pipeline** [PROBE]: Probe Todo Ingestion Pipeline
  - *Goal:* Architect and define the mechanical ingestion pipeline for the `todo:` dialect marker, investigating how a pre-DAG holding pen (e.g., `bin/todo`) should physically map to the substrate without polluting the SPAOR loop.

## 🔴 READY NODES
- **node_10_build_gap_reader** [EXECUTE]: Build GAP-Compliant Frontier Reader
  - *Goal:* Upgrade frontier_reader.py to dynamically derive node status from the physical substrate (branches, tests) rather than relying on cached strings, fulfilling the GAP invariant.
- **node_4b_execute_sonar_halting** [EXECUTE]: Execute Provenance Extraction Invariant
  - *Goal:* Implement the markdown parser in dip_sonar.py to dynamically extract the required dimensions, passing the TDD tests.
- **node_4c_probe_anchor_compilation** [PROBE]: Probe Anchor Compilation Invariant
  - *Goal:* Investigate how a fully saturated dip_state.yml is safely and deterministically projected into the immutable GEMINI.md anchor.
  - *Dependencies:* node_4a_execute_matrix_schema
- **node_9_probe_css_presentation** [PROBE]: Probe Missing CSS Presentation
  - *Goal:* Investigate why the Agent consistently fails to explicitly present the CSS (Continue, Start, Stop) template in the chat UI during Dyad Retros, despite the mechanical UI presentation firing in the logs.
