# HOW-0005: d-land Delegation (Landing Discipline)

## The Core Concept
When landing an arc (`d-land`), the Dyad practice explicitly splits responsibilities to prevent locking the main terminal and to ensure the Architect retains cognitive oversight of the handoff.

## Delegation Design Decision
1. **The Architect (Main Agent):** Retains the responsibility of parsing the conversational context and creating any pending `todo` items (via `./bin/todo`).
2. **The Executioner (Subagent):** Assumes the mechanical responsibility of serializing the state to the carry-forward ledger and updating the FSM.

## Automating the Handoff Pattern
To automate this handoff pattern and support the intended agentic architecture:
1. When the Operator issues the `d-land: <note>` moniker, the Architect evaluates the arc and authors any necessary `todos`.
2. The Architect then immediately invokes a subagent (using `invoke_subagent` with `self` TypeName and `share` Workspace).
3. The Prompt for the subagent must be: "Execute the landing discipline by running `./bin/d-land '<note>'`. Upon completion, send a message back."
4. When the subagent runs `./bin/d-land "<note>"`, the command mechanically sweeps up all pending `todos` from `artifacts/todos/` and appends them to the carry-forward note. This completes the handoff by durably serializing the context so it can be resumed effortlessly in the next session.

## Call-To-Action (CTA) Protocols for `d-land`
When the Operator invokes the `d-land` command, they may provide varying levels of context. The Architect must handle these payloads deterministically:

1. **Empty Payloads (`d-land` with no arguments):**
   - If the `d-land` command is issued without a payload, the Architect must synthesize the carry-forward note based on the established session context.
   - If there is *no prior context* in the session (e.g., invoked immediately at boot), the Architect must serialize a null-state or defer to the Operator rather than hallucinating an arc closure.
   
2. **High-G Substantive Payloads (Generative execution with no prior context):**
   - If the Operator provides a heavy, generative mandate (a "high-G" payload) directly in the `d-land` invocation *without* any preceding architectural discussion, the Architect **must not** attempt to execute the mandate in the current session.
   - Instead, the Architect must treat the high-G payload as raw intent for the *next* arc. It must parse the payload into discrete, actionable `todos` (via `./bin/todo`), and then proceed with the standard `d-land` mechanical handoff. The payload becomes the target of the next session, safely deferred rather than executed immediately.
