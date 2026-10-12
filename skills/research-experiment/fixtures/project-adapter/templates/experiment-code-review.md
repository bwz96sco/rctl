# Experiment Code Review

## review_scope

Fixture command, metric parser, and output paths.

## changed_files

None for baseline fixture.

## command_or_entrypoints

`uv run python train.py --config configs/tiny.yaml`

## metric_correctness

Fixture metric parser reads labels from fixture validation data.

## ground_truth_integrity

Fixture labels are treated as ground truth.

## data_split_safety

Train and validation fixture paths are separate.

## baseline_comparability

Baseline must use same fixture split and seed.

## output_path_integrity

All outputs stay under `runs/demo-fixture/`.

## failure_modes

Missing output, parse failure, or non-comparable baseline.

## verdict

pass

## required_fixes

None.

## reviewer_notes

Fixture review only.
