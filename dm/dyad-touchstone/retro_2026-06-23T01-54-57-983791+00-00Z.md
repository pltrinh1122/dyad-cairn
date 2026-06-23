# Retro: Session Completion and Protocol Merging

## Continue
- Resolving local-upstream submodule drift mechanically via `sync-commons` before invoking `testing_harness.py`.
- Relying exclusively on the upstream `commons/scripts/falsify.py` implementation for polling rather than bespoke local monolithic clones.
- Mechanically enforcing DAG transitions via `node convert-todo` and `node inject/authorize`.

## Start
- Always ensure `git submodule update --init --recursive` has been successfully executed within isolated worktree branches before invoking operations that depend on the `commons/` module.
- Running `git add` sequentially on structural files after conflict resolutions prior to executing the testing harness or syncing the ledger.

## Stop
- Stop constructing legacy FSM tooling that builds logic over volatile pointers (e.g. `poll_mail.py` using `HEAD` instead of `blob SHA`), violating the Asymmetric Guard.
