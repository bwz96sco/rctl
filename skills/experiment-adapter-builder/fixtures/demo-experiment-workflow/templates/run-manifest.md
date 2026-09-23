# Run Manifest

## identity

campaign_id: demo-fixture
run_id: demo-fixture-001
route: demo-local
objective: validate adapter fixture contract
created_at: fixture
owner: fixture

## command

working_directory: demo project root
entrypoint: train.py
full_command: uv run python train.py --config configs/tiny.yaml
runner: local
host_or_backend: local
queue_or_session_id: not_applicable

## code_state

project_git_state: fixture
code_repo_state: fixture
worktree_state: fixture
changed_files_relevant_to_run: none
experiment_code_review_path: not_required

## environment

environment_manager: uv
python: fixture
key_packages: fixture
accelerator_available: false
accelerator: cpu
runtime_notes: fixture only

## data_contract

data_root: data/
train_split: data/demo_train.jsonl
validation_split: data/demo_valid.jsonl
test_split: not_applicable
reference_or_label_files: data/demo_valid.jsonl
label_or_token_policy: fixture labels
sample_counts: fixture

## model_contract

architecture: demo model
model_impl: train.py
checkpoint_path: not_applicable
checkpoint_lineage: fixture initialization
checkpoint_load_audit: not_required
trainable_scope: demo parameters

## training_contract

seed_policy: seed=1
epochs_or_steps: 1 step
batching: fixture batch
optimizer: fixture optimizer
schedule: fixture schedule
augmentation_or_regularization: none

## eval_contract

primary_metric: demo_accuracy
metric_parser: metrics.json reader
decode_or_inference_policy: fixture inference
baseline_run: runs/demo-baseline/
comparability_boundary: fixture-only

## expected_outputs

output_root: runs/demo-fixture/
logs: runs/demo-fixture/train.log
metrics: runs/demo-fixture/metrics.json
checkpoints: not_required
predictions_or_diagnostics: runs/demo-fixture/predictions.jsonl

## launch_guard

preflight_path: runs/demo-fixture/preflight.md
required_prior_gate: dry-run
approval: fixture
verdict: pass

## result_summary

status: fixture
primary_metric_value: fixture
secondary_metrics: fixture
best_checkpoint: not_applicable
known_limitations: no real experiment evidence
next_action: validate fixture
