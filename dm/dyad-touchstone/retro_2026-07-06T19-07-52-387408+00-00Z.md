# Retro: Formalizing Commission Artifact Standards & Rejecting Metadata Bloat

## Continue
- **Identifying and rejecting standards bloat:** Rather than blindly adopting all upstream requirements from `pltrinh1122/standards`, recognizing when fields (like `review_status` or `version`) overlap with existing deterministic infrastructure (Git, CI/CD, the Ledger) and explicitly waiving them to prevent split-brain state.
- **Decoupling static from dynamic:** Formally recognizing that dynamic execution records (run-records, `[MET]`, `[REFUTED]`) belong exclusively in the transactional layer (e.g. `DYAD_LEDGER.md` or DM payloads) and forbidding them from polluting static architectural contracts.
- **Eating our own dog food:** When defining a standard (like ATX headings), applying that exact standard to the document defining it, ensuring structural isomorphism.

## Start
- Apply minimalist principles to metadata. Whenever importing an external standard, filter it through the strict operational needs of the dyad rather than wholesale adoption. Only retain fields that provide mechanical value to the downstream test harnesses (e.g., `grounds_on` for scope freeze pinning).
- Use explicit topological anchors (ATX headings) for every identifiable atom to guarantee deterministic cross-referencing capabilities for downstream tools and operators.

## Stop
- Stop treating generic documentation patterns (like bolded list items or markdown tables) as acceptable boundaries for machine-readable contracts. If it's a verifiable atom, it requires a deterministic HTML anchor.
