---
name: <project>-experiment-workflow
description: Run, monitor, validate, and hand off experiments for <project> using project-specific commands, runners, output roots, health gates, and evidence rules. Use when working inside <project> on experiment execution, monitoring, profiling, result validation, or project-specific run handoff.
---

# <Project> Experiment Workflow

## Purpose

Use this adapter as command authority for <project> experiments. It records stable project rules only; runner execution state belongs in manifests, logs, and result ledgers. For an rctl-managed task, read the project-local research-task skill: its contract.md governs the comparison, result.md records findings, and rctl owns phase and acceptance. Campaign notes explain run sequence without duplicating task status.

## Use When

- launching, monitoring, profiling, validating, or resuming <project> experiments
- choosing between local, remote, queued, or managed-GPU runners
- checking preflight health, training health, output validity, or paper-facing evidence readiness

## Load Order

1. `references/runners.md` for command authority and output roots.
2. `references/preflight-health.md` before launching.
3. `references/queue-and-concurrency.md` for batch or remote jobs.
4. `references/monitoring.md` while runs are active.
5. `references/profiling.md` only for bottleneck or profiling tasks.
6. `references/result-validation.md` before claim or writing handoff.
7. `references/adapter-sources.md` when auditing or updating adapter facts.

## Rules

- Do not invent commands, paths, tracker names, remote hosts, GPU IDs, or cleanup rules.
- Do not silently change dataset, split, metric, seed policy, baseline, evaluator, or output root.
- Do not treat smoke-run, launcher success, or unparsed logs as paper-valid evidence.
- Do not store live run state in this skill.

## Outputs

- run manifest from `templates/run-manifest.md`
- campaign note from `templates/experiment-campaign.md`
- code review artifact from `templates/experiment-code-review.md` when experiment implementation changed
- result ledger from `templates/result-ledger.csv`
- fact provenance from `references/adapter-sources.md`
- handoff to `research-experiment` for result-to-claim and evidence decisions
