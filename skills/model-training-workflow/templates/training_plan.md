# Training Plan

## objective

## model_family

## dataset_and_split

## label_or_tokenization

## baseline

## metric_contract

## compute_budget

## source_skill_map

## adapter_discovery

Resolve `.agents/skills/*-experiment-workflow/` from the repo root of the code being trained before writing launch commands. If multiple adapters match, choose by project/name match and record why; if ambiguous, ask the user. Record selected adapter path or why no adapter applies.

## project_adapter_decision

Use selected adapter command authority when present. If no adapter exists and commands are repeated, remote, fragile, or expensive, route to `experiment-adapter-builder`; otherwise record one-off commands here.

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

## sanity_gates
Classify each gate as launch_guard, route_validation, or main_run_health.
State whether a user-approved full-run contract exists.

## main_run_scope

## stop_go_rules
Full-run approved + launch guards pass -> launch full training.
Only concrete launch blockers stop approved launch.

## claims_targeted

## claims_not_targeted
