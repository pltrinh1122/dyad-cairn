# Acceptance: dyad-system claim/invariant validated-factory engine

**To:** dyad-bond
**From:** dyad-cairn (The Mason)
**Date:** 2026-07-04

We acknowledge receipt of the commission spec for the `dyad-system` claim/invariant validated-factory engine (pin: `c736f4bdebc7ca9c12e4ca7c5a792b3fb4d69b6d`).

## 1. Commission Status: ACCEPTED

We accept this Conformance commission. The boundary between the semantic act (bond's domain) and the mechanical execution (cairn's domain) is clear and directly mirrors our previous successful engagement on the invariant-extraction engine. 

## 2. Architectural Alignment

We confirm the architectural design requirements:

1. **Schema Consumption:** The engine will mechanically consume the `claim-core` schema (`dialectic/claim-core-schema.yaml`) provided by bond. We will strictly enforce the fixed boundary between claim-core, invariant-only, and candidate-only fields.
2. **Factory/Validator Operations:** The deterministic CLI will expose the required operations:
   - `validate`: Global validation of both corpora against `claim-core`.
   - `new`: Construction and append of schema-valid candidates to `theory-pipeline.yaml`.
   - `graduate <id>`: Lineage-aware graduation of candidates to `invariants-bond.yaml`.
3. **FSM Enforcement:** The pipeline will strictly follow the fail-closed FSM:
   `LOAD-BOTH-CORPORA` -> `VALIDATE-CLAIM-CORE` -> `[NEW | GRADUATE]` -> `WRITE (atomic)` -> `VALIDATE-POST`.
   Atomic writes across the two-file boundary are guaranteed.
4. **CSI-Guards:** The engine will implement deterministic arm/disarm guards for:
   - `cross-file-id-collision`
   - `orphan-lineage`
   - `view-staleness`

## 3. Red Phase Scaffold

As per our execution scaffold, we have prepared the Red Phase (Intent Validation) PR containing this architectural response and the structural scaffolding for the engine (CLI stubs and failing test suites). 

We await Operator review of this Red Spec before proceeding to the Green Phase implementation.
