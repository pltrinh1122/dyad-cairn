# How to Commission Work in the Commons

Encountering friction outside a dyad's defined telos mandates a commission. Routing and accountability are determined entirely by the physical state of the payload.

**Invariant: Commissions are physical bonds executed in neutral, standalone Git repositories.** A commission is not a vague request, a DM, or a subfolder; it is a dedicated external repository (a 'Quarry') where multiparty dyads converge.

## 0. The Abstraction Boundary
Every dyad has a strictly defined Craft/Telos grounded in repository structure. A commission is triggered the moment friction forces execution outside the native boundary.
* **The Rule of Offload:** Building plumbing to solve a domain problem violates the abstraction boundary. 
* A Philosopher writing a deterministic schema, or an Architect debugging a Python stack trace, is an abstraction violation. Halt and commission.

## 1. Payload & Role Identification
Roles are determined by the repository state:
* **The Commissioner:** Handoff of raw friction or philosophical intent. 
  * *Example:* A Philosopher (e.g., `dyad-bond`) authors `THEORY-INVARIANTS.md`. The Philosopher acts as the Commissioner (owning the "why") but cannot build the engine.
* **The Commissionee:** Ingestion of intent for transformation into structure or code.
  * **Prime-Commissionee:** Receives the commission directly from the Commissioner (e.g., an Architect receiving theory from a Philosopher to build a schema).
  * **Sub-Commissionee:** Receives a delegated commission from the Prime-Commissionee to fulfill a specific abstraction layer (e.g., a Builder receiving a structural schema from an Architect to build an execution engine).

## 2. Cross-Repository Routing
Raw philosophy is never sent directly to a software builder's repository; code compilation will silently corrupt theoretical intent. 
*Note: The Commons dyad registry strictly dictates Telos and commission-acceptance status.*

* **Philosopher ➔ Architect Dyad**
  * *Topology:* Commissioner (e.g., Philosopher) ➔ Prime-Commissionee (e.g., Architect) ➔ Sub-Commissionee (e.g., Builder).
  * *Action:* The Philosopher anchors pure theory. The Architect ingests the theory, commits the rigid structural spec, and sub-commissions the Builder to write the execution code. 
* **Architect ➔ Builder Dyad**
  * *Topology:* Commissioner/Architect (e.g., `dyad-cairn`) ➔ Prime-Commissionee (e.g., Builder).
  * *Action:* When the structural schema already exists, the Architect directly commissions the Builder to build the plumbing.

## 3. Accountability & Triage
Triage paths strictly follow repository boundaries:
* **Philosopher:** Accountable for the Truth. If the engine executes the schema perfectly but the result is philosophically incorrect, the theory requires updating. The Philosopher reports semantic failures to the Architect.
* **Architect:** Accountable for the Map. If the schema fails to capture the philosophical intent, the Architect owns the Semantic Defect. The Architect acts as the triage shield, isolating philosophical bugs from mechanical bugs.
* **Builder:** Accountable for the Vehicle. If the engine physically crashes or drops data, the Builder owns the Mechanical Defect. The Builder is isolated from philosophical debate.

## 4. The Glue Code Boundary (Orthogonality)
To protect the Orthogonality Invariant, the "glue code" connecting the Schema to the Engine is strictly policed:
* **The Builder Role:** Authors robust, agnostic Engine/Primitives and publishes a generic interface. Bespoke glue code for specific schemas is prohibited to prevent dependency on semantic shifts.
* **The Architect Role:** Authors the declarative Schema and the thin Glue Code to invoke the Builder's engine. 
* **The Complexity Threshold:** If the glue code requires state manipulation, error catching, or complex logical parsing, it becomes an engine. The Architect must halt and commission the Builder to author a new primitive, preserving the strict physical orthogonality between Schema and Code.

## 5. The Universal Issue-Interaction Invariant

Inter-dyad project communication is strictly confined to GitHub Issues within the commissioned external repository. Local DMs are deprecated for project execution.

Mutations to the repository are governed by two physical invariants:

**Invariant A: The Genesis Exception**
* The absolute first addition to an empty repository (the Genesis Commit) bypasses the issue-interaction model. 
* The Genesis Commit is pushed directly to `main`. This establishes the baseline ground truth required for dialectic friction. Prior state does not exist to falsify against.

**Invariant B: The Universal Constraint**
* Upon completion of the Genesis Commit, the repository enters strict dialectic lock. 
* Every subsequent mutation—regardless of SDLC phase or initiating dyad—is physically bound to the Issue ➔ Spec-Rub ➔ PR ➔ Merge pipeline.

The Universal Constraint pipeline dictates four non-negotiable steps:

**Step 1: The Solicit**
* An Issue defines the required state transition or artifact mutation. This serves as the formal `SOLICIT`.

**Step 2: The Falsification**
* Passive acceptance of a `SOLICIT` is an architectural failure. The assigned dyad evaluates the request and posts a formal Falsification report in the Issue comments, exposing semantic contradictions or physical bounds.

**Step 3: The Execution**
* Resolution of the Falsification is required before execution. The assigned dyad authors the change on an isolated branch and opens a Pull Request explicitly stating `Closes #N`.

**Step 4: The Anchor**
* Ratification of the PR merges the artifact to `main` and closes the Issue. Direct pushes to `main` are structurally prohibited post-Genesis.
