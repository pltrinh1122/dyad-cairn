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
### todo_1783550122.991821_cc2215e0 [UNRUBBED]
**Raw Thought:** Append to todo_1783548045.536934_cd799b7f (gap 6, found while authoring HOW-0006): kb/HOW-0005-d-land-delegation.md is referenced by DYAD.md:80 ('Grounded by the kb/HOW-0005-d-land-delegation.md playbook') but does not exist in kb/ — either materialize the playbook from the d-land implementation (skills/flow_state_manager.py + bin/d-land) or correct the DYAD.md pointer. Same class as gaps 1-2: canonical text naming a missing artifact.

**The Rub Matrix:**
- [ ] **WHAT:** Missing
- [ ] **WHY:** Missing
- [ ] **SCOPE:** Missing

---
### todo_1783553143.465903_144429c6 [UNRUBBED]
**Raw Thought:** CRAFT-CAPABILITY (Operator seed, 2026-07-08; re-captured after the original ledger pin was lost to a gap-5 ledger-restore): 'Converting mortar to stone is essentially converting fragile unfalsifiable statements into solid falsifiable statements.' Semantic bridge unifying DYAD.md Ontology (Cutting = 'falsify the claims to find the truth'; Mortar = hallucinated logic w/ no falsifier = unfalsifiable-in-practice), the README falsifiable-manifesto spine, and the HOW-0006 imperatives->falsifiable-conditions recast. PRECISION (never smooth): falsifiability is the necessary CUT (mortar->candidate stone); grounding + survival under attack (Validate: Falsification/Triangulation/Grounding) makes a falsifiable claim load-bearing STONE -- hence 'survives', never 'settled'. Lived proof-of-origin this arc (n>=4): README claims+falsifiers; audit wf_8918028a-253 catching 4 falsifier-drifts; inference!=invention; HOW-0006 C1-C19. NEXT: d-rub to scope WHAT/WHY/SCOPE; candidate deepening of DYAD.md Craft (mechanism = falsification-engineering) baked across Why/How/When; candidate generalized How = a mortar-detector lint flagging unfalsifiable statements in any artifact.

**The Rub Matrix:**
- [ ] **WHAT:** Missing
- [ ] **WHY:** Missing
- [ ] **SCOPE:** Missing

---
