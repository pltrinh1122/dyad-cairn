# Reflect: d-land implementation and subagent delegation

## Continue
- Successfully invoking subagents and delegating execution implementation workflows to them (e.g., executing the `d-rub` node), while relying on system boundaries and invariants to safely constrain their autonomous capabilities.

## Start
- Ensure the main Agent continues to use dynamic paths for scripts invoked via wrappers (like `bin/gh` and `bin/git`), avoiding brittle absolute paths that break in varying local/CI environments.

## Stop
- Cease bypassing built-in file view/search/list tools by inappropriately embedding `cat`, `ls`, or `grep` inside `run_command` bash tool calls.
