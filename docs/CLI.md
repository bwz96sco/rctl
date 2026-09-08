# rctl CLI Contract

v0.3 adds `task list`, `doctor`, and `update export`, and extends handoff summaries. v0.2 added `init`; the original task lifecycle commands were implemented in v0.1.0. See [release verification](RELEASE-VERIFICATION.md) for local execution and host delivery evidence.

## Global arguments and output

```text
rctl [--root PATH] [--format text|json] COMMAND ...
```

Global arguments must precede the subcommand: use `rctl --format json status TASK`,
not `rctl status TASK --format json`.

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

On success `error` is null. `data` is always an object and `warnings` is an array of strings. Task mutations return `task_id` and `phase`; verify also returns report ID, criterion results, and verdict; close returns the closure/report reference. Text mode contains the same substantive outcome. Project `init` returns `root`, `vault`, `created`, and `preserved` paths, plus any configuration-review warnings.

`--help` and `--version` also honor JSON mode, with informational text in `data.message`. In text mode they display ordinary help/version output. Context includes a bounded reminder and a compact verification summary; `status` exposes the latest full report.

| Exit | Meaning | Representative error code |
|---|---|---|
| 0 | Operation succeeded; a read may show an active, failed, or stale task. | None |
| 2 | Invalid arguments, schema, or document structure; unsupported platform. | `INVALID_INPUT`, `UNSUPPORTED_PLATFORM` |
| 3 | Missing task/root/input or unavailable record. | `NOT_FOUND`, `RECORD_UNAVAILABLE` |
| 4 | Invalid phase or closure guard rejected; saved verification failed. | `STATE_REJECTED`, `VERIFICATION_FAILED`, `AMENDMENT_REQUIRED`, `VERIFICATION_STALE` |
| 5 | Saved verification or required applicability is unknown. | `VERIFICATION_UNKNOWN` |
| 6 | Detected record change before publication. | `RECORD_CHANGED` |
| 70 | Unexpected internal failure. | `INTERNAL_ERROR` |

Malformed contract/result/review input fails before report creation. A missing declared check input discovered during verification produces a saved unknown report. A nonzero verify exit can therefore refer to a durable report. Call `status` after an interrupted or uncertain write before taking the next action.

Ordinary commands require macOS or Linux; other platforms return
`UNSUPPORTED_PLATFORM` before project access or writes. Help/version remain available.
For an unexpected internal error, `RCTL_DEBUG=1` adds the traceback to stderr while
preserving the exit-70 JSON envelope. Inspect status before reproducing a mutation
that might already have written files. This debug option does not change hook exception
containment; it applies to the ordinary CLI error boundary.

## Commands

| Command | Inputs and behavior | Writes |
|---|---|---|
| `init [--vault PATH] [--codex]` | Initialize the existing selected root; save an immutable vault binding, create missing research orientation and project-local task skill, and optionally scaffold a new vault and Codex files. Preserve existing text; reject path collisions or changed binding before writes. | Missing project files only |
| `task new TASK --kind exploration|analysis --title TEXT` | Create a new directory and draft contract. The task ID is the directory basename. Refuse existing destination. | Contract template only |
| `contract check TASK` | Parse frontmatter, unique criterion IDs, required headings, and declared method structure. This is a structural check. | None |
| `begin TASK` | Require a valid completed draft, save contract revision 1, activate. | Machine record |
| `amend TASK --reason TEXT` | Accept changed valid contract as the next revision. | Machine record |
| `checkpoint TASK --file FILE` | Read UTF-8 handoff from FILE resolved relative to the project root, then atomically replace task `state.md`. Require an active task. | Handoff only |
| `status TASK` | Show phase, contract revision/drift, latest report verdict/currentness, and historical closure. | None |
| `context [TASK]` | Generate the bounded reminder described in SPEC; use session selection when TASK is omitted, or return project-only context if unset. | None |
| `verify TASK [--reviews FILE]` | Execute frozen command criteria and record supplied review judgments. FILE is relative to project root. | Check logs and machine record |
| `close TASK` | Check currentness and latest passing report; append managed closure. | Machine record |
| `reopen TASK --reason TEXT` | Reopen a closed/cancelled task; require new verification. | Machine record |
| `cancel TASK --reason TEXT` | Stop an active task without claiming verified completion. | Machine record |
| `integration codex export DIRECTORY` | Write a new integration bundle for the selected project root. Refuse existing destination; do not modify live host configuration. | Bundle files only |

All task arguments are required except the documented `context` case. `--reason` must contain non-whitespace text. There is no unrestricted status setter, force-close, approval command, project database initializer, or remote execution command.

## Discovery and installation maintenance (v0.3)

```sh
rctl task list
rctl task list --phase active
rctl --format json task list
rctl doctor --codex
rctl update export .work/rctl-update --codex
```

`task list [--phase draft|active|closed|cancelled]` returns `data.tasks` sorted by
path, with `task_id`, `path`, nullable `title`/`phase`, verification summary,
`currentness`, warnings, and nullable error. Unavailable entries remain visible through
filters. Missing tasks directory is an empty successful list; custom task paths remain
usable through explicit per-task commands. No current task is chosen.
An existing file at `tasks/` returns `INVALID_INPUT` with `Expected directory: tasks`.
In-root aliases appear once, with the resolved task path and matching ID. Text titles
use one line of at most 160 characters; JSON titles remain complete.

`status` and `context` add `handoff: {next_action, blockers}` (nullable strings).
The existing `next_action` still describes lifecycle operations. Context bounds these
fields and prominently labels reported work separately from acceptance. Ended-task
handoffs are historical; missing or ambiguous fields point to `state.md`.
Code blocks inside explicit handoff fields are preserved. Unavailable evidence paths
do not prevent reading managed task titles or handoffs; verification path rules still apply.

`doctor [--codex]` returns `root`, `rctl_version`, `codex_inspected`, `review_needed`,
and `findings` with path, status, message, and next action. Inspection completion exits
0 even when findings need attention. Uninspectable roots/invalid CLI arguments use
existing errors. Without `--codex`, host configuration is explicitly not inspected.
Only project-local configuration is covered; static validity does not prove delivery
or trust. Differences are review candidates, not automatically diagnosed corruption.
In-root skill symlinks are reported at their logical installation paths; `.DS_Store`
files do not request review. A missing rctl entrypoint becomes an unavailable finding,
and the remaining inspection still completes with exit 0.

`update export DIRECTORY [--codex]` refuses an existing or live-asset destination.
It returns the directory and written file names. The bundle has `candidates/`, `diffs/`,
`inspection.json`, and `README.md`. Host candidates are merge fragments; skill candidates
are individual packaged files. Existing local extras are reported and retained. It
never applies updates or modifies global installation/configuration. Inspect the bundle,
then apply only reviewed changes within the separately selected project's scope.
With `--codex`, an unavailable local entrypoint returns `NOT_FOUND` before any writes.

## Internal host command

`rctl [--root PATH] hook codex` reads host JSON from stdin and returns raw Codex hook JSON, independently of `--format`. It does not use the ordinary CLI envelope. Supported events provide bounded additional context; unsupported or malformed input returns `{}`. Adapter failures exit 0, with diagnostics on stderr where applicable. See [INTEGRATION](INTEGRATION.md) for payloads, task selection, receipt logging, and budgets. Global options such as `--root` precede the subcommand.

## Terminal walkthrough

Run from a disposable example project root. Python commands use uv; `rctl` below denotes the installed executable (`uv run rctl` when using this checkout).

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

- Malformed record: name the failing field/constraint or lifecycle invariant; preserve the record and restore valid history.
- Evidence changed during verification: name the path and any executed command criteria declaring it. If a checker generates evidence, run generation before verification and amend the frozen command to a read-only check when necessary.
- Missing criterion method: identify the criterion and accepted method types.
- Result names an older contract revision: state both revisions and request an updated result followed by verification.
- Contract changed after begin: request amendment before dependent work.
- Review references an unknown criterion or wrong revision: reject the input; do not silently apply it to another criterion.
- Current record changed during verification: retain logs, reject record publication, and request status inspection.
- Latest check failed: name it and its recorded failure action; never automatically rerun or weaken its requirement.

## v0.4 context availability

`context` without a selected task succeeds with project-only context, including in
roots without initialization. `data.available` means any usable project guidance or
task context; `task_selected` and `task_available` distinguish selection and successful
task reading. `project` contains `available`, nullable bounded `goal`, `current_guidance`,
`reuse_rule`, and relative `sources`. These are reported guidance, not acceptance.
Valid selected tasks retain their existing top-level status fields. A selected-task
failure keeps the original nonzero exit/error, project data and reminder, plus warnings.
No selection supplies no invented task status. Root/argument errors still fail normally.
