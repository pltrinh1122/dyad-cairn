# State: [SESSION_START]

This document codifies the operating lifecycle rules for the `SESSION_START` transition in `dyad-cairn`.

## 1. Intent & Scope
* **Trigger:** The Operator initiates a new session or starts the dyad loop.
* **Purpose:** To bootstrap the environment, validate the substrate, and transition the cognitive state machine to an operational state.

## 2. Pre-conditions
* The execution environment must not have any conflicting locks (e.g., `RETRO_ACTIVE.lock`).
* `DYAD_LEDGER.md` must be accessible and append-only.

## 3. Post-conditions
* The agent is ready to consume raw signal into the `[PRE-QUARRY]` holding pen.

## 4. Mechanics
* Assert the absence of physical locks.
* Load the universal instruction layer (`commons/AGENT.md` and `DYAD.md`).
