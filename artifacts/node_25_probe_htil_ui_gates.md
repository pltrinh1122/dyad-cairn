# Probe: HTIL UI Gates and Decomposition Automation

## 1. The Missing UIs Problem
The Operator highlighted multiple mechanical steering failures:
- Design-Review UI wasn't accessible manually.
- Retro CSS UI wasn't firing in the conversational chat.
- Invariants weren't being presented.
- Agent failed to perform automatic DAG decomposition, instead hallucinating that decomposition spawns multiple `PLAN` nodes.

## 2. Invariant Discovery
1. **Design Review Access:** The `design_review_ui.py` script existed and correctly parsed invariants via regex, but it had no CLI entrypoint for the Operator to manually invoke it during checkout.
2. **Decomposition Hallucination:** `design_review_ui.py` contained hardcoded legacy text asserting that decomposition creates multiple `PLAN` nodes. This output was actively gaslighting the Agent into violating the "PROBE decomposes into PROBE" invariant.
3. **Missing Auto-Decomposition:** The orchestrator lacked the mechanical implementation to parse a PROBE artifact and physically inject its child nodes into the DAG.
4. **CSS UI Presentation:** `bin/retro` prints the CSS UI correctly to its standard output. The failure is conversational: the `dialect_linter.py` strictly requires the Agent to explicitly echo this presentation back to the Operator in the chat UI. If the Agent forgets, the Operator doesn't see it.

## 3. Recommended Implementation Path (PLAN)
Because the required mechanical fixes were isolated to orchestrator scripts, we physically pushed them during this Probe. This node requires no further Execution (Atomic). 
1. Added the `design-review` CLI argument to `bin/node`.
2. Purged the `PLAN` decomposition hallucination from `design_review_ui.py`.
3. Implemented regex-driven auto-decomposition in `skills/flow_state_manager.py` tied to `complete_node`.
