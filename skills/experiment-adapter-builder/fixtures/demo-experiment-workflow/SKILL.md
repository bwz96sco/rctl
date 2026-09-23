---
name: demo-experiment-workflow
description: Run, monitor, validate, and hand off fixture experiments for a fictional demo project using local commands, output roots, health gates, and evidence rules.
---

# Demo Experiment Workflow

## Purpose

Use this fixture adapter as command authority for demo project experiments. It records stable fixture rules only; current run state belongs in manifests, campaign notes, logs, and result ledgers.

## Use When

- validating `experiment-adapter-builder` output contracts
- checking local demo training command, output paths, monitoring, and result validation shape

## Load Order

1. `references/runners.md` for command authority and output roots.
2. `references/preflight-health.md` before launching.
3. `references/queue-and-concurrency.md` for batch jobs.
4. `references/monitoring.md` while runs are active.
5. `references/profiling.md` only for bottleneck tasks.
6. `references/result-validation.md` before claim handoff.
7. `references/adapter-sources.md` when updating fixture facts.

## Rules

- Use only fixture commands and paths.
- Do not treat demo metrics as real evidence.
- Do not store live run state in this skill.

## Outputs

- run manifest from `templates/run-manifest.md`
- campaign note from `templates/experiment-campaign.md`
- code review artifact from `templates/experiment-code-review.md` when experiment implementation changed
- result ledger from `templates/result-ledger.csv`
