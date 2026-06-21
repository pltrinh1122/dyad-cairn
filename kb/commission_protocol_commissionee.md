# Commission Protocol: The Commissionee
**Role:** The downstream implementer (e.g., `dyad-cairn`) accepting a **Commission-Request** from an upstream issuer (e.g., `dyad-bond`), and returning a **Commission-Delivery**.

## 1. Operating Assumption
The Commissionee assumes the upstream Dyad evaluates deliveries via strict structural determinism. The **Commission-Delivery** MUST map topologically to the **Commission-Request**.

---

## Phase 1: Receiving the Commission-Request

### Gate-0 Preconditions
* **Mechanical Falsifiability (The Oracle):** The delivery MUST expose a deterministic execution interface (e.g., CLI, API, test harness) capable of physically proving or refuting the commissioned constraints.
* **Seeded Verification Corpora:** The delivery MUST include all malformation corpora, data sets, or mock inputs required to mathematically execute the Oracle.

### Trust Boundaries
* **Class-A (Mechanical):** Deterministic structural guards MUST be proven by explicit exit codes.
* **Class-B (Cognitive):** Semantic fidelity and truthfulness MUST be ratified via HTIL (Human-in-the-Loop) Red/Green TDD gates prior to automation.

### Execution Hygiene
* **Strict Branch Isolation:** All implementation work MUST occur on `active/*` sub-branches. Direct pushes to `main` are FORBIDDEN.
* **The HTIL Gate:** The HTIL Gate MUST exclusively occur during the Red Phase Spec review. The subsequent Green Phase executes autonomously.
* **Aggressive Execution:** The Agent MUST execute `[AUTHORIZED]` DAG nodes deterministically, bypassing conversational reflexes.

---

## Phase 2: Delivering the Commission-Delivery

### Invariants of the Commission-Delivery
* **Semantic Exit Codes:** The **Commission-Delivery** MUST parse raw exit codes into the following semantic vocabulary:
  - `[MET]`: Structural constraint passed mechanically.
  - `[REFUTED]`: Structural constraint mechanically failed.
  - `[UNVERIFIED]`: Constraint could not be tested due to missing Gate-0 prerequisites.
  - `[ACCEPTED]`: Constraint failed, but the delta traces to upstream **Commission-Request** ambiguity.
* **Total Atomic Coverage:** The **Commission-Delivery** MUST map every single atom defined in the **Commission-Request**. Omissions or sub-scoping are FORBIDDEN.
* **Structural Mirroring:** The **Commission-Delivery** tables, lists, and headings MUST perfectly mirror the topographical layout of the **Commission-Request**.
* **Contract Versioning:** The **Commission-Delivery** MUST explicitly pin the Git SHA of the **Commission-Request** evaluated against.
* **Telemetry Containment:** All raw telemetry MUST be physically isolated in collapsed appendices (e.g., `<details>` blocks).
* **OBSERVED Run-Record:** The **Commission-Delivery** MUST provide an execution record mapping every commissioned atom to an explicit run command, telemetry, and exit code.
* **Pinned Provenance:** The **Commission-Delivery** MUST explicitly point to the exact Git SHA, branch, and live file paths of the executing substrate.

---

## Phase 3: Iterative Convergence (Handling Rejections)

### Invariants of Iterative Convergence
* **Delta Monotonicity:** An iteration MUST exclusively target the topological atoms explicitly rejected in the previous payload. Modifying atoms possessing a `[MET]` status is FORBIDDEN.
* **TDD Falsification (The Red Phase Precondition):** A rejection MUST be structurally translated into a failing test case in the Commissionee's substrate prior to any implementation code modification.
* **Class-A Superiority:** All mechanical Gate-0 constraints MUST achieve `[MET]` status before Class-B cognitive disagreements are negotiated.
* **Scope Freeze:** The Commissionee MUST isolate the iteration by pinning against the original **Commission-Request** SHA. Upstream appending of new constraints to a rejected delivery payload without a version bump is FORBIDDEN.
