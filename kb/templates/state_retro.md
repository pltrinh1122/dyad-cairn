# State: Reflect

## Consistency Guardrail
Conversational state transitions are mathematically forbidden. When entering a formal state (e.g., `reflect:`), the Agent must engage a physical lock (e.g., `./bin/reflect-start` creating `RETRO_ACTIVE.lock`). The SPAOR execution stack (`plan`, `checkout`, `reflect`) is violently blocked until the lock is resolved via its corresponding physical closure script (e.g., `./bin/reflect`).

## Bidirectional Retrospectives (CSS Guarded)
A formal Operator Reflect must always be countered by an internal Agent Reflect. Generative formatting memory is mathematically forbidden. The Agent's reflect must strictly adhere to the `kb/templates/reflect.md` CSS template (Continue, Start, Stop) and must be mechanically validated via `./bin/reflect "summary" path/to/reflect.md`. To satisfy the Dialect Linter's UI Presentation Guard, the Agent MUST explicitly render the exact string `📋 [MECHANICAL UI PRESENTATION: REFLECT SUMMARY]` and the full CSS template output directly in its chat response.
