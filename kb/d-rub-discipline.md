# HOW-0006: d-rub Discipline

## The Core Concept
The `d-rub` discipline encapsulates the semantic process of "Rubbing" an intent (resolving WHAT, WHY, and SCOPE) into a fully authorized Node. 

## Automating the Rub Pattern
When the Operator invokes the `d-rub` command (e.g. `d-rub: <target_id> --what "..." --why "..." --scope "FRONTIER"`), the Architect evaluates the missing semantic fields.
The Architect delegates the mechanical operation to the Executioner subagent to run `./bin/d-rub <args>`.

1. The Executioner subagent executes `./bin/d-rub <args>`.
2. The `d-rub` discipline invokes the underlying `./bin/rub` script to populate the target artifact.
3. If the Rub Matrix is complete, it automatically triggers conversion of the artifact into an authorized DAG node.
4. The discipline records the completion of this semantic alignment in the Dyad Ledger.
