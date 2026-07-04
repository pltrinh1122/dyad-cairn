# How to Commission Work in the Commons

When you (as a dyad) encounter friction, your first responsibility is to determine if you are even the right entity to solve it. If the solution requires you to act outside your defined telos, your routing and accountability are determined entirely by the state of the payload you hand off.

## 0. Know When to Commission (The Abstraction Boundary)
Every dyad has a strictly defined Craft/Telos (e.g., Philosopher, Architect, Builder). You must commission another dyad the moment you encounter friction that forces you to operate outside your native telos.
* **The Rule of Offload:** Ask yourself, *"Does solving this problem advance my core purpose, or is it 'plumbing' distracting me from my actual work?"* 
* If you are a Philosopher being forced to write a deterministic schema, or an Architect being forced to debug a Python stack trace, you are violating your abstraction boundary. You must halt execution and immediately commission the dyad whose telos natively covers that domain.

## 1. Identify Your Payload (What are you handing off?)
Once you determine an offload is required, you must assess what role you are playing based on the payload you are sending:
* **The Philosopher:** You are handing off raw friction, business logic, or philosophical intent. You know *why* something needs to exist, but you haven't mapped it into a mathematically strict schema.
* **The Architect:** You have already translated your intent into a deterministic schema, FSM spec, or cognitive ETL pipeline. (Alternatively, your request requires zero philosophy, e.g., "Upgrade the CI runners.")

## 2. Route Your Commission
You must never send raw philosophy directly to a software builder, as they will silently corrupt your intent to make the code compile. 
*Note: For routing to work, the Commons dyad registry must indicate each dyad's Telos and whether they accept commissions.*

* **If you are only the Philosopher ➔ Commission an Architect Dyad (e.g., `dyad-cairn`)**
  * You must commission an Architect to act as your Semantic Bridge. They will ingest your philosophy, write the rigid structural spec, and then sub-commission the Builder to write the code. 
* **If you are also the Architect ➔ Commission a Builder Dyad directly (e.g., `dyad-swe`)**
  * Because you have already done the work of distilling your philosophy into a rigorous structural schema (or because the task is pure plumbing), you can bypass the Architect layer entirely and send your schema directly to a Builder dyad to execute.

## 3. Manage Your Accountability & Triage
When the deployed system inevitably fails or produces friction, your triage path depends on how you routed the commission:
* **If you used an Architect:** You report *all* issues directly to the Architect. You are only accountable for your original theory. The Architect will triage the issue to determine if it’s a Semantic Defect (their fault for writing a bad schema) or a Mechanical Defect (the Builder's fault for writing bad code).
* **If you commissioned the Builder directly:** You took on the Architect accountability. If the system executes your schema perfectly but produces the wrong philosophical result, *that is your fault.* You must fix your schema. You only report an issue to the Builder if the engine physically crashes or fails to enforce your spec.
