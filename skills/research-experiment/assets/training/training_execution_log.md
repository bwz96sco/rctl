# Training Execution Log

Optional when the runner already owns adequate records. Link its manifest and
outputs from the handoff instead of creating another log. Include relevant fields.

## run_id

## run_manifest

Link the project-owned manifest, or record needed command/config/code/environment
and lineage facts here when no such record exists.

## command

## runner_route

## git_or_code_state

## environment_snapshot

## data_and_checkpoint_paths

## changed_files_relevant_to_run

State consequential changes relative to the relevant comparison or reviewed run.

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

Link checks of consequential code changes or a review required by the agreement;
record the failure each check addresses. A separate review artifact is optional.

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
