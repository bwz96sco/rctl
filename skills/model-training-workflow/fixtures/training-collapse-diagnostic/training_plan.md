# Training Plan

## objective

Fixture objective: diagnose CTC blank collapse and force bounded next route instead of retrying blindly.

## model_family

Multimodal encoder plus CTC decoder placeholder. Source reference: Whisper-style audio constraints and generic ML training debug recipes.

## dataset_and_split

Dataset: mock audio/video token pairs. Split: 20 train clips, 5 validation clips. Fixture only.

## label_or_tokenization

Check transcript tokens, blank ID, label length <= input frame length, and decode round trip.

## baseline

Baseline mock run has blank_rate 0.41 and val_cer 0.58. Failed run has blank_rate 0.98 and val_cer 1.00.

## metric_contract

Primary metric: validation CER. Diagnostic metric: blank_rate. Collapse condition: blank_rate >= 0.95 for two evals and CER not improving.

## adapter_discovery

No project-local experiment adapter applies to this fixture. Use embedded fixture paths and one-off commands.

## training_lineage_contract

Architecture implementation: fixture multimodal encoder plus CTC decoder. Checkpoint lineage: fixture init -> step200 failed checkpoint. Checkpoint load audit: mocked by preflight report. Dataset/split: 20 train clips, 5 validation clips. Refs/label policy: transcript tokens with blank ID audit. Tokenizer/units: CTC label units. Decode policy: greedy CTC fixture decode. Metric parser: fixture CER and blank-rate JSON reader. Runner/env: local fixture route, Python 3.12. Comparability boundary: fixture-only collapse diagnosis, no ASR/VSR quality claim.

## compute_budget

Fixture budget only. Real debug pass limited to 20 minutes and no scale-up without one-delta retry evidence.

## source_skill_map

See `source_skill_map.md`.

## sanity_gates

Required gates: label/frame length check, one-batch forward, two-sample overfit, decode sanity, blank-rate monitor.

## main_run_scope

Main run parked until collapse root cause has one-delta retry.

## stop_go_rules

Stop on blank_rate >= 0.95, NaN loss, invalid label lengths, or missing prediction samples.

## project_adapter_decision

Use one-off fixture. Route to `experiment-adapter-builder` for repeated queue/GPU debug jobs.

## claims_targeted

Classify failure layer and next debug delta.

## claims_not_targeted

No ASR/VSR quality claim.
