---
name: model-training-workflow
description: Set up LoRA, QLoRA, PEFT, W&B-tracked, launch-guarded, route-validation-gated, distributed, multimodal, or other ML model training workflows; run preflight checks, monitor training health, diagnose collapse or metric bugs, and hand off bounded evidence to experiment workflows using local contracts plus external Orchestra AI training references.
---

# Model Training Workflow

## Purpose

Turn model training work into reusable evidence: source-informed training setup, data/tokenization checks, cheap launch guards, explicit route-validation gates, monitored runs, failure diagnosis, bounded claims, and handoff into `research-experiment`.

This skill is a controller. It does not replace project code, `research-experiment`, or project-local adapter skills. It uses AI-Research-SKILLs as a domain-reference catalog for model architecture, tokenization, fine-tuning, post-training, distributed training, evaluation, MLOps, optimization, inference, and multimodal guidance.

Current status: active v1 after pinned source audit, selected manual source reads, fixture validation, package validation, and repository validation. Keep external Orchestra skills advisory; local project commands remain authority.

## Artifact Root

Choose root before work:

1. If `.rctl/project.json` binds a vault -> `<vault>/model-training/<topic-slug>/`; otherwise retain the existing project note convention.
2. Otherwise -> `artifacts/model-training-workflow/<topic-slug>/`.

Keep raw checkpoints, logs, tracker exports, datasets, and generated predictions in project canonical run storage. Link them from pack files.

When this work belongs to an rctl task, read the project-local research-task skill and governing contract before execution. Training plans describe implementation; they do not replace the contract or own task phase. Freeze the scientific comparison before claim-carrying runs and amend before dependent changes.

## Workflow

Load only needed references.

0. Adapter discovery: resolve `.agents/skills/*-experiment-workflow/` from the repo root of the code being trained, read/select the matching project adapter before writing a plan or launching work, choose by project/name match when multiple adapters exist, and ask the user if the match is ambiguous; record the result in `training_plan.md`.
1. Source route: read `references/source-routing.md` -> `source_skill_map.md`.
2. Training contract: define objective, dataset/split, metric, baseline, budget, model family, source refs, project adapter, and lineage contract -> `training_plan.md`.
3. Project adapter: use selected adapter command authority when available; if commands are repeated, remote, fragile, or expensive and no adapter exists, route to `$experiment-adapter-builder`; otherwise record one-off commands in the plan.
4. Preflight: data/schema/tokenizer/model/env/GPU/checkpoint/license/docs checks -> `preflight_report.md`.
5. Gate plan: classify each check as launch guard, route-validation experiment, or main-run health monitor; record approval policy -> `training_run_matrix.yaml`.
6. Execute and monitor: if a user-approved full-run contract exists and launch guards pass, launch the planned full run immediately; track run manifest, lineage, health, and persistence -> `training_execution_log.md` (manifest = adapter path or embedded, never both).
7. Diagnose: read `references/failure-taxonomy.md` when training fails, plateaus, collapses, or gives suspicious metrics -> `training_diagnostic_report.md`.
8. Handoff: inspect evidence against the experiment task's `contract.md` (frozen before claim-carrying runs), keep training evidence in runner-owned artifacts, and write its native `result.md`; use research-task for verification and closure -> `model_training_handoff.md`.

## Source Routing

- Use installed Orchestra skills only when already present under `~/.orchestra/skills/` or explicitly installed by user.
- If absent, use `smart-search-cli` to fetch the public repo/category pages or source files. Do not use native web search.
- Use `smart-search-cli` for exact library/API setup/config docs.
- Use project docs and scripts as command authority. External skills suggest patterns, not project commands.
- Do not install all AI-Research-SKILLs or change global agent config without explicit confirmation.

## Training Evidence Rules

- Smoke success is not evidence that training works.
- Tiny overfit proves plumbing and capacity only; capped/full split proves generalization.
- Teacher-forced accuracy is not free-run decode quality.
- Baseline comparison is invalid if dataset, split, metric, tokenizer, prompt/decode rule, seed, or checkpoint differs without a recorded comparability boundary.
- Training lineage must record architecture implementation, checkpoint lineage and load audit, dataset/split, refs/label policy, tokenizer or units, decode policy, metric parser, runner/env, and comparability boundary.
- Every claim needs concrete paths: command, config, git state, env, logs, checkpoint, metrics, predictions, validation, and failure evidence.
- Stop or redesign when repeated retries produce no interpretable delta.

## Gate And Approval Rules

- Keep cheap launch guards: path checks, checkpoint/load audit, one-batch forward/load audit, CUDA/env/disk risk, and invalid-loss checks.
- Treat tiny, capped, held-out, and midscale runs as explicit route-validation experiments unless the approved contract names them as blockers.
- Do not invent tiny/capped/midscale blockers after a user-approved full-run contract or passed launch gate.
- Full-run approved + launch guards pass -> start full training immediately.
- If a project adapter, queue note, or older campaign artifact says small/midscale gates block full training but the current approved contract does not explicitly name them as blockers, treat that artifact as stale: update or supersede it, then launch after cheap guards pass.
- When reporting route-validation results, state whether they are launch guards, route evidence, or main-run health. Never imply route-validation evidence blocks full training by default.
- Stop launch only for concrete blockers: failed launch guard, occupied accelerator, missing checkpoint/data, failed load audit, CUDA error, invalid loss, or disk risk.
- If training scripts, wrappers, metric parser, decode, or eval code changed, complete experiment code review before any expensive run. "Changed" means a diff against the `code_state` recorded in the comparison baseline run's manifest, or against the last reviewed run when no baseline exists.
- Repeated small-gate failure -> redesign route instead of adding another sanity-check loop.

## Tool Routing

- `research-experiment`: one task-system experiment contract, linked run evidence, explicit amendments, and validated closeout.
- `experiment-adapter-builder`: stable project commands, queues, remote GPUs, monitoring, health gates, profiling.
- Read the shared [computation checks](../research-theory/references/computation-checks.md) when numerical validity or local software usability remains unresolved after the existing training checks. Reuse the current run evidence.
- `paper-discovery`: project-scoped baseline, dataset, and benchmark paper pools with Zotero deduplication.
- `research-literature`: anchored full-paper evidence for baseline, dataset, and benchmark claims.
- `smart-search-cli`: AI-Research-SKILLs repo evidence, library/API docs, setup/config/code examples, and current web/source facts.

## Exit Criteria

Run `scripts/validate_model_training_pack.py <artifact-root>` before treating pack as reusable.

Finish only when source references are mapped, data/model/metric preflight is explicit, every gate is classified as launch guard, route validation, or main-run health, monitoring and raw artifact paths are durable, training failures are classified, claims are bounded, and next action is one of: continue, retry-with-delta, debug, scale, compare, hand off to `research-experiment`, redesign, or park.
