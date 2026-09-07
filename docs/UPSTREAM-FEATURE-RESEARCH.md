# Features worth learning from Trellis and Comet Native

Researched 2026-09-06. This is a feature comparison and recommendation, not a new
implementation plan or an expansion of the [PRD](PRD.md).

Follow-up: the first three recommendations were implemented in v0.3; see the
[M6 verification](M6-VERIFICATION.md). The comparison below retains its v0.2.1 baseline.

The strongest next increment is task discovery, a more useful continuation summary,
and inspection of installed project assets. These address everyday friction without
changing rctl's contract, verification, or closure model. Curated context and readable
review material are useful follow-ups. A complete orchestration runtime is not needed
for these improvements.

## Sources and scope

The comparison uses fresh upstream source checkouts and first-party material retrieved
through smart-search. The older local Trellis checkout was not used as the current
feature baseline.

| Project | Inspected revision | Scope |
|---|---|---|
| [Trellis](https://github.com/mindfold-ai/Trellis) | `88f4834449da9b4f607ec05e322408a0aa66f2ce` (`v0.6.16`) | Task tooling, context injection, project updates |
| [Comet](https://github.com/rpamis/comet) | `c1118e19d1fbce87706e4265ece17f50db21377e` (`0.4.0-rc.5`) | Native workflow, status, recovery, verification artifacts |
| rctl | `87e3af5943b65be2df6017a29ea5c4c1f6571fff` (`0.2.1`) | CLI, context, initialization, integration, schemas, requirements |

“Comet Native” is interpreted here as the Native workflow in `rpamis/comet`, consistent
with the research-control discussion. The separate `zeronsh/comet-native` application
is not the comparison target; the user was offered a clarification of this assumption.

The upstream capabilities below are supported by source inspection. Their presence
does not establish comparative reliability, token savings, or scientific validity.

## Recommended capabilities

### 1. Discover tasks without choosing one implicitly

Trellis provides task listing, status filtering, JSON output, and archive listing
([task implementation](https://github.com/mindfold-ai/Trellis/blob/88f4834449da9b4f607ec05e322408a0aa66f2ce/packages/cli/src/templates/trellis/scripts/task.py)).
Comet Native also discovers changes across registered workspaces
([discovery implementation](https://github.com/rpamis/comet/blob/c1118e19d1fbce87706e4265ece17f50db21377e/domains/comet-native/native-status-discovery.ts)).

rctl's [CLI](../src/rctl/cli.py) has `task new` and per-task `status`, but no list command.
Its [workspace guidance](../skills/research-task/references/workspace.md) explicitly
requires directory inspection for discovery. With multiple active and deferred tasks,
operators must maintain a separate navigation page or already know the path.

**Recommendation: next increment.** Add a read-only task list showing path, title,
phase, and verification applicability, with a phase filter and JSON output. Start with
the conventional `tasks/` directory and document its discovery boundary; existing
explicit task addressing must remain valid elsewhere. Reuse task records for the view.
Do not infer selection from recency or create another status ledger. A malformed task
should remain visible with its diagnosis instead of disappearing from the list.

### 2. Present the actual continuation step prominently

Comet Native uses a compact status summary and a continuation containing the next
action and command arguments; details are read on demand
([status specification](https://github.com/rpamis/comet/blob/c1118e19d1fbce87706e4265ece17f50db21377e/docs/comet/specs/native-status-output/spec.md),
[Native instructions](https://github.com/rpamis/comet/blob/c1118e19d1fbce87706e4265ece17f50db21377e/assets/skills/comet-native/SKILL.md)).

rctl already returns `next_action`, but [Task.status](../src/rctl/records.py) normally
returns “Prepare the result and required evidence/reviews, then verify; checkpoint to
pause” for active work. The concrete research step is separate free-form handoff text.
The [renderer](../src/rctl/context.py) truncates that text from the end, while the
[handoff template](../templates/state.md) puts the next action after other progress
fields. Consequently a long handoff can lose the part needed to resume.

**Recommendation: next increment.** Distinguish the machine-derived lifecycle action
from the reported work step and blocker. Put the concrete handoff step near the beginning
of short reminders and give it explicit space. Keep source paths and acceptance warnings.
Do not require a new machine record for handoff prose or interpret prose as authorization.
Exact CLI argument suggestions are useful only when the necessary inputs are known.
Adopt the presentation idea without making a new `next` command drive research phases.

### 3. Inspect installation drift and provide reviewable asset updates

Trellis has an update preview and distinguishes framework-managed content from local
changes; conflicts can produce a `.new` candidate for manual comparison
([updater](https://github.com/mindfold-ai/Trellis/blob/88f4834449da9b4f607ec05e322408a0aa66f2ce/packages/cli/src/commands/update.ts)).
Comet Native has diagnostics and separate repair actions
([doctor implementation](https://github.com/rpamis/comet/blob/c1118e19d1fbce87706e4265ece17f50db21377e/domains/comet-native/native-doctor-command.ts),
[recovery guidance](https://github.com/rpamis/comet/blob/c1118e19d1fbce87706e4265ece17f50db21377e/assets/skills/comet-native/reference/recovery.md)).

rctl [init](../src/rctl/initialize.py) deliberately preserves every existing file.
Upgrading the executable therefore does not upgrade a project's copied task skill.
Generated hooks also contain the installed executable and project paths, which can
become outdated after relocation; rerunning init preserves those commands too.

**Recommendation: next increment, with a small first step.** Provide a read-only
installation check and a diff against the current packaged skill/hook definitions.
Check the executable path, configured root, expected rctl handlers, and copied skill
content. A difference means “review needed,” not necessarily corruption. Offer generated
replacement files for comparison before building automatic merge machinery. Keep
research documents, vault notes, and unrelated host settings outside asset updates.
Distinguish static configuration checks from observed host delivery; static inspection
cannot establish hook trust or that the model received a reminder.

### 4. Curate task context and load details on demand

Trellis provides task-specific context lists with paths and reasons, and bounded
subagent context injection
([task commands](https://github.com/mindfold-ai/Trellis/blob/88f4834449da9b4f607ec05e322408a0aa66f2ce/packages/cli/src/templates/trellis/scripts/task.py),
[injection implementation](https://github.com/mindfold-ai/Trellis/blob/88f4834449da9b4f607ec05e322408a0aa66f2ce/packages/cli/src/templates/shared-hooks/inject-subagent-context.py)).
Comet Native instructs agents to use context summaries and expand selected items when
full sources are necessary
([Native instructions](https://github.com/rpamis/comet/blob/c1118e19d1fbce87706e4265ece17f50db21377e/assets/skills/comet-native/SKILL.md)).

rctl already bounds reminders and links source files. Its [context renderer](../src/rctl/context.py)
includes the contract and handoff plus an orientation link; it has no curated task-level
map of relevant guidelines, prior decisions, or baseline notes. Criterion evidence
references serve acceptance and should not be overloaded with general reading material.

**Recommendation: follow-up.** Start with an optional task context section listing a
small number of paths and why each matters. Deliver an index and selected short excerpts,
then let the agent read the necessary sources. There is no need to start with retrieval
models, a memory database, automatic whole-vault injection, or fixed implement/check phases.

### 5. Generate readable verification views and bounded review packets

Comet Native generates `verification.md` from machine-owned state and distinguishes it
from editable requirements. Its Verifier receives scoped acceptance references and
actual check results
([artifact contract](https://github.com/rpamis/comet/blob/c1118e19d1fbce87706e4265ece17f50db21377e/assets/skills/comet-native/reference/artifacts.md),
[command reference](https://github.com/rpamis/comet/blob/c1118e19d1fbce87706e4265ece17f50db21377e/assets/skills/comet-native/reference/commands.md)).

rctl already records criterion-level results, command logs, and attributed reviews.
Its [CLI](CLI.md) exposes the full latest report through `status`, but has no formatted
report export or reviewer packet command. This is a presentation and handoff gap, not
a missing verification engine.

**Recommendation: follow-up.** Render a readable view directly from the acceptance
record: governing revision, each criterion and verdict, rationale, evidence/log paths,
and present applicability. An optional review packet can collect the frozen agreement,
current result, and relevant evidence references for a user-requested reviewer. Rendered
files must not become another acceptance authority. Preserve the distinction between
recorded check results and scientific interpretation in `result.md`. Do not make an
independent model reviewer mandatory or automatically rerun scientific work after a failure.

### 6. Trace supplied requirements to acceptance when a task is large enough

Comet Native maps requirements supplied in source documents to target specifications
and acceptance IDs, while retaining classifications for background, non-goals, and
superseded requirements
([artifact contract](https://github.com/rpamis/comet/blob/c1118e19d1fbce87706e4265ece17f50db21377e/assets/skills/comet-native/reference/artifacts.md)).

rctl's own [acceptance plan](ACCEPTANCE.md) already maps product requirements to checks.
Individual [task contracts](../schemas/contract.schema.json) have criterion IDs but no
standard way to show which supplied requirement each criterion covers. Structural
contract validation cannot discover an omitted substantive requirement.

**Recommendation: optional authoring guidance first.** For a large supplied development
plan or multi-part research request, include a short requirement-to-criterion table in
the contract body. Record intentional exclusions and their reasons. Use evidence-based
review to assess coverage. Small tasks do not need another mandatory artifact, an
exhaustive document-unit inventory, or a repeated confirmation stage.

## Capabilities to defer or retain outside rctl

| Upstream idea | Recommended boundary |
|---|---|
| Supervisor tasks, dependency DAGs, worktree dispatch, integration orchestration | Comet Native documents these in its [Native instructions](https://github.com/rpamis/comet/blob/c1118e19d1fbce87706e4265ece17f50db21377e/assets/skills/comet-native/SKILL.md). Keep execution coordination with agents and runners. Simple task links can support navigation if needed; parent closure must not be inferred from child labels. |
| Mandatory Shape confirmation and Build–Verify repair loops | Preserve existing user authorization and contract stopping conditions. A negative scientific result is not an implementation defect to repair until it passes. |
| Automatic memory learning and reusable policy promotion | rctl already assigns durable findings to project research files and notes. Improve domain-skill practice when there is a demonstrated omission; do not add a competing memory authority. |
| Additional hosts and subagent hooks | Useful when actually required, but the [PRD](PRD.md) intentionally starts with Codex. Each additional adapter needs host-specific documentation and actual delivery evidence. It is not a prerequisite for the improvements above. |

Contract freezing, explicit amendments, currentness checks, command/review separation,
guarded closure, and fresh-session recovery are already implemented correctly for
rctl's documented scope. They should not appear again as missing upstream features.

## Suggested sequence

1. Task list and continuation presentation: make current work easy to find and resume.
2. Installation inspection and candidate diffs: make ongoing package/skill upgrades usable.
3. Curated context and readable verification views: reduce repeated manual reconstruction.
4. Optional source-coverage guidance: use it on tasks where omissions are a real concern.

Names such as `task list`, `doctor`, `update`, or `report` in this discussion are proposed
interfaces, not commands available in rctl 0.2.1. Any selected implementation should
first update the owning product/CLI specification and define checks for its actual failure
modes. This investigation does not itself authorize implementation or publication.

## Retrieval and document checks

Representative commands actually used:

```sh
smart-search doctor --format json
smart-search exa-search '"Comet Native" agent research workflow' --num-results 6 --format json
smart-search exa-search 'Trellis mindfold-ai github features workflow context' --num-results 4 --format json
smart-search fetch https://github.com/rpamis/comet --format markdown --output .work/feature-research/comet-readme-fetch.md
smart-search fetch https://github.com/mindfold-ai/Trellis --format markdown --output .work/feature-research/trellis-readme-fetch.md
git clone --depth 1 https://github.com/rpamis/comet.git .work/feature-research/comet
git clone --depth 1 https://github.com/mindfold-ai/Trellis.git .work/feature-research/trellis
uv run scripts/check_docs.py
git diff --check
```

Discovery results identified candidate sources; the fetched pages and pinned source
files support the comparison. The documentation check passed with 202 local links,
86 JSON files, four schemas/example inputs, and the existing requirement-to-acceptance
mapping. This check validates documentation structure and references, not the proposed
features or upstream execution.

## Limitations

This is source-based research, not an execution benchmark of Trellis or Comet. No
upstream runtimes were installed or run, and their test suites were not executed. The
Comet identity is an explicit assumption pending user correction. Context efficiency
and reviewer independence claims were not measured. The suggestions preserve the
existing preparation and host-evidence boundaries in [READINESS](READINESS.md#limitations).

Local retrieval receipts and disposable checkouts are under `.work/feature-research/`;
the pinned primary-source links above make this note readable without those files.
