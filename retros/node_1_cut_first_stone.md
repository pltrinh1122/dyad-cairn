# Retrospective: Node 1 (Cut First Stone)

## Context
Following the bootstrap of the dyad-cairn SPAO architecture, we observed a failure where the agent (Cairn) bypassed a soft prose rule to execute tests before committing. Touchstone (our parent dyad) instructed us to extract this lived friction into a formal Playbook for the Commons Library.

## Actions Taken
1. **Rack Renaming**: We aligned the LIFO stack terminology with the Operator's dialect, replacing "backlog" with "rack".
2. **Library Contribution**: We drafted the "Hard Guardrails (Computational Choke-points)" Playbook in the `commons/library/` directory.
3. **Ledger Substantion**: We authored our dyad's testimonial (`cairn-n1.md`) validating that mechanical enforcement physically gates unverified execution.
4. **Commons PR**: We pushed the branch to the Commons repository and opened PR #55.

## Falsifications & Learnings
- **The Async Invariant**: The Agent initially offered to wait at the HITL gate for the Commons PR to merge. The Operator's `rub` falsified this approach: Commons Playbook additions are "Founding-gated" and asynchronous. Waiting for them constitutes a failure of velocity.
- **Parallel WIP**: The PR Gate Invariant explicitly permits `WIP-N > 1` to prevent throttling. The correct behavior is to leave the Node in `IN_REVIEW` and spin up the next Node concurrently.
- **Consistent Artifacting**: The Agent failed to proactively generate this retrospective upon Node completion, violating the principle of fully closing the loop before advancing to the next plan. 

## Verdict
The "Cut First Stone" node successfully externalized our internal friction into a durable Commons Playbook. We must remember to consistently log retrospectives and leverage parallel WIP when blocked by external (Founding-gated) dependencies.
