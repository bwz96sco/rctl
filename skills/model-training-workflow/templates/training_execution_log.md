# Training Execution Log

## run_id

## run_manifest

Exactly one: `manifest_path: <path>` when a project adapter owns the manifest, OR embedded manifest fields when none exists. Never both.

## command

## runner_route

## git_or_code_state

## environment_snapshot

## data_and_checkpoint_paths

## changed_files_relevant_to_run

Changed means a diff of training, wrapper, metric parser, decode, or eval code against the `code_state` recorded in the comparison baseline run's manifest, or against the last reviewed run when no baseline exists.

## training_lineage_contract

- architecture_implementation:
- checkpoint_lineage:
- checkpoint_load_audit:
- dataset_split:
- refs_or_label_policy:
- tokenizer_or_units:
- decode_or_inference_policy:
- metric_parser:
- runner_and_environment:
- comparability_boundary:

## experiment_code_review

Required before expensive runs when training scripts, wrappers, metric parser, decode, or eval code changed. Record review path/verdict, or `not_required: <reason>` only when relevant code is unchanged versus `changed_files_relevant_to_run`.

## preflight_verdict

## health_gate_verdict

## logs

## metrics

## checkpoints

## predictions_or_samples

## raw_artifact_paths

## status

## failure_mode

## next_action
