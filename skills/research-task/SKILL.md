---
name: research-task
description: Start, resume, verify, or close a bounded research task managed by rctl, preserving its contract, evidence, amendments, and cross-session handoff.
---

# Research task

Use the selected rctl task as the owner of live work. Read its `contract.md`, optional `state.md`, existing `result.md`, and `rctl status TASK` before dependent work. A hook reminder is a bounded view; follow its source paths when details or warnings affect the next action. Root and task selection are explicit (`--root`/`RCTL_PROJECT_ROOT`, `TASK`/`RCTL_TASK_PATH` for context).

## Agreement and execution

For a new task, fill the draft contract's question, scope, constraints, stop conditions, and acceptance criteria before `begin`. Each criterion states evidence, a command or review method, and the failure that changes the next action. A comparison fixes baseline/intervention, data/split, metric direction/evaluator, aggregation/selection, budget, and the stopping rule. Existing user authorization is sufficient; ask only for missing information that changes scope, authority, or acceptance.

Choose tools and execution order within the agreement. Declare checker scripts, helper files, and preexisting data as command inputs. Use bounded local validation commands; analysis generation precedes verification. New remote jobs require separate authority. An unfavorable finding is a valid outcome, not a reason to expand the budget or weaken criteria.

Before work governed by a material contract change, use `amend TASK --reason TEXT`; retain the earlier agreement. A different scientific question belongs in a new task. Appropriate scientific/domain skills may guide methods and validation, while rctl continues to own this task's lifecycle: keep contract/result/state paths and rctl commands even if a consulted skill assumes Trellis or another framework. Structural validators establish structure; actual execution and evidence inspection support the research claim.

## Evidence and closure

Write `result.md` for the current revision with outcome, evidence, deviations, next action, and limitations. Distinguish computed observations, parsed evidence, and hypotheses. Inspect the cited content before writing review entries: record pass/fail/unknown, reviewer source, rationale, and all required references. An operator-only criterion requires an operator judgment; a review label is not authenticated identity.

Run `verify TASK --reviews FILE` when reviews are required. Check every criterion and inspect command logs as needed. Nonzero verification may still save a report; use status after interruption or uncertain writes. Correct the named failure or leave work unresolved, then explicitly verify again. Changed result/evidence, amendments, and reopen cycles require fresh verification before closure.

Use `close TASK` only when the latest report passes and remains applicable. Report managed completion only after close succeeds. Scientific `not_supported` or bounded `inconclusive` results may satisfy the contract. `reopen --reason TEXT` starts a new cycle; `cancel --reason TEXT` stops work without claiming completion.

## Handoff and durable knowledge

To pause, save last verified progress, evidence locations, unresolved work, and one concrete next action with `checkpoint TASK --file FILE`. Ending a conversation does not close the task. Handoff prose describes progress; `.rctl/record.json` owns acceptance and phase, and supported CLI commands write it.

Keep slow-changing project knowledge in its existing research files. Promote only established findings at closeout; task progress and execution history stay with the task and its evidence. Use `rctl --help` for syntax. For Python setup or execution, use uv.
