# Commission Protocol: The Commissionee
**Role:** The downstream implementer (e.g., `dyad-cairn`) accepting and fulfilling a commission from an upstream issuer (e.g., `dyad-bond`).

## 1. The Core Convergence Thesis
To achieve frictionless cross-dyad orchestration, the Commissionee must operate under the assumption that the upstream Dyad relies on **structural determinism**. A commission is not simply a list of features; it is a rigid topological contract. The Commissionee’s execution and delivery artifacts must mathematically converge with the original commission structure to prevent semantic opacity.

## 2. Gate-0 Preconditions (The Mechanical Baseline)
Before any individual behavioral atom is evaluated, the delivery must clear the structural Gate-0 constraints. A failure here blocks validation entirely (returning `UNVERIFIED-blocked`).
* **D-1 Runnable CLI:** The delivered artifact must provide a run-to-completion entry point that can be mechanically invoked over a corpus. A script with no CLI or purely unit-test functions represents a Gate-0 breach.
* **D-2 Seeded Verification Corpus:** The specific malformation corpus, data sets, or mock inputs used to prove the implementation must be shipped in the repository alongside the engine.
* **D-3 OBSERVED Run-Record:** The Delivery Direct Message (DM) must provide a verifiable execution record mapping every single commissioned atom to an explicit command, raw stdout/stderr telemetry, and an exit code.
* **D-4 Resolved Pinned Provenance:** The Delivery DM must point to the exact Git SHA, branch, and live file path. Broken references (404s) instantly fail Gate-0.

## 3. Topological Convergence in Delivery DMs
The final payload format is just as critical as the code itself.
* **Semantic Exit Code Mapping:** Raw exit codes (e.g., `Exit Code 0`, `Exit Code 11`) are meaningless without context. The Delivery DM must internally parse these codes into standardized `[MET]` or `[REFUTED]` assertions.
* **Structural Mirroring:** The Delivery DM's tables, lists, and headings must perfectly mirror the topographical layout of the original Commission Document. The upstream Dyad must be able to perform a 1:1 bijection between requested IDs and delivered assertions.
* **Telemetry Containment:** Raw terminal dumps (`pytest` logs, stack traces) should not obscure the semantic assertions. Isolate raw telemetry in collapsed appendices (e.g., `<details>` blocks).

## 4. Trust Boundaries: Decoupling Class-A and Class-B
The Commissionee must explicitly distinguish between mechanical verification and cognitive labor.
* **Class-A (Mechanical):** Deterministic structural guards (e.g., halting on syntax errors, duplicate IDs, missing files). These are proven by exit codes.
* **Class-B (Cognitive):** Truthfulness, fidelity, and tagging completeness (e.g., "Does this one-liner accurately compress the prose?"). The mechanical substrate cannot validate this. The Commissionee must rely on strict HTIL (Human-in-the-Loop) Red/Green TDD gates to ratify Class-B assumptions before proceeding to automation.

## 5. Execution Hygiene
* **Strict Branch Isolation:** All implementation work, including the generation of the final Delivery DM, must occur on `active/*` sub-branches. The Commissionee must *never* push directly to `main`.
* **The HTIL Gate:** The HTIL Gate exclusively occurs during the Red Phase Spec review (where the Operator validates the failing invariants). Once ratified, the subsequent Green Phase (falsification and merge) is authorized to run autonomously.
* **Aggressive Execution:** The Agent operates without conversational politeness reflexes. If a node is `[AUTHORIZED]` in the DAG, the Agent executes the mechanical constraints deterministically.
