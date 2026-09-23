# Result Validation

## expected_outputs

## metric_parsing

## experiment_code_review

Use `templates/experiment-code-review.md` when experiment code changes before expensive runs. Save the review as `EXPERIMENT_CODE_REVIEW.md` or project-local equivalent. Review must cover metric correctness, ground-truth use, data split safety, baseline comparability, and output path integrity.

## baseline_comparison

## failure_classes

missing_output:

parse_failure:

non_comparable:

diverged:

incomplete:

## paper_valid_evidence_gate

## eval_integrity

Evaluation must use dataset ground truth, never another model's output. If a teacher/reference model is used, its predictions are inputs, not evaluation targets.

## claim_boundary

## handoff_to_research_experiment

## unknowns
