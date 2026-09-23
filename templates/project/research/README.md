# Research Overview

This directory is the static onboarding surface for the research project. It
records durable scientific context, not live experiment or task status.

## Reading Order

1. [`PROBLEM_METHODS.md`](PROBLEM_METHODS.md) — problems, candidate mechanisms,
   actual coverage and unresolved questions.
2. [`PROGRAM.md`](PROGRAM.md)'s Goal and Current guidance — scientific intent and
   established corrections.

Then follow the question at hand:

- Before proposing work, inspect related entries and evidence in
  [`ROUTES.md`](ROUTES.md), including the scope of earlier investment decisions.
- When choosing controls or interpreting comparisons, read
  [`comparison-design.md`](guidelines/comparison-design.md) and the actual versions
  in [`BASELINES.md`](BASELINES.md).
- For resources, consult [`INVENTORY.md`](INVENTORY.md); for success criteria,
  evaluation surfaces or constraints, consult the relevant PROGRAM sections.

Run `rctl context` for project guidance even before selecting a task. Reminders read
PROGRAM.md's Goal and optional Current guidance, plus ROUTES.md's Reuse Rule.
Read the linked evidence before experimental planning; short reminders are excerpts.

For current work, inspect the selected task:

```text
rctl status tasks/your-task
rctl context tasks/your-task
```

Read the current task's question, frozen plan, evidence, outcome, and next
decision. A campaign note may explain the scientific sequence; each task retains its own acceptance.

## Authority

| Location | Authority |
|---|---|
| `research/README.md` | Static entry point and reading order; never live status |
| `research/PROGRAM.md` | Slow-changing scientific intent |
| `research/PROBLEM_METHODS.md` | Open problems, method coverage and unresolved opportunities |
| `research/INVENTORY.md` | Verified resource availability |
| `research/BASELINES.md` | Versioned comparison contracts and baseline evidence |
| `research/ROUTES.md` | Scoped investment decisions; not an open-question list or task lifecycle |
| `research/guidelines/comparison-design.md` | Comparison and interpretation guidance |
| `rctl tasks/` | Active plans, execution state, task-local outcomes, and next decisions |
| `__VAULT_LOCATION__` | Long-form interpretation and literature notes |
| `Project runner storage` | Raw logs, predictions, metrics, and checkpoints |

When sources disagree, use the source that owns that kind of truth.

## Update Policy

Do not copy process state, accelerator state, ETAs, or partial metrics into this
directory. Update the owner whose durable truth changed when established, with
evidence and scope; keep per-run results in the task outcome and linked notes.
