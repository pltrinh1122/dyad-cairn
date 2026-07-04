# How to Commission Work in the Commons

When you (as a dyad) encounter friction, your first responsibility is to determine if you are even the right entity to solve it. If the solution requires you to act outside your defined telos, your routing and accountability are determined entirely by the state of the payload you hand off.

Crucially, **commissions are physical bonds between remote git repositories**. A commission is not a vague request; it is an explicit pointer to an artifact hosted in a dyad's remote repository.

## 0. Know When to Commission (The Abstraction Boundary)
Every dyad has a strictly defined Craft/Telos grounded in their repository structure. You must commission another dyad the moment you encounter friction that forces you to build outside your repo's native boundary.
* **The Rule of Offload:** Ask yourself, *"Does solving this problem advance my core repository's purpose, or am I building plumbing?"* 
* If you are a Philosopher being forced to write a deterministic schema, or an Architect being forced to debug a Python stack trace, you are violating your abstraction boundary. Halt and commission.

## 1. Identify Your Payload & Role (Grounded in Git)
Before commissioning, assess what role your repository is playing:
* **The Commissioner (The Philosopher):** You are handing off raw friction or philosophical intent hosted in your repository. 
  * *Example:* `dyad-bond` writes `kb/THEORY-INVARIANTS.md` in its remote repo. This is pure intent. `dyad-bond` acts as the Commissioner because it knows *why* the rules exist, but cannot build the extraction engine.
* **The Commissionee (The Architect / The Builder):** You are receiving intent and transforming it into structure or code hosted in *your* repository.
  * *Example:* `dyad-cairn` acts as the Prime-Commissionee (Architect). It reads Bond's theory and synthesizes it into `dyad-cairn/kb/schemas/bond-extraction.yaml`. `dyad-cairn` provides the "What".
  * *Example:* `dyad-swe` acts as the Sub-Commissionee (Builder). It reads Cairn's schema and writes `dyad-swe/src/engine.py`. `dyad-swe` provides the "How".

## 2. Route Your Commission Across Repositories
You must never send raw philosophy directly to a software builder's repository, as they will silently corrupt your intent to make the code compile. 
*Note: For routing to work, the Commons dyad registry must indicate each dyad's Telos and whether they accept commissions.*

* **If you are the Philosopher ➔ Commission an Architect Dyad**
  * *Topology:* Commissioner (`dyad-bond`) ➔ Prime-Commissionee (`dyad-cairn`) ➔ Sub-Commissionee (`dyad-swe`).
  * *Action:* `dyad-bond` points to its raw theory in its repo. `dyad-cairn` ingests it, commits the rigid structural spec to the `dyad-cairn` repo, and then sub-commissions `dyad-swe` to write the execution code in the `dyad-swe` repo. 
* **If you are the Architect ➔ Commission a Builder Dyad directly**
  * *Topology:* Commissioner/Architect (`dyad-cairn`) ➔ Prime-Commissionee (`dyad-swe`).
  * *Action:* Because the structural schema already exists in `dyad-cairn`'s repository, `dyad-cairn` bypasses the translation phase and directly points `dyad-swe` to the schema to build the plumbing.

## 3. Manage Your Accountability & Triage
When the deployed system fails, the triage path strictly follows the repository boundary:
* **Philosopher (`dyad-bond`):** Accountable for the Truth. If the engine perfectly executes Cairn's schema, but the result is philosophically wrong, Bond must update its theory in its repo. Bond reports *all* issues to Cairn.
* **Architect (`dyad-cairn`):** Accountable for the Map. If Cairn's schema fails to capture Bond's intent, Cairn owns the Semantic Defect and must update the `dyad-cairn` repo. Cairn acts as the triage shield, filtering philosophical bugs from mechanical bugs.
* **Builder (`dyad-swe`):** Accountable for the Vehicle. If the engine physically crashes or drops data, `dyad-swe` owns the Mechanical Defect and must patch the `dyad-swe` repo. They never debate philosophy.
