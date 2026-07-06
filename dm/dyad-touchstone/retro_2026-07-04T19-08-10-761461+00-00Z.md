# Reflect: Standup, Mechanical Debt Closure, and the Steward RUB

## Continue
- Verifying substrate viability against the actual pinned toolchain (Python 3.12, per `.github/workflows/*`) before trusting a local failure as a real code defect — the initial `SyntaxError` on `./bin/start` was my environment's `python3` (3.11), not a bug in `flow_state_manager.py`.
- Treating an existing Red test as the spec to satisfy, not license to invent new logic: `test_substrate_form.py` already named the exact wording required; the fix was transcription into `DYAD.md`, not authorship.
- Attacking my own claims as hard as an external one: claim 1c of the RUB looked like a real crack (the invariant reading born-asserted, not forged) until `DYAD_LEDGER.md`'s genesis-commit history was actually checked — the claim survived, and reporting that reversal is more honest than only reporting the frictions that stick.
- Marking `NA` instead of manufacturing a `FALSE` I couldn't back: the wu-wei/bond/healer/touchstone halves of the RUB's evidence were out of my repo scope, and saying so is the mortar rule applied to my own verdict, not just to Commons material.

## Start
- Before opening a rub/falsification verdict-DM, checking whether the FR bundles quoted evidence + blob SHA for any peer anchor it cites as load-bearing — if not, say so up front (as a scoping caveat on the verdict) rather than silently under-verifying. Already proposed to steward as a process fix; worth holding myself to it too.
- Pinning the actual interpreter/venv explicitly in this session's shell (`PATH=".../.venvs/dyad-cairn/bin:$PATH"`) before running `./bin/run-tests`, rather than re-discovering the 3.11-vs-3.12 mismatch each time a fresh shell forgets it.

## Stop
- Treating `dyad-state/fsm_state.yml` divergence from `DYAD.md`'s documented `dyad-state/active_anchor` path as something to quietly work around without ever flagging the doc/implementation drift itself back to the ledger — noted this session, not yet fixed upstream.
- Assuming a repo-scope limitation (no access to a cited peer dyad) means "can't render a verdict" — `NA` is a legitimate, mechanically honest verdict state, not a blocker to close out the rub.
