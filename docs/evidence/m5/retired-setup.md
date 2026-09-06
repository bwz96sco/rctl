---
name: research-project-setup
description: Inspect, design, or change research workspaces and their minimal scientific control plane with explicit Git, data, privacy, and migration boundaries. Use for new-project setup, existing-project retrofit, workspace reorganization, or standard vault initialization.
---

# Research Project Setup

Separate code, manuscripts, notes, data, and generated evidence reproducibly — with explicit authority for every change.

## Workflow

1. **Bound the operation.** What is requested, which paths may change, and what authority exists for repository init, moves, deletion, or commits.
2. **Inspect first.** Filesystem state plus root and nested Git boundaries. For a named small inventory, read it with this SKILL.md in one initial read-only call; treat supplied listings as declarations, not verified state.
3. **Choose a setup mode.** For a new project, design boundaries and propose the control files before copying them. For a retrofit, inspect existing orientation, evidence, and control files; preserve supported content, merge deliberately, and add only what is missing. Never overwrite existing files or promote remembered or ambiguous metrics into accepted baselines.
4. **Design boundaries.** Code, paper, notes, data, privacy, and Git/history separation. For advice, return one compact target tree plus exactly six single-sentence migration steps unless another count is requested. State only decision-changing assumptions.
5. **Execute only what was authorized.** Change only requested paths; never initialize, move, delete, or commit a repository without user authority. On an explicit scientific-control setup request, copy the five templates from `assets/research-control/` to `research/`, replace placeholders only with verified facts, and keep `research/README.md` static rather than copying live task state into it. Copy the vault scaffold from `assets/obsidian-vault/` only on an explicit vault setup request.
6. **Verify actual state.** Reinspect each affected repository: paths, boundaries, ignored and tracked state, outputs. Confirm that the research index links resolve and routes current work to the project's task system, then report mismatches and blockers.

Complete when the requested diagnosis or change is done or blocked, boundaries and authority are explicit, verification matches reality, and proposed operations remain distinct from performed ones.

## Boundaries

- Keep code, paper, and notes independent when collaborators, privacy, or release cadence differ; a meta repository tracks only the project map, never nested repo contents.
- Parallel checkouts via `git worktree add` under `code/worktrees/`; never copy repositories manually.
- Large or sensitive data, PDFs, logs, checkpoints, and run outputs stay outside normal Git or ignored.
- Load `references/graphify.md` only for explicit Graphify setup.

## Scientific Control Files

- `research/README.md` is the static onboarding entry point: reading order, authority map, and how to discover current work in the project's task system; it never owns live status.
- `research/PROGRAM.md` owns slow-changing goals, success definitions, evaluation surfaces, constraints, and open questions.
- `research/INVENTORY.md` owns verified availability of datasets, checkpoints, code, and infrastructure; mark unknown state `audit_required` rather than guessing.
- `research/BASELINES.md` owns named evaluation surfaces and baseline evidence contracts, including training data, initialization, metric contract, evidence, and status.
- `research/ROUTES.md` owns mechanism-level directions that are refuted, parked, or not executed: aliases, what closed or stopped them, and the reopen condition. Record a treatment that never ran as `not_executed`, never as `refuted`; use `parked` when an external or unresolved condition could change. One entry per direction, never per run.
- Active work and task-local outcomes stay in the project's task system. Long-form notes and large artifacts stay in their designated repositories or ignored storage.
