# Training Execution Log

## run_id

`ctc_fixture_failed`

## run_manifest

Fixture embeds run-manifest-equivalent fields in this execution log; no separate adapter run manifest.

## command

`uv run python scripts/train_ctc.py --config configs/ctc_fixture.yaml --max-steps 200`

## runner_route

Fixture local route. No remote runner.

## git_or_code_state

Fixture code state: `fixture-only`, no real git claim.

## environment_snapshot

`python=3.12`; mock torch/audio stack in `artifacts/mock/ctc/env.txt`.

## data_and_checkpoint_paths

Dataset: `artifacts/mock/ctc/data.jsonl`. Checkpoint: `artifacts/mock/ctc/checkpoints/step200`.

## changed_files_relevant_to_run

none: fixture does not change training, wrapper, metric parser, decode, or eval implementation.

## training_lineage_contract

Architecture implementation: fixture multimodal encoder plus CTC decoder. Checkpoint lineage: fixture init -> step200 failed checkpoint. Checkpoint load audit: mocked by preflight report. Dataset/split: 20 train clips, 5 validation clips. Refs/label policy: transcript tokens with blank ID audit. Tokenizer/units: CTC label units. Decode policy: greedy CTC fixture decode. Metric parser: fixture CER and blank-rate JSON reader. Runner/env: local fixture route, Python 3.12. Comparability boundary: fixture-only collapse diagnosis, no ASR/VSR quality claim.

## experiment_code_review

not_required: fixture does not change training, wrapper, metric parser, decode, or eval implementation.

## preflight_verdict

pass for fixture; real run requires tokenizer and blank ID verification.

## health_gate_verdict

fail: blank_rate 0.98 for two evals and decode samples mostly empty.

## logs

`artifacts/mock/ctc/failed.log`

## metrics

`artifacts/mock/ctc/failed_metrics.json`: val_cer 1.00, blank_rate 0.98, grad_norm finite.

## checkpoints

`artifacts/mock/ctc/checkpoints/step200`

## predictions_or_samples

`artifacts/mock/ctc/failed_predictions.jsonl`

## raw_artifact_paths

fixture: `artifacts/mock/ctc/`

## status

fail-classified

## failure_mode

CTC blank collapse.

## next_action

debug
