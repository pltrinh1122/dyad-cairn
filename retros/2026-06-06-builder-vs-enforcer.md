# Reflect: Builder vs Enforcer & Grain Friction

## Continue
- Explicitly falsifying our structural assumptions when friction surfaces (e.g., removing the `SecurityException` when it contradicted our role).
- Using physical, mechanical tests to prove or disprove our alignment with the Operator's directives.

## Start
- Anticipating that existing upstream grains (playbooks and structures in the Commons) may contain deeply embedded assumptions that require "re-rubbing" (falsification) when physical reality contradicts them.
- Maintaining strict separation of concerns: The tool that builds (Mason) must not be the tool that guards (Enforcer).

## Stop
- Conflating the Mason's role as a Synthesizer with the Enforcer's role as a sandbox warden.
- Attempting to handle substrate invariants using internal validation logic inside execution tools (let the dedicated CI guards do their job).
