# rctl — Research Control Layer

rctl helps a research task start with an explicit contract, finish with evidence-backed verification, and resume with an accurate reminder of its state.

**Status: v0.1.0 complete on 2026-09-06.** The local package provides contracts, command and review verification, guarded closure, handoffs, and Codex reminders. All 20 release acceptance cases have observed evidence, including two fresh host sessions completing a new bounded analysis. See the [release verification record](docs/RELEASE-VERIFICATION.md) for results and the tested compatibility boundary.

## Run the local CLI

```sh
uv sync --locked
uv run rctl --help
uv run rctl task new tasks/my-analysis --kind analysis --title "Inspect retained evidence"
# Replace the authoring placeholders in tasks/my-analysis/contract.md.
uv run rctl contract check tasks/my-analysis
uv run rctl begin tasks/my-analysis
uv run rctl context tasks/my-analysis
```

`contract check` checks structure. `begin` retains the exact agreement; neither certifies evidence or closes a task. Edit the contract and use `amend --reason TEXT` to retain a new revision. Save a handoff with `checkpoint TASK --file FILE`, then use `context TASK` in a fresh process. All paths resolve from the explicit project root, `RCTL_PROJECT_ROOT`, or the working directory, in that order.

After writing the result and preparing the declared evidence, run verification and close:

```sh
uv run rctl verify tasks/my-analysis --reviews tasks/my-analysis/reviews.json
uv run rctl close tasks/my-analysis
```

`verify` executes the frozen command criteria and records supplied review judgments. Omit `--reviews` when no review criteria are declared. A failure or missing review is saved in a report and prevents closure. Negative or inconclusive scientific findings may close when their required checks pass. Changed contracts require amendment; changed results, inputs, or execution logs require fresh verification. `reopen --reason TEXT` begins a new cycle; `cancel --reason TEXT` stops an active task without claiming closure.

For development and packaging:

```sh
uv run pytest
uv run ruff check src tests scripts/smoke_package.py
uv build
uv run scripts/smoke_package.py dist/rctl-0.1.0-py3-none-any.whl
```

The installed-package smoke uses a temporary project under `.work/`, an isolated environment, and offline dependency installation after `uv sync`. Schemas, templates, and the local task skill are included in the wheel; editable source execution reads their authoritative repository directories.

## Codex reminders

```sh
uv run rctl integration codex export .work/codex-bundle
```

Use a new destination, review the generated files, then follow its README to select `RCTL_TASK_PATH` and launch Codex with the exported inline settings. The bundle includes a project-local `research-task` skill. Codex owns hook review and trust; exporting does not install configuration. Reminders read the selected task at session startup and prompt submission without running checks.

Codex CLI 0.153.4 is tested with inline configuration and, in a [follow-up](docs/PROJECT-HOOKS-VERIFICATION.md), project-file loading with normal configuration and invocation-only hook-trust bypass. The isolated `--ignore-user-config` project-file attempt delivered no reminder; persisted installation without bypass remains unestablished. See [limitations](docs/READINESS.md#limitations).

## Start here

1. [PRD](docs/PRD.md): problem, scope, requirements, and release outcome.
2. [Domain language](CONTEXT.md): the meanings of contract, verification, closure, and handoff.
3. [Specification](docs/SPEC.md): records, lifecycle, storage, and verification behavior.
4. [CLI contract](docs/CLI.md): exact command and output boundaries.
5. [Host integration](docs/INTEGRATION.md): shared skill responsibilities and the first Codex adapter.
6. [Acceptance plan](docs/ACCEPTANCE.md) and [development plan](docs/DEVELOPMENT.md): what to build and how to establish that it works.
7. [Readiness record](docs/READINESS.md): milestone completion, preparation history, and limitations.

The [source register](docs/SOURCES.md) records the original design, existing skills, and the Pinyin-VSR pilot. [ADR-0001](docs/adr/0001-file-based-task-boundaries.md) explains the narrower initial architecture.

## Document authority

User instructions take precedence. Within this documentation baseline, the PRD owns product scope; SPEC owns behavior; CLI owns command syntax; JSON schemas own structural field constraints; ACCEPTANCE owns release checks. Other documents explain or instantiate those contracts. A contradiction is a documentation defect to fix before implementing the affected behavior.

The earlier [development proposal](research-control-layer-development-plan.md) is retained as historical design material. Its database, approval, client, command, and milestone requirements do not override this baseline. [DEVELOPMENT](docs/DEVELOPMENT.md#changes-from-the-original-proposal) makes the changes explicit.

## Minimal task arrangement

```text
research/README.md                # project orientation and ownership map
tasks/<task>/contract.md          # question, scope, acceptance rules
tasks/<task>/state.md             # optional human-readable handoff
tasks/<task>/result.md            # outcome and interpretation
tasks/<task>/evidence/            # small local evidence; large runs stay elsewhere
tasks/<task>/.rctl/record.json    # machine-owned acceptance and lifecycle record
```

Task records carry current work. Project research files carry durable scientific knowledge. Hooks read these records; a hook receipt is not a scientific result.

Templates are in [templates](templates/README.md). The [synthetic example](examples/retained-comparison/README.md) illustrates a correctly completed negative finding without importing private research data and is exercised by the installed-package smoke. The [integration verification](docs/M3-VERIFICATION.md) retains actual host delivery evidence.
