# The Cognitive State Machine

This document codifies the operating lifecycle of `dyad-cairn`. It defines the strict physical rails that govern how *intent* transforms into *reality*.

## 1. STATE: `[PRE-QUARRY]` (The Holding Pen)
* **Input:** Raw, unclassified signals (from the Operator, the Agent, or an external dyad's outbox).
* **Location:** `artifacts/todos.yml`
* **Characteristics:** No scope. No execution vector. Just raw `intent`.

## 2. TRANSITION: `[THE RUB]` (Formalization)
* **The Bridge:** `bin/node convert-todo`
* **Mechanics:** The dyad engages the raw signal. We answer *What, Why, and When*. This friction collapses the ambiguity, crystallizing the intent into a formal `scope` (`[FRONTIER]`, `[SUBSTRATE]`, or `[INTEGRITY]`).

## 3. STATE: `[ACTIVE]` (The Engine)
* **Location:** `artifacts/frontier_state.yml` (The Execution DAG)
* **Characteristics:** The node now possesses a Scope and an Execution Phase (`PROBE`, `PLAN`, `EXECUTE`, `REFLECT`). The dyad mines this quarry through iterative coding and TDD until the node is `DONE`.

## 4. TRANSITION: `[SYNTHESIS]` (Crystallization)
* **The Bridge:** `bin/node complete` / `retro`
* **Mechanics:** The completed work is stripped from the Active plate. It undergoes one final transition to become permanent.

## 5. STATE: `[FROZEN]` (The Invariants & Exhaust)
* **Location A (Guards):** `artifacts/audit_state.yml` — The work becomes a physical invariant guarding the dyad's health.
* **Location B (History):** `DYAD_LEDGER.md` — The work becomes chronological exhaust.
