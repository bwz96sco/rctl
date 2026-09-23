# Run Manifest

## identity

campaign_id:
run_id:
route:
objective:
created_at:
owner:

## command

working_directory:
entrypoint:
full_command:
runner:
host_or_backend:
queue_or_session_id:

## code_state

project_git_state:
code_repo_state:
worktree_state:
changed_files_relevant_to_run:
experiment_code_review_path:

## environment

environment_manager:
python:
key_packages:
accelerator_available:
accelerator:
runtime_notes:

## data_contract

data_root:
train_split:
validation_split:
test_split:
reference_or_label_files:
label_or_token_policy:
sample_counts:

## model_contract

architecture:
model_impl:
checkpoint_path:
checkpoint_lineage:
checkpoint_load_audit:
trainable_scope:

## training_contract

seed_policy:
epochs_or_steps:
batching:
optimizer:
schedule:
augmentation_or_regularization:

## eval_contract

primary_metric:
metric_parser:
decode_or_inference_policy:
baseline_run:
comparability_boundary:

## expected_outputs

output_root:
logs:
metrics:
checkpoints:
predictions_or_diagnostics:

## launch_guard

preflight_path:
required_prior_gate:
approval:
verdict:

## result_summary

status:
primary_metric_value:
secondary_metrics:
best_checkpoint:
known_limitations:
next_action:
