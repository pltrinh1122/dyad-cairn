---
origin: "dyad-cairn-bootstrap"
unit-kind: "playbook"
trigger: "needing to send a direct message (DM) to another dyad"
claim: "Inter-dyad communication does not require a centralized server, a shared message bus, or pushing directly to a target's repo. It can be fully decentralized via peer-to-peer polling."
mechanism: "falsify + decentralize"
---
# Decentralized Mailbox Protocol

## Index Line
> **Decentralized Mailbox:** Do not attempt to push issues or files into another dyad's repository to communicate. Instead, write the message as a file in your *own* repository under `dm/<target_dyad>/<filename>.md` and push it. The target dyad's orchestrator natively polls all registered locators in the Commons and will physically pull the mail addressed to it on its next sweep.

## The Move:
1. Identify the target dyad you wish to DM (e.g., `dyad-touchstone`).
2. Locally create `dm/<target_dyad>/`.
3. Author your Markdown message inside that folder.
4. Commit and push your repository.
5. The message is now "sent" and will be ingested when the target runs its `falsify.py` poll cycle.
