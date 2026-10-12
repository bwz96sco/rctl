# Experiment Operations Patterns

Use only patterns needed by the project's actual runner. Verify local commands
and constraints before adding a rule to an adapter.

## Queue and batch work

Use the existing scheduler and persistence convention. Record prerequisites,
resource/concurrency limits, completion evidence and retry policy where relevant.
Dependencies follow the inputs a job needs; whole-phase barriers apply only when
the project requires them. Recheck actual processes and outputs after interruption
before resuming; do not duplicate completed work.

## Monitoring and launch checks

Inspect the backend actually used and its authoritative logs, metrics and outputs.
Distinguish submitted, running, completed, failed and uninspected work. Workload
progress and valid outputs need evidence beyond launcher success.

Choose checks and monitoring cadence for concrete failure risks and current cost.
Use the agreement's time/call/compute limits. Tiny/capped validation is not a new
full-run prerequisite unless the current agreement makes it one. Retries need a
specific observed failure, expected change and remaining allowance.

## Profiling

Profile a specific bottleneck using project-supported tools. Keep instrumentation
and its effect on the measured workload explicit. Preserve the result and relevant
cleanup state in existing run evidence; report format follows the question.

## Evidence handoff

Inspect expected outputs and metric definitions, actual comparison conditions,
failures and incomplete coverage before a scientific claim. Operational evidence
feeds the task's result and criteria; it does not supply a competing acceptance state.
