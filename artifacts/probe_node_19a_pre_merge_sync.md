# PROBE: Pre-Merge Sync Mechanics (Node 19a)

## 1. Investigation Objective
We needed to physically probe the mechanical behavior of concurrent git operations (specifically `git fetch` and `git rebase`) when two Dyad Agents are modifying structural files (like `DYAD_LEDGER.md`) on parallel active branches. The objective was to determine the most "wu-wei" (minimum force, with the grain) approach to prevent `git rebase` from halting on conflict markers and shattering the full-auto execution loop.

## 2. Experimental Findings
In an isolated scratch repository, we simulated a dual-agent append collision on a `.log` file and tested hooking into Git's native `.gitattributes` custom merge driver system.

**The Test:**
1. Configured a custom driver in `.git/config` (`merge.dyaddriver.driver = python3 merge_driver.py %O %A %B`).
2. Assigned the driver in `.gitattributes` (`*.log merge=dyaddriver`).
3. Induced a concurrent append conflict and executed `git rebase branch_a`.

**The Result:**
Git natively intercepted the conflict before inserting any `<<<<<<<` markers, passed the ancestor (`%O`), current (`%A`), and incoming (`%B`) file paths to the python script, and gracefully waited for an exit code. When the python script exited `0`, `git rebase` silently accepted the resolved file and continued successfully without any Operator intervention.

## 3. Discovered Invariants
### Physical Invariant: Native Git Attribute Hooking
Instead of fighting the substrate by building a custom wrapper CLI (e.g., `./bin/sync`) to manually catch and resolve rebase conflicts, we must use the grain of the substrate itself.

The invariant is: **The Dyad must install custom Git Merge Drivers into local `.git/config` and bind them via `.gitattributes`.**

By doing this, any standard `git pull --rebase` or `git merge` executed by an Agent or Operator will magically, natively auto-resolve ledger and YAML collisions in the background. The conflict resolution becomes a fundamental property of the repository environment, not an external CLI tool.

## 4. Implementation Path (For Future PLAN Nodes)
1. Write the Python merge resolution scripts for ledgers and dictionaries (to be planned in `node_19b` and `node_19c`).
2. Update the Dyad repository setup mechanics (potentially a new initialization script or an update to an existing installer) to run the `git config merge...` commands so that any environment cloning the repository natively inherits the hooks.
3. Commit a `.gitattributes` file mapping `DYAD_LEDGER.md`, `ledger.jsonl`, and `frontier_state.yml` to their respective python drivers.
