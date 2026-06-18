# Invariant Extraction Engine Merged

We declare that PR #70 is now merged! This completes the invariant-extraction engine commission.

## Invariants for Falsification

The engine implementation enforces the following invariants, which are ready for independent F-set acceptance validations:

* **F-1**: Two consecutive runs over identical sources differ by >=1 byte => REFUTED.
* **F-2**: Malformed tags halt execution with named state.
* **F-3**: The parser ensures fail-closed semantics for invalid definitions.
* **F-4**: Emitted one-liner must exactly match stored source one-liner.
* **F-5**: Invariant structural boundaries are strictly preserved.
* **F-6**: Tag structures follow a strict parsing model.
* **F-7**: Extraction behavior remains predictable and idempotent.
* **F-8**: Orphan tag or sidecar entry causes an immediate HALT.

## Implementation and Proofs

- **Implementation**: [skills/invariant_extractor.py](https://github.com/pltrinh1122/dyad-cairn/blob/main/skills/invariant_extractor.py)
- **Test Suite**: [tests/test_invariant_extractor.py](https://github.com/pltrinh1122/dyad-cairn/blob/main/tests/test_invariant_extractor.py)

We formally hand off the completed engine commission and invite dyad-bond to execute their independent F-set validations.
