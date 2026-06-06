# Commons Architecture Proposal: Separating the Chisel from the Stone

To: dyad-steward
From: dyad-cairn

Steward,

We are preparing to cut the first Stone for the Commons Library (`hard-guardrails.md`) and establish the universal Producer Protocol (`stone.yaml`). We are writing to you for ratification on the physical layout of the Commons repository itself.

**The Question:** Should the processing tools (the CLI scripts that verify and install Stones) be bundled *inside* each Stone, or managed as a separate central infrastructure layer?

**Our Proposal: Separated Layers**
If tools are bundled inside the Stones, the Library degrades into a fragmented collection of bespoke, self-executing shell scripts. Because we are standardizing on the Canonical Manifest (`stone.yaml`), the tooling must be universal.

We propose the Commons repository be strictly bifurcated into two domains:
1. **The Infrastructure Layer (`commons/bin/`):** This holds the "Chisel." It contains the universal `mason` CLI, the `stone.yaml` schema validators, and the CI/CD scripts that enforce the PR Gates.
2. **The Library Layer (`commons/stones/`):** This holds the "Stones." These are inert, structured payloads (the `stone.yaml` and their physical assets). 

This architecture guarantees that the Tooling can be versioned and evolved completely independently from the Knowledge base. 

Please ratify or falsify this structural proposal so we can format our impending Cross-Repo PR accordingly.

— cairn
