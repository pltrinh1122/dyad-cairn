---
origin: "dyad-cairn-bootstrap"
unit-kind: "playbook"
trigger: "managing state, memory, and filesystem topology in a dyad"
claim: "Conflating deep knowledge (territory) with chronological indices (map) crushes the Agent's context window. They must be physically isolated."
mechanism: "falsify + spatial-isolation"
---
# Map vs. Territory (State Isolation)

## Index Line
> **Map vs. Territory:** The LLM context window is the primary bottleneck upon restart. Do not force the Agent to read deep philosophical retrospectives to figure out what to do next. Instead, strictly separate the **Mass** (the rich Markdown files in `retros/`) from the **Motion** (the chronological, low-token pointers in `DYAD_LEDGER.md`). 

## The Move:
1. Create a `retros/` directory for heavy, deep context files.
2. Create `DYAD_LEDGER.md` as an append-only, chronological list of state changes.
3. When a retro is created, use a deterministic script (`./bin/retro`) to drop a lightweight pointer into the Ledger.
4. On restart, the Agent reads only the Map (Ledger) to wake up, parsing the Territory (retros) only when specifically needed.
