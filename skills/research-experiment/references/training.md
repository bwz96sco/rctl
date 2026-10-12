# Training execution and evidence

Use project code and runner records for setup, launch, monitoring or diagnosis.
Choose implementation and execution order within the requested scope and allowance.

## Before execution

Establish model/checkpoint, data/split, objective, evaluation/decode rule, relevant
control, compute allowance and stop conditions. Reuse the accepted comparison and
runner metadata. Material scientific changes need amendment before dependent work.
Use a matching project adapter when it owns commands; verified one-off commands
can stay in the current task. Reusable operational knowledge can use the
[project-adapter reference](project-adapters.md).

Check concrete unresolved launch risks: unavailable data/checkpoints, incorrect
loading, invalid loss, accelerator occupancy or disk limits. Tiny, capped and
midscale runs are prerequisites only when the current agreement makes them so.
An authorized full run proceeds after its actual launch guards pass. Review
consequential code changes for named failures using existing evidence.

Project scripts/configs own commands. For unresolved library/API setup or training
questions, use smart-search and relevant official documentation. External training
catalogs are advisory; using this reference requires no catalog audit or source map.

## Before reporting completion

Inspect actual run state and outputs. Retain or link command/config/code/environment,
model/data lineage, logs, metrics, predictions and failures needed for the claim.
Runner-owned records can supply these facts without duplicate reports.

Distinguish launch success, workload progress, completed execution and validated
quality. Tiny overfit supports plumbing/capacity; teacher-forced scores do not
establish free-run quality. State changed comparison conditions and bound the
conclusion. A retry needs a concrete expected delta and remaining allowance.

Use [failure diagnosis](training-failures.md) for an observed failure or suspicious
metric, and [computation checks](computation-checks.md) for unresolved numerical
validity. Deliver the requested setup, observation, diagnosis or native result.
Managed verification and closure remain with research-task.

A reusable training summary is optional. The
[handoff example](../assets/training/model_training_handoff.md) links existing run
records; additional templates are a menu. From this skill directory,
`uv run --no-project --script scripts/validate-training.py ROOT` checks its structure,
not execution validity or machine acceptance. `--strict-diagnostics` requires a
separate diagnostic report only when that deliverable was requested.
