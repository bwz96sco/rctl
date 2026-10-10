# rctl — Research Control Layer

rctl helps a research task start with an explicit contract, finish with evidence-backed verification, and resume with an accurate reminder of its state.

**Status: v0.6.4 prepared for release; push, CI and installation pending.**

The previous installed release is recorded in the [v0.6.3 deployment record](docs/V0.6.3-DEPLOYMENT.md).
The local package provides contracts, command/review verification, guarded closure,
handoffs, governing-question alignment, and Codex and Claude Code reminders. The
[simplification verification](docs/SIMPLIFICATION-VERIFICATION.md) covers the routed
task skill, immutable task snapshots, and one concise reminder layout. Historical
milestone and host evidence is in the [release-evidence index](docs/RELEASE-EVIDENCE.md).
Version 0.6.0 adds **goal-contribution and goal-impact review**:
when PROGRAM has a completed Goal, new contracts/amendments must declare their
goal contribution and a required structured goal-impact review. Status and
reminders show the reviewed investment decision separately from local pass.
See [behavior](docs/SPEC.md#goal-contribution-and-review-v060)
and [source development](docs/DEVELOPMENT.md#goal-review-controller-increment-10-october-2026).
The installed CLI includes this enforcement. Retained older agreements remain
readable; new work and amendments follow the current entry rules.
Version 0.6.1 packages the [guidance consolidation](docs/DEVELOPMENT.md#guidance-consolidation-10-october-2026):
shorter contract/result templates and research-task skill guidance, with no
schema, controller or lifecycle change.

Version 0.6.2 packages the
[Codex first-use repair](docs/DEVELOPMENT.md#codex-first-use-repair-10-october-2026):
`init` prepares project hooks and `doctor` inspects them by default, with an explicit
`--no-codex` opt-out. It also adds
[Claude Code host support](docs/DEVELOPMENT.md#claude-code-host-support-10-october-2026): `init` prepares
`.claude/settings.json` hooks and a `.claude/skills/research-task/` skill copy, and
`doctor` inspects them, with an explicit `--no-claude` opt-out.
Version 0.6.3 gives selected-task
[prompt reminders](docs/DEVELOPMENT.md#per-prompt-task-reminder-10-october-2026)
one whole sentence per decision-relevant field instead of fragments of every field.
Version 0.6.4 adds [automatic reminder selection](docs/DEVELOPMENT.md#automatic-reminder-task-selection-10-october-2026):
without `RCTL_TASK_PATH`, reminders use the project's only active task.

The repository also manages the [research workflow skills](docs/RESEARCH-SKILLS.md).
Their [source migration](docs/RESEARCH-SKILLS-MIGRATION.md) keeps auxiliary tools
separate and preserves task-only project initialization.

## Run the local CLI

Requires Python 3.11+ on macOS or Linux. Windows users can run inside WSL.

```sh
uv sync --locked
uv run rctl --help
uv run rctl init --vault note/main
uv run rctl doctor
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
uv run scripts/smoke_package.py dist/rctl-0.6.4-py3-none-any.whl
```

The GitHub Actions workflow is configured to run tests, lint, the document check,
build, and wheel smoke on macOS and Linux with Python 3.11 and 3.13.
See [the workflow](.github/workflows/ci.yml).

The installed-package smoke uses a temporary project under `.work/`, an isolated environment, and offline dependency installation after `uv sync`. Schemas, templates, and the local task skill are included in the wheel; editable source execution reads their authoritative repository directories.

## Initialize a research project

Install the built wheel once with `uv tool install /path/to/rctl/dist/rctl-0.6.4-py3-none-any.whl`,
then run this inside an existing project root:

```sh
rctl init --vault note/main
```

Omit `--vault` when not needed. Codex and Claude Code files are prepared by default;
use `--no-codex` or `--no-claude` to skip a host. The previous `--codex` form remains
supported. The command creates missing `research/`
orientation files, `tasks/`, `.agents/skills/research-task/` and its Claude Code copy
under `.claude/skills/research-task/`. `.rctl/project.json`
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

The source scaffold includes a problem/method overview and comparison guidance.
PROBLEM_METHODS owns open questions and candidate methods; ROUTES records scoped
investment decisions; BASELINES identifies fixed and enhanced control versions.
Task templates prompt the actual
information conditions and endpoint without adding scientific schema fields.
Installed CLI assets change only with a package upgrade; source edits and skill
symlinks do not upgrade an existing wheel installation.

Upgrading changes the version recorded by verification. Under the current policy,
older reports show `stale` even when their materials are unchanged; the explanation
identifies the version mismatch. Historical closures remain intact. An active task
needs verification by the installed version before it can close.

## Project guidance before task selection

`rctl context` without a selected task reads `research/PROGRAM.md` (Goal and optional
Current guidance) and `research/ROUTES.md` (Reuse Rule). Task selection, explicit or
automatic for the only active task, adds task status and handoff; task errors retain project guidance and the original CLI error.
Keep current corrections with their evidence and scope in PROGRAM.md. Read related
route evidence before proposing experiments and explain the unanswered question,
reopen condition or mechanism difference, and decision a new result would change.

Both hook budgets use one concise layout, reserving space for actual warnings,
blockers and next steps without appended contract/handoff prose. Source alias C
identifies the accepted contract in the record, or the working draft. These remain bounded
excerpts; follow sources when relevant details are truncated. Existing projects can
add Current guidance in place; records and the vault binding need no migration.

## Find work and review updates

```sh
rctl task list
rctl task list --phase active
rctl status tasks/my-analysis
rctl doctor
rctl update export .work/rctl-update --codex
```

Listing reads immediate task directories under `tasks/`; it never selects a task or
executes checks. Damaged entries stay visible. Status separates lifecycle advice from
`handoff.next_action` and `handoff.blockers`. Put `## Next action` and `## Blockers` first
in new handoffs; existing plain/bulleted `Next action:` fields remain supported. Reminders
prioritize those fields even when they occur late in a long document.

Doctor inspects the project binding, task skill and project-local Codex configuration
by default; `--no-codex` limits it to core assets. Differences mean review needed,
not proof that a customization is
wrong. Update export writes packaged candidates and scoped diffs to a new directory;
it never applies them. Merge host fragments without replacing unrelated settings.
Configuration inspection does not establish trust or actual reminder delivery.

## Codex reminders

```sh
uv run rctl integration codex export .work/codex-bundle
```

`init` prepares missing project files; follow the
[host first-use procedure](skills/research-task/references/workspace.md#host-first-use),
review `.rctl/codex/README.md`, and trust the exact hooks through Codex `/hooks`.
Reminders use the only active task automatically; `RCTL_TASK_PATH` overrides that. For an exported bundle,
use a new destination, review the generated files, then follow its README to select `RCTL_TASK_PATH` and launch Codex with the exported inline settings. The bundle includes a project-local `research-task` skill. Codex owns hook review and trust; exporting does not install configuration. Reminders read the selected task at session startup and prompt submission without running checks.

After trust, start a fresh project session and submit a prompt to confirm both
event reminders. Configuration creation and a passing doctor inspection leave host
trust and reminder delivery uninspected; they do not complete host acceptance.

Codex CLI 0.153.4 is tested with inline configuration and, in a [follow-up](docs/PROJECT-HOOKS-VERIFICATION.md), project-file loading with normal configuration and invocation-only hook-trust bypass. The isolated `--ignore-user-config` project-file attempt delivered no reminder; persisted installation without bypass remains unestablished. See [limitations](docs/READINESS.md#limitations).

## Claude Code reminders

`init` writes the two rctl handlers to `.claude/settings.json` and the task skill to
`.claude/skills/research-task/`; review `.rctl/claude/README.md`. Claude Code runs
project settings hooks after the folder's workspace trust dialog is accepted. Reminders use the only active task automatically (`RCTL_TASK_PATH=tasks/your-task claude`
overrides that); confirm both event reminders in a fresh session. An existing
`.claude/settings.json` is preserved; merge the handlers from
`rctl update export DIRECTORY --claude`. One non-interactive Claude Code 2.1.296
session has been observed receiving both reminders; the interactive trust path has
not. See [limitations](docs/READINESS.md#limitations).

## Start here

1. [PRD](docs/PRD.md): problem, scope, requirements, and release outcome.
2. [Domain language](CONTEXT.md): the meanings of contract, verification, closure, and handoff.
3. [Specification](docs/SPEC.md): records, lifecycle, storage, and verification behavior.
4. [CLI contract](docs/CLI.md): exact command and output boundaries.
5. [Host integration](docs/INTEGRATION.md): shared skill responsibilities and the first Codex adapter.
6. [Acceptance plan](docs/ACCEPTANCE.md) and [development plan](docs/DEVELOPMENT.md): what to build and how to establish that it works.
7. [Readiness record](docs/READINESS.md): milestone completion, preparation history, and limitations.

The [simplification review and implementation plan](docs/SIMPLIFICATION-REVIEW.md)
prioritizes the packaged skill and concise reminders for GPT-6-Astra. Its first
increment is locally validated; installation and compatibility decisions remain deferred.

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
