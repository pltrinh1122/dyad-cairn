# PLAN: Disambiguation of `rub:`

## 1. Riff (Brainstorming the Ambiguity)
The Operator currently uses `rub:` as an unbound conversational marker. However, the term "rub" inherently implies *friction* and can occur in two opposing directionalities within the dyad:
- **Direction A (Operator -> Agent):** The Operator is providing structural friction or critiquing an Agent's move. (e.g., "rub: your plan violates the structural mutex.")
- **Direction B (Agent -> Operator):** The Operator is *requesting* that the Agent provide a "Rub-Back" on their prompt or idea. (e.g., "rub: is this architecture lean enough?")

Currently, these two intents are conflated under the single `rub:` moniker, forcing the Semantic Router to guess the Operator's intent based on payload context.

## 2. Rub (Friction against the Riff)
- We shouldn't create excessive new markers that cause cognitive overload. 
- However, relying on context-guessing violates the Asymmetric Intake Playbook, which demands clear structural authority.
- If the Operator is *requesting* a rub-back, they are asking a question. If they are *providing* friction, they are making an assertion. 

## 3. Proposed Implementation
We disambiguate `rub:` via punctuation, mirroring the existing `lean.` vs `lean!` convention.

- **`rub:`** -> Operator provides a critique/friction against the Agent's recent action. (Assertion)
- **`rub?`** -> Operator requests a "Rub-Back" from the Agent against the Operator's idea/prompt. (Interrogation)

### Required Actions:
1. Update `commons/AGENT.md` to formally define `rub:` and `rub?` in the vocabulary.
2. Update the Intake Playbook section in `commons/AGENT.md` to instruct the Agent on how to react to each marker.

Do you approve of this disambiguation schema (`rub:` vs `rub?`)? If approved, I will implement the documentation updates and close this node.
