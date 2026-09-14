---
name: research-task
description: Manage bounded rctl research tasks, resume their handoffs, verify or close them, initialize research workspaces, and plan related experiments.
---

# Research task

Orient selected work using a fresh `rctl status TASK` or delivered reminder. Follow
its source paths for criteria, warnings, and missing or truncated details. The
retained contract owns the accepted agreement; `state.md` reports progress and
`result.md` interprets evidence. The machine record owns verification and phase.

Use the relevant reference when entering an operation:

| Operation | Reference |
| --- | --- |
| Initialize, inspect/update installation, use a vault, or migrate | [Workspace](references/workspace.md) |
| Author contract, result, review input, or handoff | [Task files and examples](references/task-files.md) |
| Propose an experiment, create its contract, or materially change scientific direction | [Planning and history reuse](references/planning.md) |
| Evaluate evidence, verify, or close | [Verification and closeout](references/verification.md) |

Before experimental planning, cite related history, what remains unanswered, and
which decision new evidence changes. For a task derived from a broader question,
use the optional Question alignment fields in the task-file reference and keep
conclusions within `This task tests` and `This task does not decide`.

Fill the agreement and acceptance criteria before `begin`. Choose methods and order
within existing authorization; preparing a contract does not require another approval.
Use domain skills for scientific methods and evidence, and rctl for this task's
lifecycle. Advice and bounded mechanical edits may stay inline without a managed task.

## Commands and addressing

`TASK` is an explicit project-relative path, such as `tasks/retained-check`.
Global options precede the command: `rctl --root /absolute/project --format json status TASK`.
JSON results are under `data`, beside `ok`, `error`, and `warnings`.

| Intent | Command |
| --- | --- |
| Find work | `rctl task list --phase active` (omit the filter for all phases) |
| Read state | `rctl --format json status TASK` |
| Refresh reminder | `rctl context [TASK]` |
| Create draft | `rctl task new TASK --kind analysis --title "Bounded question"` |
| Check structure | `rctl contract check TASK` |
| Retain agreement | `rctl begin TASK` |
| Accept changed agreement | `rctl amend TASK --reason "Why it changed"` |
| Save handoff (active) | `rctl checkpoint TASK --file .work/handoff.md` |
| Verify | `rctl verify TASK --reviews TASK/reviews.json` (omit reviews for command-only tasks) |
| Close | `rctl close TASK` |
| Resume an ended task | `rctl reopen TASK --reason "Why work resumes"` |
| Stop without closure | `rctl cancel TASK --reason "Why work stops"` |

Root selection is `--root`, then `RCTL_PROJECT_ROOT`, then the working directory.
Listing never selects a task. `RCTL_TASK_PATH` supplies an omitted task only for
context/hooks; lifecycle commands require `TASK`. CLI `--file` and `--reviews`
paths resolve from the project root; document `evidence_refs`, command `inputs`,
and command execution resolve from the task directory. Use targeted help for
unfamiliar syntax or version differences; reuse established syntax otherwise.

## Completion and handoff

Managed completion requires successful `close` with a current passing verification.
A negative or bounded inconclusive scientific result can satisfy that agreement.
Structural checks establish structure; execution and inspected evidence support a
claim. A nonzero `verify` may still save a report; inspect status after an uncertain
write before continuing.

To pause, checkpoint a handoff with `## Next action` and `## Blockers` first and one
concrete continuation step. Reported handoff progress is separate from lifecycle
advice. A chat ending does not close the task. Use uv for Python setup and execution.
