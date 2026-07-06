# Reflect: Falsifying Survivor Bias (The GAP Trap)

## Continue
We must continue falsifying our assumptions by looking at the discrepancies between local test execution and remote GitHub Actions Pipeline (GAP) states.

## Start
We must start physically verifying the remote GAP status before assuming a phase (Red or Green) has truly completed. Relying purely on local `run-tests` introduces a dangerous **Survivor Bias** where environmental drift (e.g., Git file permission modes like `100644` vs `os.X_OK`) creates a split-brain condition—passing locally but failing in the GAP. We must "codify" GAP verification into the SPAOR execution flow to prevent this.

## Stop
We must stop implicitly trusting the local testing substrate when determining if a PR is ready. A successful local `run-tests` is necessary but not sufficient.
