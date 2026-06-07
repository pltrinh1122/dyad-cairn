# HOW-0003: Dual-Agent GitHub Orchestration (PROBE)

## The Core Concept
The Dyad is split into two specialized cognitive loops:
1. **The Architect (Gemini / Local Agent):** Responsible for SENSE and PROBE. It establishes the physical invariants, updates the Theoretical framework (`AGENT.md`), defines the `CSI Guards`, and ratifies the goal.
2. **The Executioner (Claude / Remote Agent):** Responsible for PLAN, EXECUTE, and REFLECT. It receives the ratified PROBE, breaks it into executable chunks, writes the code, satisfies the tests, and opens a PR.
3. **The Anchor (Gemini / Local Agent):** Receives the PR, runs `dialect_linter.py` and `testing_harness.py`, enforces Wu-Wei closure, and merges.

## Workflow Orchestration (GitHub as the Message Bus)
To coordinate these agents without them getting entangled, GitHub is used as the asynchronous message bus.

### Step 1: Hand-Off (Architect -> Executioner)
When the Architect completes a `PROBE` node, it generates a `SPEC.md` (or simply a `READY` node on the DAG) and pushes a branch to GitHub, or opens a GitHub Issue labeled `agent:claude`.

### Step 2: The Execution Loop (Remote)
A GitHub Action workflow (`.github/workflows/claude-execution.yml`) triggers on the event.
- It spins up a remote Claude instance (e.g., using a CLI tool like `aider` or a custom script).
- Claude reads `AGENT.md` (for invariants), the DAG (`frontier_state.yml`), and the `SPEC.md`.
- Claude executes the `PLAN`, `EXECUTE`, and `REFLECT` phases.
- Claude opens a Pull Request against `main`.

### Step 3: Closing the Trail (Anchor)
- The PR triggers the mechanical CI Gates (`test_commons_sync.py`, `test_dependency_guard.py`, etc.).
- Once CI is green, the Local Agent (Architect) uses `./bin/node reflect-green` to merge the PR and transition the DAG status to `DONE`.

## Next Steps for Implementation
1. We need to define the GitHub Action workflow that will run Claude.
2. We need to decide what tool Claude will use to modify the codebase (e.g., Anthropic Computer Use, Aider, or a custom wrapper).
3. We need to update `bin/node complete` for `probe` nodes to automatically trigger the hand-off.
