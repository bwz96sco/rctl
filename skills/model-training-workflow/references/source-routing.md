# Source Routing

## Purpose

Use Orchestra AI-Research-SKILLs as model-training domain reference without importing the whole repo or overriding local experiment discipline.

## Source Basis

Public repo:

```text
https://github.com/Orchestra-Research/AI-Research-SKILLs
```

Fetched evidence shows the repo presents itself as a 98-skill AI research library across 23 categories, with training-relevant categories such as model architecture, tokenization, fine-tuning, post-training, distributed training, optimization, evaluation, inference, MLOps, and multimodal.

Pinned audit source:

```text
repo: https://github.com/Orchestra-Research/AI-Research-SKILLs.git
commit: 773a52944ba4747a18bd4ae9ade53fff041adcbc
audit: references/source-audits/orchestra-ai-research-skills-model-training.md (relative to this skill package)
```

Use the packaged [audit](source-audits/orchestra-ai-research-skills-model-training.md)
as historical inventory evidence only. The accompanying
[manual review](source-audits/orchestra-ai-research-skills-model-training-review.md)
records the original activation decision. These pinned records describe the source
at that commit; current execution and authorization rules are in this skill's
`SKILL.md` and the governing project contract.

## Category Map

Use these categories when the training problem matches:

| Need | AI-Research-SKILLs category |
|---|---|
| model family choice, clean implementation, architecture sanity | `01-model-architecture` |
| tokenizer or label-space design | `02-tokenization` |
| SFT, LoRA, QLoRA, PEFT, tool-specific fine-tuning | `03-fine-tuning` |
| RLHF/RLAIF/GRPO/DPO-family training | `06-post-training` |
| multi-GPU, FSDP, DeepSpeed, Accelerate, Ray Train | `08-distributed-training` |
| GPU cloud or launch environment | `09-infrastructure` |
| quantization, flash attention, memory/latency optimizations | `10-optimization` |
| benchmark harnesses and evaluation backends | `11-evaluation` |
| deployment/inference comparability | `12-inference-serving` |
| W&B, MLflow, TensorBoard tracking | `13-mlops` |
| VLM/audio/video/multimodal training | `18-multimodal` |

## Selection Procedure

1. Identify exact training route: architecture, data/tokenization, objective/loss, runner, evaluator, and tracker.
2. Pick at most three relevant AI-Research-SKILLs categories for this pass.
3. Check the pinned audit, then fetch or read only the matching category/skill docs.
4. Map each useful source concept into a local file: plan, preflight, run matrix, monitoring, diagnostic report, adapter, result audit, or handoff.
5. Record source URL/path, checked date, and why it was used in `source_skill_map.md`.

## Boundaries

- External skills are advisory reference material. Project scripts, configs, and local adapters remain command authority.
- Do not install all categories by default. Ask/confirm before global install, global symlink changes, or npm installer runs.
- Do not copy large external docs into local skill files. Link source and distill reusable workflow rules.
- Do not treat repo stars, category names, or examples as local evidence that training worked.

## `source_skill_map.md` Minimum Fields

```text
training_problem:
source_repo:
source_checked_at:
selected_categories:
selected_source_files_or_urls:
local_targets:
used_concepts:
waived_concepts:
command_authority:
open_questions:
```
