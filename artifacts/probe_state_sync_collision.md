# Probe: State Sync Collision
## 1. The Collision Problem
When the Dyad scales to a Multi-Agent Architecture (e.g., an Architect Agent planning and an Executioner Agent executing simultaneously), both agents will be working in isolated Git branches (`active/<node_id>`). 

The friction arises when both agents attempt to merge their branches back to `main`. Because both agents append to the same structural files, Git will throw merge conflicts.
Specifically, collisions are mathematically guaranteed in:
1. `DYAD_LEDGER.md` (Append-only)
2. `dyad-state/ledger.jsonl` (Append-only)
3. `artifacts/frontier_state.yml` (Dictionary mutations)
4. `artifacts/frontier_state.md` (Rendered projection)

If these conflicts shatter the Executioner's mechanical loop, the full-auto sequence will fail and require manual Operator intervention.

## 2. Invariant Discovery
To prevent shattering, we must introduce physical invariants that mechanize the resolution of these specific conflicts.
Git conflict resolution must be lifted out of manual intervention and placed into a deterministic structural gate.

### Physical Invariant 1: The Pre-Merge Sync
Before an agent attempts to transition a node to `DONE` and merge to `main`, it must execute a `sync` command that fetches `main`, attempts an automatic rebase, and structurally resolves known file collisions.

### Physical Invariant 2: Deterministic Ledger Resolution
For append-only ledgers (`DYAD_LEDGER.md`, `ledger.jsonl`), if a conflict occurs, a mechanical script can simply read both conflict chunks, extract the JSON/markdown entries, sort them chronologically by their timestamp, and rewrite the file cleanly.

### Physical Invariant 3: Structural State Merging
For `frontier_state.yml`, a standard Git text merge might fail. A structural merge script can load the `.yml` from `HEAD` and the `.yml` from the incoming branch, merge the node dictionaries logically (using a last-write-wins or status-priority heuristic), and reserialize the YAML. `frontier_state.md` is simply re-projected from the resolved YAML.

## 3. Recommended Implementation Path (PLAN)
We must implement a new mechanical tool: `skills/state_sync.py` (exposed as `./bin/sync`).
This tool will:
1. `git fetch origin main`
2. `git rebase origin/main`
3. If conflicts occur, intercept them.
4. If the conflict is in `ledger.jsonl` or `DYAD_LEDGER.md`, sort and append mathematically.
5. If the conflict is in `frontier_state.yml`, perform a dictionary deep-merge.
6. Re-project `frontier_state.md`.
7. `git add` and `git rebase --continue`.

I recommend authorizing a `PLAN` node to build the schema for `skills/state_sync.py`.
