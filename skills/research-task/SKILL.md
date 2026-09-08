---
name: research-task
description: Initialize a research workspace or plan experiments or start, resume, verify, or close a bounded research task managed by rctl, preserving its contract, evidence, amendments, and cross-session handoff.
---

# Research task

Use the selected rctl task as the owner of live work. Read its `contract.md`, optional `state.md`, existing `result.md`, and `rctl status TASK` before dependent work. A hook reminder is a bounded view; follow its source paths when details or warnings affect the next action. Use `rctl task list` when the task path is unknown; listing does not select a task. Root and task selection are explicit (`--root`/`RCTL_PROJECT_ROOT`, `TASK`/`RCTL_TASK_PATH` for context).

For initialization, installation diagnostics/update candidates, vault use, Git/data boundaries, or migration, first read [references/workspace.md](references/workspace.md). `rctl init [--vault PATH] [--codex]` creates missing scaffolding in the selected existing root. Inspect `.rctl/project.json` for the bound vault; no global current-task pointer is created. Advice and bounded mechanical edits may stay inline when no managed task is needed.

## Command reference

Use the commands below directly for the covered operations. `TASK` means the selected project-relative path, such as `tasks/retained-check`; substitute actual paths and reasons. Run from the project root, or prepend `--root /absolute/project` after `rctl`. Global options precede the command: `rctl --root /absolute/project --format json status TASK`. JSON responses put command results under `data`, with sibling `ok`, `error`, and `warnings` fields.

| Intent | Command | When to use |
| --- | --- | --- |
| Find work | `rctl task list --phase active` | Task path is unknown; omit the filter to include drafts and ended tasks. |
| Resume | `rctl --format json status TASK` | Read phase, revision, verification, and handoff before dependent work. |
| Read reminder | `rctl context [TASK]` | Obtain project guidance and optional selected-task context. |
| Create draft | `rctl task new TASK --kind analysis --title "Bounded question"` | New task; use `exploration` for bounded exploration. |
| Check structure | `rctl contract check TASK` | After filling the draft; does not execute criteria. |
| Begin | `rctl begin TASK` | Retain the completed draft before governed execution. |
| Amend | `rctl amend TASK --reason "Why the agreement changed"` | After editing an active contract, before dependent work. |
| Save handoff | `rctl checkpoint TASK --file .work/handoff.md` | Save prepared UTF-8 Markdown while leaving the task active. |
| Verify | `rctl verify TASK --reviews TASK/reviews.json` | Result and evidence are ready; omit `--reviews` for command-only contracts. |
| Close | `rctl close TASK` | Latest verification passes and remains current. |
| Reopen | `rctl reopen TASK --reason "Why work resumes"` | Closed/cancelled task needs another cycle. |
| Cancel | `rctl cancel TASK --reason "Why work stops"` | Stop active work without verified closure. |

CLI task paths, `--file`, and `--reviews` resolve from the project root. Inside documents, `evidence_refs`, command `inputs`, and command execution resolve from the task directory. `RCTL_TASK_PATH` supplies an omitted task only for `context` and hooks; lifecycle commands still need `TASK`.

For contract/result/review authoring, read [references/task-files.md](references/task-files.md) for matching minimal examples and command-check fields. Use the selected task's existing files when resuming. Consult targeted help (for example, `rctl checkpoint --help` or `rctl task new --help`) only for uncovered syntax, an argument error, or a version mismatch. Reuse syntax already established in the session; a new task alone does not require another help lookup.

## History before experimental planning

Before proposing an experiment, creating its contract, or materially changing direction, read `research/PROGRAM.md` and `research/ROUTES.md`, then inspect the evidence linked by related mechanisms. State what prior work answered, what remains unanswered, the substantive difference or satisfied reopen condition, and which decision the new result would change. Match mechanisms across names. If no related route is found, name the sources checked. Include this reasoning in the proposal and the contract's Question/Scope; use domain skills to judge its scientific adequacy.

`rctl context` also works without a selected task and supplies project guidance. It is a bounded excerpt: read the source when a relevant field is absent, ambiguous, or truncated. Project guidance remains reported intent, distinct from task acceptance. Keep current corrections and their evidence/scope in PROGRAM.md's `## Current guidance`; link superseding route conclusions in ROUTES.md while preserving old evidence. Update corrections when established, independently of task closeout.

## Agreement and execution

For a new task, fill the draft contract's question, scope, constraints, stop conditions, and acceptance criteria before `begin`. Each criterion states evidence, a command or review method, and the failure that changes the next action. A comparison fixes baseline/intervention, data/split, metric direction/evaluator, aggregation/selection, budget, and the stopping rule. Existing user authorization is sufficient; ask only for missing information that changes scope, authority, or acceptance.

Choose tools and execution order within the agreement. Declare checker scripts, helper files, and preexisting data as command inputs. Use bounded local validation commands; analysis generation precedes verification. New remote jobs require separate authority. An unfavorable finding is a valid outcome, not a reason to expand the budget or weaken criteria.

Before work governed by a material contract change, use `amend TASK --reason TEXT`; retain the earlier agreement. A different scientific question belongs in a new task. Appropriate scientific/domain skills may guide methods and validation, while rctl continues to own this task's lifecycle: use the domain skill for scientific methods and evidence, and research-task for contract/result/state paths and lifecycle commands. Structural validators establish structure; actual execution and evidence inspection support the research claim.

## Evidence and closure

Write `result.md` for the current revision with outcome, evidence, deviations, next action, and limitations. Distinguish computed observations, parsed evidence, and hypotheses. Inspect the cited content before writing review entries: record pass/fail/unknown, reviewer source, rationale, and all required references. An operator-only criterion requires an operator judgment; a review label is not authenticated identity.

Run `verify TASK --reviews FILE` when reviews are required. Check every criterion and inspect command logs as needed. Nonzero verification may still save a report; use status after interruption or uncertain writes. Correct the named failure or leave work unresolved, then explicitly verify again. Changed result/evidence, amendments, and reopen cycles require fresh verification before closure.

Use `close TASK` only when the latest report passes and remains applicable. Report managed completion only after close succeeds. Scientific `not_supported` or bounded `inconclusive` results may satisfy the contract. `reopen --reason TEXT` starts a new cycle; `cancel --reason TEXT` stops work without claiming completion.

## Handoff and durable knowledge

To pause, write `## Next action` and `## Blockers` first in the handoff, followed by last verified progress, evidence locations, and unresolved work; save it with `checkpoint TASK --file FILE`. Use one concrete continuation step. `status.handoff` describes reported work; `status.next_action` describes lifecycle operations. Read the source when a reminder reports missing, ambiguous, or truncated handoff fields. Ending a conversation does not close the task. Handoff prose describes progress; `.rctl/record.json` owns acceptance and phase, and supported CLI commands write it.

Keep slow-changing project knowledge in its existing research files. Promote only established findings at closeout; task progress and execution history stay with the task and its evidence. For Python setup or execution, use uv.
