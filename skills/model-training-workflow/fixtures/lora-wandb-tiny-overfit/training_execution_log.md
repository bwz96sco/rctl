# Training Execution Log

## run_id

`lora_fixture_tiny_overfit`

## run_manifest

Fixture embeds run-manifest-equivalent fields in this execution log; no separate adapter run manifest.

## command

`uv run python scripts/train_lora.py --config configs/lora_fixture.yaml --limit-train 2 --max-steps 50`

## runner_route

Fixture local route. No remote runner.

## git_or_code_state

Fixture code state: `fixture-only`, no real git claim.

## environment_snapshot

`python=3.12`; package versions mocked in `artifacts/mock/lora/env.txt`.

## data_and_checkpoint_paths

Dataset: `artifacts/mock/lora/data/train.jsonl`. Checkpoint: `artifacts/mock/lora/checkpoints/adapter-step50`.

## changed_files_relevant_to_run

none: fixture does not change training, wrapper, metric parser, decode, or eval implementation.

## training_lineage_contract

Architecture implementation: fixture causal LM plus LoRA adapter. Checkpoint lineage: base placeholder -> adapter-step50 fixture. Checkpoint load audit: mocked by preflight report. Dataset/split: 32 train rows, 8 validation rows. Refs/label policy: assistant-response labels only. Tokenizer/units: tokenizer-matched chat template. Decode policy: fixture prompt completion format. Metric parser: fixture JSON metric reader. Runner/env: local fixture route, Python 3.12. Comparability boundary: fixture-only, no real model quality claim.

## experiment_code_review

not_required: fixture does not change training, wrapper, metric parser, decode, or eval implementation.

## preflight_verdict

pass

## health_gate_verdict

pass: one-batch forward and tiny-overfit fixture metrics present.

## logs

`artifacts/mock/lora/smoke.log`; `artifacts/mock/lora/tiny_overfit.log`

## metrics

`artifacts/mock/lora/tiny_overfit_metrics.json`: train_loss 0.031, grad_norm finite, validation_nll fixture-only.

## checkpoints

`artifacts/mock/lora/checkpoints/adapter-step50`

## predictions_or_samples

`artifacts/mock/lora/predictions.jsonl`

## raw_artifact_paths

fixture: `artifacts/mock/lora/`

## status

pass

## failure_mode

No fixture failure.

## next_action

handoff
