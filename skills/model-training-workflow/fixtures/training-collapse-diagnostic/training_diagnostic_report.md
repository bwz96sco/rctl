# Training Diagnostic Report

## run_id

`ctc_fixture_failed`

## failure_layer

evaluation_decode

## failure_type

ctc_blank_collapse

## observed_signal

Blank_rate stayed at 0.98 for two evals; validation CER stayed at 1.00; prediction samples mostly empty.

## evidence_paths

`artifacts/mock/ctc/failed_metrics.json`; `artifacts/mock/ctc/failed_predictions.jsonl`; `artifacts/mock/ctc/failed.log`

## data_diagnostics

Mock labels non-empty and label length <= frame length. Real run must repeat this check on full split.

## tokenization_or_label_diagnostics

Blank ID inside vocab range. Suspect loss weighting or decoder initialization, not missing labels.

## optimization_health

Grad norm finite. No NaN. LR may be too high for decoder warmup.

## evaluation_or_decode_diagnostics

Decode samples show blank-only outputs. Metric is consistent with samples.

## comparability_boundary

Fixture cannot compare model quality. It only validates diagnostic shape.

## fastest_falsification

Run two-sample overfit with blank bias initialized lower and LR reduced 5x.

## one_delta_retry

Change only decoder LR/warmup; keep data, seed, and metric fixed.

## stop_condition

Stop if blank_rate remains >= 0.95 after one-delta retry.

## next_route

debug

## claims_allowed

Failure can be classified as blank-collapse-shaped in fixture.

## claims_blocked

No claim about real root cause, model quality, or dataset quality.
