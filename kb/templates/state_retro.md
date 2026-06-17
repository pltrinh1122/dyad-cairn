# State: Retro

## Consistency Guardrail
Conversational state transitions are mathematically forbidden. When entering a formal state (e.g., `retro:`), the Agent must engage a physical lock (e.g., `./bin/retro-start` creating `RETRO_ACTIVE.lock`). The SPAOR execution stack (`plan`, `checkout`, `reflect`) is violently blocked until the lock is resolved via its corresponding physical closure script (e.g., `./bin/retro`).

## Bidirectional Retrospectives (CSS Guarded)
A formal Operator Retro must always be countered by an internal Agent Retro. Generative formatting memory is mathematically forbidden. The Agent's retro must strictly adhere to the `kb/templates/retro.md` CSS template (Continue, Start, Stop) and must be mechanically validated via `./bin/retro "summary" path/to/retro.md`. To satisfy the Dialect Linter's UI Presentation Guard, the Agent MUST explicitly render the exact string `📋 [MECHANICAL UI PRESENTATION: RETRO SUMMARY]` and the full CSS template output directly in its chat response.
