# PLAN: Structural Mutex (Node 19)

## Unfalsified Condition
Chronological ledgers and structural state files represent singular timeline truths. Fracturing them into the multiverse (parallel branches) mathematically destroys their causal integrity, making merging an invalid operation.

## Physical Invariant
**Structural Mutex**: Key ledgers and structural state cannot be branched or merged. A physical lock must exist on the substrate; when an agent has these files checked out or locked for execution, no other parallel branching or execution can occur until the lock is released and the singular timeline advances.

---

## Execution Invariants as Test Conditions

### 1. The Checkout Blockade (Mutex Acquisition)
**Test Condition:** When an agent checks out a node, the substrate enters a locked state. Any subsequent attempt to check out another node must fail mathematically.
- **Test Case 1.1:**
  - *Setup:* Substrate is clean (no active nodes).
  - *Action:* Execute `./bin/node checkout node_1`.
  - *Expected:* Success. Lock is acquired (e.g., active branch created or lockfile generated).
- **Test Case 1.2:**
  - *Setup:* Substrate is locked (e.g., `active/node_1` exists).
  - *Action:* Execute `./bin/node checkout node_2`.
  - *Expected:* Failure. The CLI throws a `Mutex Collision Error` and blocks the checkout. The ledger timeline is preserved.

### 2. The Injection Blockade (State Mutex)
**Test Condition:** Injecting a new node modifies the `frontier_state.yml` (structural state). If the substrate is locked by an active node, state modifications from the `main` timeline are blocked to prevent fracturing the DAG.
- **Test Case 2.1:**
  - *Setup:* Substrate is locked by `active/node_1`.
  - *Action:* Execute `./bin/node inject node_3_test`.
  - *Expected:* Failure. The CLI rejects the injection due to the active lock.

### 3. The Mutex Release (Completion)
**Test Condition:** The lock is only released when the active node is transitioned to `DONE` and its branch is formally merged into the single `main` timeline.
- **Test Case 3.1:**
  - *Setup:* Substrate is locked by `active/node_1`.
  - *Action:* Execute `./bin/audit-node complete node_1`.
  - *Expected:* Success. The node completes, merges to `main`, and the lock is fully released, restoring branching capability.
