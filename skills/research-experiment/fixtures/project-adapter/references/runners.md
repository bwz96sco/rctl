# Runners

## command_authority

Fixture command authority: `uv run python train.py --config configs/tiny.yaml`.

## working_directory

Run from the fictional demo project root.

## environment_manager

Use `uv` with the project `pyproject.toml`.

## runner_selection

local: default fixture route.

ssh: not used in fixture.

queue: not used in fixture.

managed_gpu: not used in fixture.

serverless: not used in fixture.

manual: only for validating generated documentation.

## canonical_output_root

`runs/demo-fixture/`

## structured_result_paths

Metrics: `runs/demo-fixture/metrics.json`.

## raw_log_paths

Logs: `runs/demo-fixture/train.log`.

## archive_policy

Keep fixture artifacts under `runs/demo-fixture/` until validation ends.

## cleanup_rules

Remove temporary fixture outputs after tests when needed.

## unknowns

None for fixture.
