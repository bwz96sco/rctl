# Queue And Concurrency

## queue_authority

Fixture has no external queue; local shell is authority.

## max_parallel

`1`

## grid_spec

Single fixture row: `variant=demo`, `seed=1`.

## job_state_machine

pending: manifest exists but command not launched.

running: process is active and log is growing.

completed: expected metrics file exists.

failed_oom: not expected for CPU fixture.

failed_other: process exits nonzero or expected output missing.

blocked: preflight blocker exists.

stale: process state cannot be verified.

Completion detection: verify `runs/demo-fixture/metrics.json` exists before marking completed.

## phase_chaining

No chained phases in fixture.

## retry_policy

Retry once only after fixing data, config, or environment cause.

## stale_job_cleanup

Delete stale fixture output root only after preserving logs.

## wave_transition_gate

No wave transition in fixture.

## crash_recovery

Re-read manifest and logs, then rerun dry-run before retry.

## known_failure_modes

Missing fixture data, syntax error in config, or unwritable `runs/`.

## shared_state_hazards

Shared output root can be overwritten by parallel fixture tests.

## unknowns

None for fixture.
