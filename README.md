# rctl — Research Control Layer

rctl helps a research task start with an explicit contract, finish with evidence-backed verification, and resume with an accurate reminder of its state.

**Status: v0.4.1 — project reminders and history reuse before experimental planning.**
The [M7 verification](docs/M7-VERIFICATION.md) records project-only and damaged-task
reminders, meaningful short-context fields, packaged planning guidance, and actual
Codex startup and automatic-compaction delivery.
The [v0.3.1 checks](docs/M6-VERIFICATION.md#v031-review-fixes) cover the review regressions.
The original [v0.3 verification](docs/M6-VERIFICATION.md) records 165 passing tests, installed-wheel checks, and fresh-session recovery of a long handoff.
The local package provides contracts, command/review verification, guarded closure,
handoffs, and Codex reminders. See the [v0.2 verification](docs/M5-VERIFICATION.md)
for initialization and skill-migration evidence, and the [v0.1 release record](docs/RELEASE-VERIFICATION.md)
for the original two-session host acceptance.
The [v0.2.1 checks](docs/M2-VERIFICATION.md#v021-review-follow-up) cover the diagnostic and publication fixes.

## Run the local CLI

Requires Python 3.11+ on macOS or Linux. Windows users can run inside WSL.

```sh
uv sync --locked
uv run rctl --help
uv run rctl init --vault note/main --codex
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
uv run ruff check src tests scripts
uv run scripts/check_docs.py
uv build
uv run scripts/smoke_package.py dist/rctl-0.4.1-py3-none-any.whl
```

The GitHub Actions workflow is configured to run tests, lint, the document check,
build, and wheel smoke on macOS and Linux with Python 3.11 and 3.13.
See [the workflow](.github/workflows/ci.yml).

The installed-package smoke uses a temporary project under `.work/`, an isolated environment, and offline dependency installation after `uv sync`. Schemas, templates, and the local task skill are included in the wheel; editable source execution reads their authoritative repository directories.

## Initialize a research project

Install the built wheel once with `uv tool install /path/to/rctl/dist/rctl-0.4.1-py3-none-any.whl`,
then run this inside an existing project root:

```sh
rctl init --vault note/main --codex
```

Omit `--vault` or `--codex` when not needed. The command creates missing `research/`
orientation files, `tasks/`, and `.agents/skills/research-task/`. `.rctl/project.json`
records the vault binding; it never selects an implicit current task. Existing files are
preserved and listed. Choose the vault at first init; changing a recorded binding requires
an explicit reviewed edit. Existing vaults are associated without edits. New vaults receive
note templates, ownership guidance, and local ignore rules. Init does not upgrade existing
skills/templates; use `doctor` and candidate export to review updates.

The vault holds reading notes, derivations, and interpretation linked to task and runner
evidence. Task contract/result/state and machine acceptance remain under `tasks/`.
`research-project-setup` is retired from the shared-skill repository; workspace and migration
guidance now ships in [research-task](skills/research-task/references/workspace.md).
No live project migration, Git setup, or host trust grant occurs during initialization.

## Project guidance before task selection

`rctl context` without a selected task reads `research/PROGRAM.md` (Goal and optional
Current guidance) and `research/ROUTES.md` (Reuse Rule). Task selection adds task
status and handoff; task errors retain project guidance and the original CLI error.
Keep current corrections with their evidence and scope in PROGRAM.md. Read related
route evidence before proposing experiments and explain the unanswered question,
reopen condition or mechanism difference, and decision a new result would change.

Short hook reminders reserve space for actual warnings, blockers and next steps,
using relative source references and no duplicate full handoff. These remain bounded
excerpts; follow sources when relevant details are truncated. Existing projects can
add Current guidance in place; records and the vault binding need no migration.

## Find work and review updates

```sh
rctl task list
rctl task list --phase active
rctl status tasks/my-analysis
rctl doctor --codex
rctl update export .work/rctl-update --codex
```

Listing reads immediate task directories under `tasks/`; it never selects a task or
executes checks. Damaged entries stay visible. Status separates lifecycle advice from
`handoff.next_action` and `handoff.blockers`. Put `## Next action` and `## Blockers` first
in new handoffs; existing plain/bulleted `Next action:` fields remain supported. Reminders
prioritize those fields even when they occur late in a long document.

Doctor inspects the project binding and task skill; `--codex` adds project-local host
configuration checks. Differences mean review needed, not proof that a customization is
wrong. Update export writes packaged candidates and scoped diffs to a new directory;
it never applies them. Merge host fragments without replacing unrelated settings.
Configuration inspection does not establish trust or actual reminder delivery.

## Codex reminders

```sh
uv run rctl integration codex export .work/codex-bundle
```

`init --codex` prepares missing project files; review `.rctl/codex/README.md`, select
`RCTL_TASK_PATH`, and trust the exact hooks through Codex `/hooks`. For an exported bundle,
use a new destination, review the generated files, then follow its README to select `RCTL_TASK_PATH` and launch Codex with the exported inline settings. The bundle includes a project-local `research-task` skill. Codex owns hook review and trust; exporting does not install configuration. Reminders read the selected task at session startup and prompt submission without running checks.

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
