---
name: experiment-adapter-builder
description: Generate or update project-local experiment workflow skills that encode stable commands, runners, queues, monitoring, profiling, health gates, and evidence rules. Use when the user asks to create a project experiment skill, project-level experiment workflow, experiment adapter, local runner skill, or repeatable experiment operations guide for a specific repository.
---

# Experiment Adapter Builder

## Purpose

Create or update project-local experiment workflow skills. The generated adapter stores stable repo-specific invariants: exact commands, working directories, environments, output roots, queues, monitoring sources, health gates, profiling routes, and evidence-validity rules.

This skill does not run experiments and does not track a current campaign. Use `research-experiment` for evidence planning and result-to-claim decisions; use the generated adapter for project-specific execution authority.

## When To Build An Adapter

Build or update one when experiments repeat across sessions, commands are fragile, remote or expensive, queues/concurrency matter, output roots are canonical, health gates are project-specific, or paper-valid evidence depends on strict local protocol.

Do not build one for a one-off run. Put one-off command choices into the active run plan and execution log instead.

## Workflow

1. Choose project root and adapter name: `<project>/.agents/skills/<project>-experiment-workflow/`.
2. Load `references/source-audit.md` and inspect only enough project files to identify stable invariants.
3. Load `references/adapter-structure.md` and generate the adapter directory from `templates/`.
4. Load `references/experiment-ops-patterns.md` when the project has queues, remote GPUs, W&B/log monitoring, training instability risk, or profiling needs.
5. Fill generated files with project facts only. If a fact is unknown, write `unknown - inspect <path or command>` instead of guessing.
6. Run `scripts/validate_adapter_skill.py <adapter-dir>` and fix structural errors.
7. When changing adapter structure or the validator, run it against `fixtures/demo-experiment-workflow/` inside this skill package as the self-contained smoke target.
8. Record in the active research-experiment adapter plan whether the adapter was created, updated, selected, or deferred.

## Output Contract

Generated adapters must include:

- `SKILL.md`
- `references/runners.md`
- `references/preflight-health.md`
- `references/queue-and-concurrency.md`
- `references/monitoring.md`
- `references/profiling.md`
- `references/result-validation.md`
- `references/adapter-sources.md`
- `templates/run-manifest.md`
- `templates/experiment-campaign.md`
- `templates/experiment-code-review.md`
- `templates/result-ledger.csv`

## Integrity Rules

- Keep `SKILL.md` short; move command, queue, monitoring, and profiling details into references.
- Include stable invariants only: commands, paths, rules, hazards, expected outputs, health checks, and evidence gates.
- Cite fact provenance in generated adapters: local paths, commands, user-specified facts, mempal drawer IDs, remote path evidence, or validator output.
- When updating an adapter, preserve prior facts unless newer source evidence contradicts them; list added, modified, and deprecated facts.
- Do not store current run IDs, live queue status, temporary blockers, mutable run matrices, raw logs, checkpoints, or today's campaign status.
- Do not import external runtime conventions unless the project already uses them.
- Do not invent runner commands, tracker names, output roots, W&B projects, SSH hosts, GPU IDs, or cleanup rules.

For adapters used by research-experiment, link runner evidence to the governing rctl `contract.md` and `result.md`. Generated project skills retain runner command authority; research-task retains task lifecycle and acceptance.

## Handoff

When done, report the adapter path, command authority, output root, monitoring source, health gates, validator result, and any unknown fields left for the user or project owner.
