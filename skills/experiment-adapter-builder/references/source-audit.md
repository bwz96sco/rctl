# Source Audit

Use this before generating a project-local experiment workflow skill. Inspect only enough to extract stable project invariants.

## Project Files To Check

- `AGENTS.md`, README, experiment docs, setup docs, and existing local skills
- launch scripts, training scripts, analysis scripts, sweep configs, queue files, and manifest writers
- result directories, run logs, checkpoints, tracker exports, and paper-facing analysis outputs
- environment files such as `pyproject.toml`, `requirements.txt`, `environment.yml`, `uv.lock`, shell scripts, or Docker files
- remote execution notes, SSH scripts, cluster configs, cloud provider notes, and cleanup scripts
- mempal drawer IDs, previous adapter notes, validator output, and user-specified instructions when they are used as evidence

## Facts To Extract

- command authority: which scripts or docs own launch commands
- working directory and environment manager
- runner selection: local, SSH, queue, managed GPU, serverless, notebook, or manual
- canonical output root and naming conventions
- raw logs, structured result files, tracker names, and archival policy
- baseline reuse rules and invalidation triggers
- preflight checks for data, checkpoints, environment, GPU, memory, and baseline files
- queue, concurrency, retry, and stale-job cleanup rules
- monitoring sources: logs, JSON/CSV outputs, W&B, screen/tmux, scheduler, cloud logs
- training health gates and stop/continue criteria
- profiling routes and allowed instrumentation style
- result validation rules before claims feed writing or review
- cleanup rules for worktrees, branches, caches, launch logs, remote instances, and temporary artifacts

## Stop Conditions

Stop and write unknowns instead of guessing when command authority, output root, baseline source, tracker name, remote host, or cleanup rule cannot be verified from project files.

## Evidence Discipline

Every generated adapter rule should cite a local source path, command, observed convention, mempal drawer ID, remote path evidence, validator output, or user instruction in `references/adapter-sources.md`. If a rule comes from user instruction, label it `user-specified`.

For updates, preserve prior adapter facts unless a newer cited source contradicts them. Record added, modified, and deprecated facts before rerunning the validator.
