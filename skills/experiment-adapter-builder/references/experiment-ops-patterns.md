# Experiment Operations Patterns

Use these patterns when the target project has batch runs, remote GPUs, long training, unstable metrics, or profiling needs.

## Queue And Batch Runs

- Prefer an explicit manifest for multi-seed, multi-config, teacher-student, or staged runs.
- A job row should have a stable id, command args, expected outputs, prerequisites, retry policy, and status location.
- Queue state should distinguish `pending`, `running`, `completed`, `failed_oom`, `failed_other`, `blocked`, and `stale`.
- Start a new wave only after prior processes exited, stale sessions are cleaned, memory settled, and next-wave prerequisites exist.
- OOM retry should have max attempts, delay, and a rule for when to mark blocked instead of looping.

## Monitoring

- Monitor the backend actually used: local process, tmux/screen, SSH queue, scheduler, managed GPU, serverless logs, or manual run.
- Collect raw numbers before interpretation: recent metrics, output files, baseline values, and status.
- Prefer configured trackers such as W&B when project files say they are authoritative; fall back to logs or structured result files.
- Report whether the run is still running, completed, failed, blocked, or inconclusive.
- Include cost or cleanup risk for long-running remote or managed GPU jobs when the project uses them.

## Campaign Ordering

- Sanity-first: run the smallest/fastest experiment before committing to the full suite.
- On sanity failure: classify error (config, code, data, environment), fix, retry (max 3 attempts), then escalate.
- Track GPU-hours against the plan budget. Warn when approaching the limit. Flag any run exceeding 2x estimated time.

## Training Health

- Health checks judge whether a run remains useful, not just whether the process exists.
- Check NaN/Inf, divergence, sudden spikes, plateau, failed evals, metric regression, learning-rate schedule, and gradient norm when available.
- Use decisions `CONTINUE`, `WAIT`, or `STOP`.
- Stop only on sustained or hard evidence. Preserve metrics, logs, tracker URLs, and stop reason.
- Adaptive check interval: start at short intervals (e.g. 10 min), widen (20→30→60 min) when consistently healthy, reset to short after any anomaly.

## Profiling

- Profile only when a bottleneck question exists or the project adapter says profiling is part of normal workflow.
- Choose tools based on target: CPU, memory, GPU, interconnect, framework profiler, or code instrumentation.
- Prefer wrappers or standalone profiling runners over inline edits. If inline instrumentation is necessary, mark and later remove it.
- Save profiling artifacts under a project-approved profiling output root.
- Record an instrumentation changelog listing changed files and cleanup status.

## Evidence Gate

A run becomes paper-valid evidence only after expected outputs exist, metrics parse cleanly, baseline comparability is checked, and known failure classes are either absent or explicitly bounded.
