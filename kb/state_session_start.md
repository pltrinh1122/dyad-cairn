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
* Load the universal instruction layer (`DYAD.md`).
* Read `dyad-state/carry-forward.md` right after the anchor, if present, for live in-flight state
  from the prior session (adopted from dyad-bond's carry-forward discipline; written by
  `./bin/d-reflect`).


## Invariants
- **PR Constraint:** The Agent must never use raw `gh pr create` or `gh pr merge`. All PR actions must be mapped to `./bin/pr-sync`.
