# State Arc Start

## Intent
<What is the exact goal of this state arc?>

## Initial State
<What is the current state of the workspace and the DAG?>

## Actions Required
- [ ] Define boundaries
- [ ] List required nodes
- [ ] Identify dependencies

## Transition Conditions
<What must be true for this state arc to be considered complete?>

## Lineage Dialect (The Mechanical Bindings)
Inherited from our parent (`dyad-touchstone`) and mechanically enforced:
- `bind:` forge an Ontological Bond. **Mechanically mapped to:** `./bin/bind "<Message>"` (Synchronously validates Theory, Mechanics, and State).
- `lean.` advance to the design-review gate. **Mechanically mapped to:** `./bin/node inject <node_id> "<Title>" "<Goal>"` (Defaults node to `IN_REVIEW`).
- `lean!` surface and take the move. **Mechanically mapped to:** `./bin/node authorize <node_id>` (Transitions node to `READY`).
- `reflect-green` / `complete` (Wu-Wei Closure). **Mechanically mapped to:** requiring a `<retro_msg>` argument to append the closure synthesis to the Ledger before locking the state.
- `execute:` formally dispatch a subagent to resolve a node. **Mechanically mapped to:** The `invoke_subagent` tool. *(Note: The UI-level `/goal` command is strictly retired and forbidden. We exclusively rely on the Agent-steered `execute: <node_id>` dialect to cement Agent autonomy over execution while keeping the main terminal unlocked).*
- `read:` (or `read`, `read.`) implicitly maps to `read: quarries`. **Mechanically mapped to:** `./bin/read quarries` (or other targets if specified).
- `pr:` pull request actions. **Mechanically mapped to:** `./bin/pr-sync`. *(Note: Explicitly forbid the use of raw `gh pr create` or `gh pr merge` to ensure CSI Guard telemetry is captured).*
- *Other conversational markers (unbound):* `rub:`, `riff:`, `todo:`, `pin:`, `fb:`, `retro:`, `lean?`, `follow:`, `clip:`

## Invariants
- **PR Constraint:** The Agent must never use raw `gh pr create` or `gh pr merge`. All PR actions must be mapped to `./bin/pr-sync`.
