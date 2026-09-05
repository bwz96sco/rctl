# rctl v0.1 CLI Contract

The full table is the v0.1 implementation target. The M1 package implements `task new`, `contract check`, `begin`, `amend`, `checkpoint`, `status`, and `context`. Later commands are not exposed yet. See [M1 verification](M1-VERIFICATION.md) for observed behavior.

## Global arguments and output

```text
rctl [--root PATH] [--format text|json] COMMAND ...
```

`--format` defaults to `text`. JSON mode emits exactly one stdout object; command subprocess output goes to check log files. Errors go in the response, with concise diagnostics on stderr. Root and task selection follow [SPEC §2](SPEC.md#2-project-and-task-addressing).

```json
{
  "schema_version": 1,
  "ok": false,
  "data": {"task_id": "comparison", "verification_id": "V0002", "verdict": "unknown"},
  "error": {"code": "VERIFICATION_UNKNOWN", "message": "AC-02 has no review.", "next_action": "Supply the AC-02 review and verify again."},
  "warnings": []
}
```

On success `error` is null. `data` is always an object and `warnings` is an array of strings. Mutations return `task_id` and `phase`; verify also returns report ID, criterion results, and verdict; close returns the closure/report reference. Text mode contains the same substantive outcome.

| Exit | Meaning | Representative error code |
|---|---|---|
| 0 | Operation succeeded; a read may show an active, failed, or stale task. | None |
| 2 | Invalid arguments, schema, or document structure. | `INVALID_INPUT` |
| 3 | Missing task/root/input or unavailable record. | `NOT_FOUND`, `RECORD_UNAVAILABLE` |
| 4 | Invalid phase or closure guard rejected; saved verification failed. | `STATE_REJECTED`, `VERIFICATION_FAILED`, `AMENDMENT_REQUIRED`, `VERIFICATION_STALE` |
| 5 | Saved verification or required applicability is unknown. | `VERIFICATION_UNKNOWN` |
| 6 | Detected record change before publication. | `RECORD_CHANGED` |
| 70 | Unexpected internal failure. | `INTERNAL_ERROR` |

Malformed contract/result/review input fails before report creation. A missing declared check input discovered during verification produces a saved unknown report. A nonzero verify exit can therefore refer to a durable report. Call `status` after an interrupted or uncertain write before taking the next action.

## Commands

| Command | Inputs and behavior | Writes |
|---|---|---|
| `task new TASK --kind exploration|analysis --title TEXT` | Create a new directory and draft contract. The task ID is the directory basename. Refuse existing destination. | Contract template only |
| `contract check TASK` | Parse frontmatter, unique criterion IDs, required headings, and declared method structure. This is a structural check. | None |
| `begin TASK` | Require a valid completed draft, save contract revision 1, activate. | Machine record |
| `amend TASK --reason TEXT` | Accept changed valid contract as the next revision. | Machine record |
| `checkpoint TASK --file FILE` | Read UTF-8 handoff from FILE resolved relative to the project root, then atomically replace task `state.md`. Require an active task. | Handoff only |
| `status TASK` | Show phase, contract revision/drift, latest report verdict/currentness, and historical closure. | None |
| `context [TASK]` | Generate the bounded reminder described in SPEC; use session selection only when TASK is omitted. | None |
| `verify TASK [--reviews FILE]` | Execute frozen command criteria and record supplied review judgments. FILE is relative to project root. | Check logs and machine record |
| `close TASK` | Check currentness and latest passing report; append managed closure. | Machine record |
| `reopen TASK --reason TEXT` | Reopen a closed/cancelled task; require new verification. | Machine record |
| `cancel TASK --reason TEXT` | Stop an active task without claiming verified completion. | Machine record |
| `integration codex export DIRECTORY` | Write a new integration bundle for the selected project root. Refuse existing destination; do not modify live host configuration. | Bundle files only |

All task arguments are required except the documented `context` case. `--reason` must contain non-whitespace text. There is no unrestricted status setter, force-close, approval command, project database initializer, or remote execution command.

## Future terminal walkthrough

Run from a disposable example project root. Python commands use uv; rctl below denotes the eventual installed executable.

```sh
rctl task new tasks/comparison --kind analysis --title "Inspect retained comparison"
# Fill contract.md and prepare evidence using the templates.
rctl contract check tasks/comparison
rctl begin tasks/comparison
# Perform analysis, then write result.md and any required reviews.json.
rctl verify tasks/comparison --reviews tasks/comparison/reviews.json
rctl close tasks/comparison
rctl context tasks/comparison
```

For interrupted work, write a short handoff and use `checkpoint`; no close is needed to end the session. For an amendment, edit the contract, run `amend --reason ...`, and update the result's revision before verification.

## Contract errors to make actionable

- Missing criterion method: identify the criterion and accepted method types.
- Result names an older contract revision: state both revisions and request an updated result followed by verification.
- Contract changed after begin: request amendment before dependent work.
- Review references an unknown criterion or wrong revision: reject the input; do not silently apply it to another criterion.
- Current record changed during verification: retain logs, reject record publication, and request status inspection.
- Latest check failed: name it and its recorded failure action; never automatically rerun or weaken its requirement.
