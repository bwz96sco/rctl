# Research Overview

This directory is the static onboarding surface for the research project. It
records durable scientific context, not live experiment or task status.

## Reading Order

1. [`PROGRAM.md`](PROGRAM.md) — scientific goal, success criteria, evaluation
   surfaces, constraints, and open questions.
2. [`INVENTORY.md`](INVENTORY.md) — verified datasets, checkpoints, code,
   environments, and infrastructure.
3. [`BASELINES.md`](BASELINES.md) — comparable evaluation contracts and audited
   baseline evidence.
4. [`ROUTES.md`](ROUTES.md) — refuted, parked, and not-executed mechanisms plus
   the evidence required to reopen them.

Run `rctl context` for project guidance even before selecting a task. Reminders read
PROGRAM.md's Goal and optional Current guidance, plus ROUTES.md's Reuse Rule.
Read the linked evidence before experimental planning; short reminders are excerpts.

After these files, inspect current work in the project's task system:

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
| `research/INVENTORY.md` | Verified resource availability |
| `research/BASELINES.md` | Audited comparable contracts and baselines |
| `research/ROUTES.md` | Refuted, parked, or not-executed mechanism-level directions |
| `rctl tasks/` | Active plans, execution state, task-local outcomes, and next decisions |
| `__VAULT_LOCATION__` | Long-form interpretation and literature notes |
| `Project runner storage` | Raw logs, predictions, metrics, and checkpoints |

When sources disagree, use the source that owns that kind of truth.

## Update Policy

Do not copy process state, accelerator state, ETAs, or partial metrics into this
directory. At task closeout, update only the control file whose durable truth
changed; otherwise keep the conclusion in the task outcome.
