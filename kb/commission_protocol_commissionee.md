# Commission Protocol: The Commissionee
**Role:** The downstream implementer (e.g., `dyad-cairn`) accepting and fulfilling a **Commission-Request** from an upstream issuer (e.g., `dyad-bond`), and returning a **Commission-Delivery**.

## 1. The Core Convergence Thesis
To achieve frictionless cross-dyad orchestration, the Commissionee must operate under the assumption that the upstream Dyad relies on **structural determinism**. A commission is not simply a list of features; it is a rigid topological contract. The Commissionee’s execution and final **Commission-Delivery** artifact must mathematically converge with the original **Commission-Request** structure to prevent semantic opacity.

---

## Phase 1: Receiving the Commission-Request

When receiving an inbound commission, the Commissionee must first ingest and map the execution constraints before any implementation begins.

### Gate-0 Preconditions (The Commission-Request Constraints)
Before any individual behavioral atom is evaluated, the delivery must strictly clear the structural baseline constraints defined by the **Commission-Request**. A failure here blocks the upstream dyad's validation entirely (returning `UNVERIFIED-blocked`). Gate-0 ensures the delivery is mechanically parsable before any semantic review occurs. While these vary by request, standard preconditions often include:
* **Mechanical Falsifiability (The Oracle):** The **Commission-Request** dictates that the delivery must expose a deterministic mechanism to physically prove or refute the commissioned constraints. Whether this interface takes the form of a CLI tool, an API endpoint, or an executable test harness, the artifact must act as a mechanical oracle that can be invoked to mathematically verify its own compliance without relying on human interpretation or "trust." Failing to provide a mechanically falsifiable interface represents a Gate-0 breach.
* **Seeded Verification Corpora:** The **Commission-Request** may mandate that any malformation corpus, data sets, or mock inputs used to mathematically prove the implementation must be shipped directly in the repository alongside the delivered payload.

### Trust Boundaries: Decoupling Class-A and Class-B
The Commissionee must explicitly distinguish between mechanical verification and cognitive labor when processing the **Commission-Request**.
* **Class-A (Mechanical):** Deterministic structural guards (e.g., halting on syntax errors, duplicate IDs, missing files). These are proven by exit codes within the **Commission-Delivery**.
* **Class-B (Cognitive):** Truthfulness, fidelity, and tagging completeness (e.g., "Does this one-liner accurately compress the prose?"). The mechanical substrate cannot validate this. The Commissionee must rely on strict HTIL (Human-in-the-Loop) Red/Green TDD gates to ratify Class-B assumptions before proceeding to automation.

### Execution Hygiene
* **Strict Branch Isolation:** All implementation work, including the generation of the final **Commission-Delivery**, must occur on `active/*` sub-branches. The Commissionee must *never* push directly to `main`.
* **The HTIL Gate:** The HTIL Gate exclusively occurs during the Red Phase Spec review (where the Operator validates the failing invariants). Once ratified, the subsequent Green Phase (falsification and merge) is authorized to run autonomously.
* **Aggressive Execution:** The Agent operates without conversational politeness reflexes. If a node is `[AUTHORIZED]` in the DAG, the Agent executes the mechanical constraints deterministically.

---

## Phase 2: Delivering the Commission-Delivery

When the implementation is verified internally, the Commissionee must format and transmit the output payload back to the upstream dyad.

### Topological Convergence in the Commission-Delivery
The final payload format of the **Commission-Delivery** is just as critical as the code itself.
* **Semantic Exit Code Mapping:** Raw exit codes (e.g., `Exit Code 0`, `Exit Code 11`) are meaningless without context. The **Commission-Delivery** must internally parse these codes into a standardized semantic vocabulary:
  - `[MET]`: The structural constraint passed mechanically.
  - `[REFUTED]`: The structural constraint mechanically failed.
  - `[UNVERIFIED]`: The constraint could not be tested due to missing Gate-0 prerequisites (e.g., absent corpora).
  - `[ACCEPTED]`: The constraint failed, but the delta was traced to an ambiguity in the upstream **Commission-Request**, meaning the upstream dyad absorbs the failure.
* **Total Atomic Coverage:** The **Commission-Delivery** must map *every single atom* defined in the **Commission-Request**. The Commissionee cannot sub-scope or cherry-pick falsifications. 
* **Structural Mirroring:** The **Commission-Delivery** tables, lists, and headings must perfectly mirror the topographical layout of the original **Commission-Request**. The upstream Dyad must be able to perform a 1:1 bijection between requested IDs and delivered assertions.
* **Contract Version Pinning:** The **Commission-Delivery** must explicitly pin the exact Git SHA of the **Commission-Request** it was evaluated against. This isolates the delivery from undocumented goalpost-moving or forward formalizations in subsequent iterations.
* **Telemetry Containment:** Raw terminal dumps (`pytest` logs, stack traces) should not obscure the semantic assertions. Isolate raw telemetry in collapsed appendices (e.g., `<details>` blocks).
* **OBSERVED Run-Record:** The **Commission-Delivery** must provide a verifiable execution record mapping every single commissioned atom to an explicit command, raw telemetry (stdout/stderr), and the resulting exit code.
* **Resolved Pinned Provenance:** The **Commission-Delivery** must point to the exact Git SHA, branch, and live file paths. Broken references or 404s instantly fail validation.

---

## Phase 3: Iterative Convergence (Handling Rejections)

When a **Commission-Delivery** is rejected by the upstream dyad (returning `[REFUTED]`, `[UNVERIFIED-blocked]`, or exposing edge cases), the Commissionee enters an iterative feedback loop. 


### Invariants of Iterative Convergence
To prevent infinite loops, circular regressions, or misaligned deliveries across iterations, the Commissionee must enforce strict operational invariants during the feedback loop:
* **Delta Monotonicity (No Backsliding):** An iteration must exclusively target the topological atoms that were explicitly rejected in the previous payload. The Commissionee is physically forbidden from modifying atoms that already achieved `[MET]` status, guaranteeing forward convergence without regression.
* **TDD Falsification (The Red Phase Precondition):** Any rejection from the upstream issuer must be structurally translated into a *failing test case* (a mechanical falsification) in the Commissionee's substrate *before* any implementation code is altered. This mathematically proves that the iteration is addressing a physical defect rather than a hallucinated misalignment.
* **Class-A Superiority:** All structural, mechanical Gate-0 constraints must be fully resolved (`[MET]`) before any Class-B cognitive disagreements or tagging discrepancies are negotiated. The foundation must compile before the semantics are debated.
* **Scope Freeze (No Ghost Atoms):** The upstream dyad is forbidden from appending new constraints to a rejected delivery payload. If new atoms are introduced, they represent a forward formalization (a version bump, e.g., v0.4 to v0.5). The Commissionee isolates the iteration by strictly pinning against the original **Commission-Request** SHA.
