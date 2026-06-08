# Execution Spec: Node 22 (Retro CSS Formatting)

## The Invariant Discovered
The **Retro Ledger Persistence Trap**. `skills/ledger_manager.py` was physically dropping the CSS `payload` upon logging to the Ledger, saving only the `summary` string. Furthermore, the markdown generation for `DYAD_LEDGER.md` would immediately shatter the bulleted list syntax if it blindly ingested a multi-line CSS template.

## The Strategy
To enforce Cognitive State Synchronization, the machine JSONL must preserve the full payload, and the human-readable `DYAD_LEDGER.md` must render it safely without breaking structural formatting. 

We will use `<details><summary>` blocks to encapsulate the CSS payload, and apply markdown list-continuation indentation to any newlines within the message.

## Red Phase (Deterministic Execution Gate)
**`tests/test_ledger_manager.py`**
1. **`test_process_retro_persists_payload`**: Mock `append_ledger` and ensure `process_retro` passes the full `<details>`-wrapped payload when a CSS file is provided, rather than just the summary.
2. **`test_append_ledger_multiline_formatting`**: Create a mock JSONL file with a multi-line message. Run `append_ledger` and assert that the resulting `DYAD_LEDGER.md` properly indents the newlines (e.g., `\n  `) to preserve the markdown list block structure.

## Green Phase (Implementation)
**`skills/ledger_manager.py`**
1. **`process_retro(summary, file_path)`**:
   Modify to construct a `full_message` if `payload` is available:
   ```python
   full_message = f"{summary}\n\n<details><summary>View Retro Payload</summary>\n\n{payload}\n</details>"
   ```
   Pass `full_message` instead of `summary` to `append_ledger`.
2. **`append_ledger(action, message, tool_name)`**:
   Modify the markdown line rendering:
   ```python
   # Indent newlines to maintain the list structure
   formatted_message = data['message'].replace('\n', '\n  ')
   lines.append(f"- **{ts}** | `{data['action']}` | {formatted_message}")
   ```

## Closure
Once tests pass mechanically and the CI gate is cleared, transition to `DONE`.
