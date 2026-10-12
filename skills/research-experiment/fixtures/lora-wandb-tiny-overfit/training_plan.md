# Training Plan

## objective

Fixture objective: verify workflow pack for LoRA/QLoRA fine-tuning with W&B tracking and tiny-overfit gate.

## model_family

Base: `TinyLlama/TinyLlama-1.1B-Chat-v1.0` style causal LM placeholder. Adapter: LoRA r=16, alpha=32, dropout=0.05.

## dataset_and_split

Dataset: fixture JSONL instruction-response set. Split: 32 train rows, 8 validation rows. No real training claim.

## label_or_tokenization

Use tokenizer-matched chat template. Train only assistant response tokens. Check BOS/EOS and padding labels before launch.

## baseline

Baseline: base model zero-shot eval on same fixture validation prompts. Metric baseline stored in `artifacts/mock/lora/baseline_metrics.json`.

## metric_contract

Primary metric: validation negative log likelihood. Secondary: exact format match rate on 8 prompts. Tiny-overfit success: train loss below 0.05 on 2 examples within 50 steps.

## adapter_discovery

No project-local experiment adapter applies to this fixture. Use embedded fixture paths and one-off commands.

## training_lineage_contract

Architecture implementation: fixture causal LM plus LoRA adapter. Checkpoint lineage: base placeholder -> adapter-step50 fixture. Checkpoint load audit: mocked by preflight report. Dataset/split: 32 train rows, 8 validation rows. Refs/label policy: assistant-response labels only. Tokenizer/units: tokenizer-matched chat template. Decode policy: fixture prompt completion format. Metric parser: fixture JSON metric reader. Runner/env: local fixture route, Python 3.12. Comparability boundary: fixture-only, no real model quality claim.

## compute_budget

Fixture budget: mock logs only. A real run uses its current agreement's resources,
allowance and authorization; this fixture supplies none.

## source_skill_map

See `source_skill_map.md`.

## sanity_gates

Required gates: schema check, tokenizer decode check, one-batch forward, tiny-overfit, W&B offline artifact dry run.

## main_run_scope

No main run is included in this fixture. A real run follows its current agreement;
the tiny-overfit result is a prerequisite only if that agreement says so.

## stop_go_rules

Stop on NaN, loss spike above 100, missing W&B run ID/artifact path, or failed tiny-overfit. Go only if preflight and tiny-overfit pass.

## project_adapter_decision

Use one-off commands for fixture. Use the project-adapter reference if stable remote/queue command facts need a reusable home.

## claims_targeted

Workflow can claim pack completeness and validator behavior.

## claims_not_targeted

No model quality, benchmark, generalization, or performance claim.
