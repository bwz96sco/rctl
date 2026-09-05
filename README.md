# rctl — Research Control Layer

rctl helps a research task start with an explicit contract, finish with evidence-backed verification, and resume with an accurate reminder of its state.

**Status: M1 implemented, 0.1.0a1, on 2026-09-05.** The local Git repository, Python package, and executable are named `rctl`. Contract and readable-state commands are available; verification, closure, and host integration remain later milestones. This is an initial development increment, not the v0.1 release. See the [M1 verification record](docs/M1-VERIFICATION.md).

## Run the M1 increment

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

For development and packaging:

```sh
uv run pytest
uv run ruff check src tests scripts/smoke_package.py
uv build
uv run scripts/smoke_package.py dist/rctl-0.1.0a1-py3-none-any.whl
```

The installed-package smoke uses a temporary project under `.work/`, an isolated environment, and offline dependency installation after `uv sync`. Schemas and templates are included in the wheel; editable source execution reads their authoritative repository directories.

## Start here

1. [PRD](docs/PRD.md): problem, scope, requirements, and release outcome.
2. [Domain language](CONTEXT.md): the meanings of contract, verification, closure, and handoff.
3. [Specification](docs/SPEC.md): records, lifecycle, storage, and verification behavior.
4. [CLI contract](docs/CLI.md): exact command and output boundaries.
5. [Host integration](docs/INTEGRATION.md): shared skill responsibilities and the first Codex adapter.
6. [Acceptance plan](docs/ACCEPTANCE.md) and [development plan](docs/DEVELOPMENT.md): what to build and how to establish that it works.
7. [Readiness record](docs/READINESS.md): preparation checks, outstanding implementation gates, and limitations.

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

Templates are in [templates](templates/README.md). The [synthetic example](examples/retained-comparison/README.md) illustrates a correctly completed negative finding without importing private research data. Examples involving verification, closure, or integration remain specifications for M2–M4.
