# Queue And Concurrency

## queue_authority

## max_parallel

## grid_spec

Declarative parameter grid → expanded job list. Define a `grid:` block (parameter names × value lists) and a `template:` block (command pattern with placeholders). Expansion produces one job row per Cartesian product element.

## job_state_machine

pending:

running:

completed:

failed_oom:

failed_other:

blocked:

stale:

Completion detection: verify expected output file exists before marking completed; do not trust process/screen state alone.

## phase_chaining

Declare the actual inputs/prerequisites of dependent jobs. Use a whole-phase barrier
only when the project requires all prior jobs to complete before the next phase.

## retry_policy

## stale_job_cleanup

## wave_transition_gate

## crash_recovery

On scheduler restart: read persistent state file, check which jobs are still running, re-evaluate state for each row, continue pending. Scheduler must be idempotent — restarting mid-campaign should not duplicate completed work.

## known_failure_modes

- SSH/connection drop: scheduler survives if state is on disk; reconnect and re-check.
- GPU reservation by another user: wait and retry, do not preempt.
- Disk full: mark stuck, alert, do not retry until space is freed.

## shared_state_hazards

## unknowns
