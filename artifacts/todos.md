# Todo Backlog (Pre-DAG Holding Pen)

> Ideas parked here have not formally entered the SPAOR execution loop.
> Use `./bin/node convert-todo <todo_id>` to ingest an item into the DAG.

### todo_1783433329.473695_088d8946 [UNRUBBED]
**Raw Thought:** help

**The Rub Matrix:**
- [ ] **WHAT:** Missing
- [ ] **WHY:** Missing
- [ ] **SCOPE:** Missing

---
### todo_1783545603.9572_5d40faf0 [UNRUBBED]
**Raw Thought:** add/edit interaction-invariant - SH should be framed as Agent's observation of Should Have (debt) and Should Hold (credit) for Operator's prompting, intent clarity and intent coherence.

**The Rub Matrix:**
- [ ] **WHAT:** Missing
- [ ] **WHY:** Missing
- [ ] **SCOPE:** Missing

---
### todo_1783548045.536934_cd799b7f [UNRUBBED]
**Raw Thought:** Fix substrate gaps identified during README grounding audit (2026-07-08): (1) dip_state.yml missing — CLAUDE.md/GEMINI.md shims declare projection from it and skills/anchor_compiler.py:12 expects artifacts/dip_state.yml, but the file exists nowhere and has no git history; materialize it or correct the provenance claim. (2) DYAD.md:89 (§9 Topology) still calls GEMINI.md 'The Anchor' and DYAD.md:42 names it a Why-home — stale since the AGENT.md→DYAD.md rename (b8add89); GEMINI.md is now a thin shim. Substrate Form mutation — needs Operator consensus on the fix shape. Append further gaps confirmed by workflow wf_8918028a-253 before closing.

**The Rub Matrix:**
- [ ] **WHAT:** Missing
- [ ] **WHY:** Missing
- [ ] **SCOPE:** Missing

---
### todo_1783548461.503489_1ad107ed [UNRUBBED]
**Raw Thought:** Append to todo_1783548045.536934_cd799b7f (README audit gaps, wf_8918028a-253 confirmed): (3) The Ontological Bond's Why axis is physically vacant — zero kb/WHY-* files exist, and the disjunct's other home (GEMINI.md) is now a 398-byte shim redirecting to DYAD.md; DYAD.md:42 needs a real Why-home decision. (4) Leaked test fixtures committed as real artifacts: bin/hard-guardrails is an 'echo test' stub and kb/HOW-0002-hard-guardrails.md is '# Dummy KB' — fixtures from tests/test_mason_install_stone.py leaked into the repo; remove or replace with real implementations.

**The Rub Matrix:**
- [ ] **WHAT:** Missing
- [ ] **WHY:** Missing
- [ ] **SCOPE:** Missing

---
### todo_1783549068.004563_0fa5ec7f [UNRUBBED]
**Raw Thought:** Append to todo_1783548045.536934_cd799b7f (gap 5, found during d-land of PR #154): the test suite mutates the real DYAD_LEDGER.md — tests/test_todo.py:17 spawns the real ./bin/todo with collision_intent_* fixtures and tests/test_substrate_concurrency_lock.py:24 calls ledger_manager.append_ledger directly; every ./bin/run-tests re-stamps 50 noise lines in the append-only ledger, violating the Ledger invariant and permanently re-dirtying the tree (d-land Durability check can never stay green). Fix: sandbox the ledger path in tests (tmpdir), then purge the 50 committed collision_intent_* lines from DYAD_LEDGER.md in a consensus commit.

**The Rub Matrix:**
- [ ] **WHAT:** Missing
- [ ] **WHY:** Missing
- [ ] **SCOPE:** Missing

---
