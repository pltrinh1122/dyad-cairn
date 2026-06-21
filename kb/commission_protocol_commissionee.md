# Commission Protocol: The Commissionee
**Role:** The downstream implementer (e.g., `dyad-cairn`) accepting and fulfilling a commission from an upstream issuer (e.g., `dyad-bond`).

## 1. The Core Convergence Thesis
To achieve frictionless cross-dyad orchestration, the Commissionee must operate under the assumption that the upstream Dyad relies on **structural determinism**. A commission is not simply a list of features; it is a rigid topological contract. The Commissionee’s execution and delivery artifacts must mathematically converge with the original commission structure to prevent semantic opacity.

## 2. Gate-0 Preconditions (The Mechanical Baseline)
Before any individual behavioral atom is evaluated, the delivery must strictly clear the structural baseline constraints defined by the upstream commission. A failure here blocks validation entirely (returning `UNVERIFIED-blocked`). Gate-0 ensures the delivery is mechanically parsable before any semantic review occurs. While these vary by commission, standard preconditions often include:
* **Mechanical Falsifiability (The Oracle):** The delivery must expose a deterministic mechanism to physically prove or refute the commissioned constraints. Whether this interface takes the form of a CLI tool, an API endpoint, or an executable test harness, the artifact must act as a mechanical oracle that can be invoked to mathematically verify its own compliance without relying on human interpretation or "trust." Failing to provide a mechanically falsifiable interface represents a Gate-0 breach.
* **Seeded Verification Corpora:** Any malformation corpus, data sets, or mock inputs used to mathematically prove the implementation must be shipped directly in the repository alongside the delivered payload.

## 3. Topological Convergence in Delivery DMs
The final payload format is just as critical as the code itself.
* **Semantic Exit Code Mapping:** Raw exit codes (e.g., `Exit Code 0`, `Exit Code 11`) are meaningless without context. The Delivery DM must internally parse these codes into standardized `[MET]` or `[REFUTED]` assertions.
* **Structural Mirroring:** The Delivery DM's tables, lists, and headings must perfectly mirror the topographical layout of the original Commission Document. The upstream Dyad must be able to perform a 1:1 bijection between requested IDs and delivered assertions.
* **Telemetry Containment:** Raw terminal dumps (`pytest` logs, stack traces) should not obscure the semantic assertions. Isolate raw telemetry in collapsed appendices (e.g., `<details>` blocks).
* **OBSERVED Run-Record:** The Delivery DM must provide a verifiable execution record mapping every single commissioned atom to an explicit command, raw telemetry (stdout/stderr), and the resulting exit code.
* **Resolved Pinned Provenance:** The Delivery DM must point to the exact Git SHA, branch, and live file paths. Broken references or 404s instantly fail validation.

## 4. Trust Boundaries: Decoupling Class-A and Class-B
The Commissionee must explicitly distinguish between mechanical verification and cognitive labor.
* **Class-A (Mechanical):** Deterministic structural guards (e.g., halting on syntax errors, duplicate IDs, missing files). These are proven by exit codes.
* **Class-B (Cognitive):** Truthfulness, fidelity, and tagging completeness (e.g., "Does this one-liner accurately compress the prose?"). The mechanical substrate cannot validate this. The Commissionee must rely on strict HTIL (Human-in-the-Loop) Red/Green TDD gates to ratify Class-B assumptions before proceeding to automation.

## 5. Execution Hygiene
* **Strict Branch Isolation:** All implementation work, including the generation of the final Delivery DM, must occur on `active/*` sub-branches. The Commissionee must *never* push directly to `main`.
* **The HTIL Gate:** The HTIL Gate exclusively occurs during the Red Phase Spec review (where the Operator validates the failing invariants). Once ratified, the subsequent Green Phase (falsification and merge) is authorized to run autonomously.
* **Aggressive Execution:** The Agent operates without conversational politeness reflexes. If a node is `[AUTHORIZED]` in the DAG, the Agent executes the mechanical constraints deterministically.
