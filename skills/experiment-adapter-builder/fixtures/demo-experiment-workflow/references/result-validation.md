# Result Validation

## expected_outputs

Expected files: `metrics.json`, `train.log`, and optional `predictions.jsonl`.

## metric_parsing

Parse `demo_loss` and `demo_accuracy` from `metrics.json`.

## experiment_code_review

Use `templates/experiment-code-review.md` when fixture training, metric parser, or validation code changes. Save the review as `EXPERIMENT_CODE_REVIEW.md`.

## baseline_comparison

Compare against `runs/demo-baseline/metrics.json` only when dataset and seed match.

## failure_classes

missing_output: expected file absent.

parse_failure: metrics JSON cannot be read.

non_comparable: baseline contract differs.

diverged: loss is NaN or above fixture threshold.

incomplete: process exited before writing metrics.

## paper_valid_evidence_gate

Fixture never produces paper-valid evidence.

## eval_integrity

Evaluation must use fixture labels, not generated predictions as targets.

## claim_boundary

Allowed claim: validator fixture shape is complete.

## handoff_to_research_experiment

Do not hand off fixture metrics as research evidence.

## unknowns

None for fixture.
