# Development Plan

## Latest deployment

v0.6.0 source `7c5dd75` is pushed, passed all four CI jobs, and is installed in the
global tool environment. Installed code/resources match the clean committed tree;
goal-review entry, closure and reminder checks passed in a disposable project.
See the [deployment record](V0.6.0-DEPLOYMENT.md). Live task-draft migration is
separate work. Version-only historical currentness and additional reminder coverage
remain separate runtime work.

## Guidance consolidation, 10 October 2026

Starting agreement: after comparing a peer's agent-paper workflow with LEO, the
user approved a three-step plan: playbook first, then rctl, then LEO. For rctl the
scope is documentation only: reduce research-judgment prose that restated project
guidance in templates and the research-task skill, add a development rule for
future process failures, and change no schema, controller or lifecycle behavior.
Source provenance is in [Distilled sources](DISTILLED-SOURCES.md#guidance-consolidation-10-october-2026).

Changes: the contract and result templates and the skill's SKILL, planning,
task-file and verification references keep the operational parts of the
target-setting, publication-purpose and goal-review guidance and point to project
guidance for the judgments. The task-file section is renamed "Goal contribution
and review" and no longer calls the deployed controller a source increment. Two
operational notes are added: contract exclusions are written for the task's own
question rather than copied from earlier plans, and a method task's primary
criterion can run a fixed evaluator and record its numbers, leaving the outcome to
the goal review. `AGENTS.md` gains the development rule. Net: six template/skill
files, 49 lines added and 99 removed.

Acceptance selected: M1/A-01 (scaffold placeholders and accepted contract structure),
M5/A-21/A-23 (initialization and resource delivery), M8/A-40 (packaged alignment
guidance) and A-41–A-43 (goal entry, review and recovery), all covered by the
existing suite.

Validation on local macOS/Python 3.13.2 in a separate worktree:

- `uv run --locked pytest -q`: **349 passed, 49 subtests passed**.
- `uv run --locked ruff check src tests scripts`: passed.
- `uv run --locked python scripts/check_docs.py`: passed (364 local links,
  100 JSON files, four schemas, 22 requirements and 43 acceptance cases).
- `git diff --check`: passed.

End review: local delivery is a shorter, operational skill and template set with
unchanged behavior. It does not establish that future contracts will be better
judged or that goal drift will recur less. Release, global installation and
live-project skill updates are separate work; the installed CLI remains 0.6.0.

## v0.6.0 release preparation, 10 October 2026

The user authorized push and update after the goal-review branch was repaired,
committed and merged into local main. Version 0.6.0 distinguishes the new mandatory
goal contribution/review behavior and the captured-Goal race repair from installed
0.5.1. It also includes the intervening paper-reading skill and source fixes.

Acceptance selected: A-41–A-43 for goal entry, review and recovery; A-23/A-29/A-40
for installed resources and reminder delivery. Release validation covers tests,
lint, documentation checks, build and isolated wheel smoke. Deployment follows
the exact-source CI gate below and updates the installed CLI from a clean committed
tree. Live task drafts and customized project guidance need their own scoped work.

Local macOS 26.6.2/Python 3.13.2 validation:

- `uv lock`: only the project version changed; runtime/development dependency
  versions are unchanged. An initial `uv lock --offline` could not resolve the
  available registry metadata, so the normal lock command was used.
- `uv run --locked pytest -q`: **349 passed, 49 subtests passed**.
- `uv run --locked ruff check src tests scripts`: passed.
- `uv run --locked python scripts/check_docs.py`: passed.
- `uv build --out-dir .work/goal-review-audit/release-0.6.0/dist`: sdist and wheel built.
- `uv run --locked python scripts/smoke_package.py .work/goal-review-audit/release-0.6.0/dist/rctl-0.6.0-py3-none-any.whl`:
  isolated package smoke passed.
- `uv run --isolated --no-project --offline --with .work/goal-review-audit/release-0.6.0/dist/rctl-0.6.0-py3-none-any.whl python .work/goal-review-audit/verify_goal_race_fix.py`:
  the arithmetic command passes while the concurrent Goal edit makes the review
  unknown and retains the original Goal. Logs are under `.work/goal-review-audit/`.

## Goal-review verification race repair, 10 October 2026

Starting agreement: branch review found that an uncited PROGRAM Goal edited while
a read-only command criterion was running could silently bind an existing review
to the new Goal. Verify read the Goal only when the designated review was reached,
so the report could pass and close. The user requested repair, commit and merge.

Changes: prepare the supplied goal review and capture its Goal before command
execution, then compare that retained Goal after all checks. A substantive edit
or unavailable Goal makes the goal check unknown and adds a subject issue. Retain
the original Goal and exact review input; restoring the Goal later still requires
fresh verification. Whitespace-only edits and Current guidance edits follow the
existing semantic Goal and whole-file citation rules.

Acceptance selected: A-42, with the existing R-21/R-05/R-06/R-07 boundaries. The
regressions use the public CLI and a real arithmetic subprocess, synchronized with
a cooperating editor over loopback. They cover both criterion orders, deletion,
unfinished and malformed Goal content, later restoration, whitespace reflow and
unrelated guidance edits.

Validation on local macOS 26.6.2/Python 3.13.2:

- Red: `uv run --locked pytest -q tests/test_goal_review.py -k goal_change_during_verify`
  failed both criterion orders against the reviewed source: expected unknown, got
  pass; the command-first case recorded the new Goal with the old judgment.
- Green: `uv run --locked pytest -q tests/test_goal_review.py`: **37 passed**.
- `uv run --locked pytest -q`: **349 passed, 49 subtests passed**.
- `uv run --locked ruff check src tests scripts`: passed.
- `uv run --locked python scripts/check_docs.py`: passed.
- `uv build --out-dir .work/goal-review-audit/dist`: built the sdist and wheel.
- `uv run --locked python scripts/smoke_package.py .work/goal-review-audit/dist/rctl-0.5.1-py3-none-any.whl`:
  isolated installed-package smoke passed.
- `uv run --locked python .work/goal-review-audit/verify_goal_race_fix.py`:
  the retained original race probe now rejects with `VERIFICATION_UNKNOWN`, keeps
  the original error Goal and records an unknown goal review while arithmetic
  passes. The same probe passed with the final wheel through
  `uv run --isolated --no-project --offline --with .work/goal-review-audit/dist/rctl-0.5.1-py3-none-any.whl python .work/goal-review-audit/verify_goal_race_fix.py`.

Document/schema checks establish structure; CLI and wheel checks establish
execution and retained subject lineage. Scientific adequacy and deployment
boundaries remain as described in [Readiness](READINESS.md#limitations).

## Goal-decision currentness, 10 October 2026

Starting agreement: after the follow-up below, PROGRAM.md could still reach the
retained goal decision through a reviewer-added citation, an author citation or
another criterion's evidence, because the decision reused report-wide currentness.
Any Goal rewrap also marked decisions stale. The user asked to commit the
follow-up and implement the proposed fix; scope stays source-only.

Changes: `goal_impact.currentness` (and `task list` `goal_decision`) now covers
cycle, revision, version, contract/result text, the goal review's own local
evidence and the recorded Goal, which replaces PROGRAM.md observation when present.
Goal comparison ignores whitespace. `close` keeps report-wide currentness.

Validation on local macOS/Python 3.13.2:

- New cases: a reviewer-cited PROGRAM.md edited before close blocks close until
  verified again; edited after close leaves the task stale while the goal decision,
  task-list row and reminder stay current; a reflowed Goal stays current and closes.
  Both failed against the previous source (`stale` instead of `current`) and pass now.
- `uv run --locked pytest -q`: **342 passed, 49 subtests passed**.
- `uv run --locked ruff check src tests scripts`: passed.
- `uv run --locked python scripts/check_docs.py`: passed (356 local links, 100 JSON
  files, 22 requirements and 43 acceptance cases).

Not rerun: wheel build and packaged smoke; no LEO observation. A typo fix or
equivalent rewording of the Goal still marks retained decisions stale.

## Goal-review follow-up, 10 October 2026

Starting agreement: a review of the controller increment below found that the
mandatory `research/PROGRAM.md` citation made every goal review depend on the whole
file. Observation compares size and mtime, so Current guidance edits, closeout
promotion, or a checkout marked reviewed stop decisions stale in status and
reminders, which reads as permission to continue. The user asked to commit the
increment and implement the recommended fixes. Scope stays source-only and
unreleased; no live task, installation or release changes.

Changes:

- The goal review cites `result.md` and primary evidence; PROGRAM.md is optional
  and not primary evidence. Verify records the Goal text as `reviewed_goal`;
  currentness compares it with the current Goal. An unavailable Goal leaves the
  review unknown. Pre-follow-up reports have no `reviewed_goal` and are unaffected.
- `contract check` keeps the original agreement for an unchanged accepted contract;
  a changed contract follows the amendment rule.
- `task list` rows carry `goal_decision`; planning guidance reads related decisions
  and requires a resumed stopped/adjusted obligation to name its task and reason.
- Verification guidance recommends writing `goal_impact` from a fresh context and
  allows `reviewer: operator` for costly continuation; this is practice, not
  enforcement.

Acceptance selected: A-41–A-43 wording updated (counts unchanged at 22/43).

Validation on local macOS/Python 3.13.2:

- `uv run --locked pytest -q`: **340 passed, 49 subtests passed**. New or changed
  cases: Goal change blocks close; Current guidance edits before and after close
  keep the review and `goal_decision` current; unavailable Goal leaves the review
  unknown; PROGRAM-only primary evidence rejects; unchanged retained contract passes
  `contract check` while a changed one rejects.
- `uv run --locked ruff check src tests scripts`: passed.
- `uv run --locked python scripts/check_docs.py`: passed (356 local links, 100 JSON
  files, 22 requirements and 43 acceptance cases).
- A scratch run of text-mode `task list` printed the indented goal decision line.

Not rerun: candidate wheel build and isolated package smoke; no LEO observation.
The fresh-context review practice is guidance only and untested in a live host.

## Goal-review controller increment, 10 October 2026

Starting agreement: the user asked how to make final-goal checking unavoidable,
after inspecting the gap between publication-purpose guidance and core validation.
The useful output is a source implementation that prevents missing goal judgments
at entry/closeout and exposes their investment consequence at recovery. This
enables accountable paper-directed task decisions; it does not validate a LEO
method, novel contribution, paper viability or future judgment quality.

Bounded scope: use existing PROGRAM Goal, contract criteria, review inputs and
snapshot/reminder projections. No new goal database, project flag, human approval,
task scheduler, global installation, live-task migration, release or commit.
Retained old agreements stay readable. New contracts/amendments in a project
with a completed Goal require contribution and its review. Structured impact is
retained separately from local pass; negative decision tasks may close.

Acceptance selected: new R-21/R-22 and A-41–A-43, with compatibility coverage from
M1/M2 (contract, record, actual checks and closure), M7/M8 (bounded retained-source
reminders) and packaged task guidance. Source tests must observe omitted-review
rejection, honest negative closure, evidence changes and revision separation.
Field completeness is mechanical; evidence support remains a reviewer judgment.

Validation on local macOS/Python 3.13.2:

- `uv run --locked pytest -q`: **337 passed, 49 subtests passed** after repairs.
  The first targeted run exposed mis-indented reviewer YAML and a scaffold
  comment leaking into enabled frontmatter; repaired both. Older reminder tests
  now accept their legacy agreement before loading later PROGRAM guidance.
  Fully authored generated drafts also exposed commented placeholder leakage;
  the generator now removes instruction comments and positive cases cover both
  standalone and goal-linked entry.
- `uv run --locked ruff check src tests scripts`: passed.
- `uv run --locked python scripts/check_docs.py`: passed (356 local links,
  100 JSON files, four schemas, 22 requirements and 43 acceptance cases).
- Built the candidate wheel in `.work/goal-review-increment/dist/` and checked its
  isolated package compatibility: **37 CLI invocations passed**. Eight changed
  code/schema/template/skill files matched the final wheel bytes. The smoke log is
  `.work/goal-review-increment/wheel-smoke-final.log`.
- Read-only LEO observation: the installed CLI accepts the current
  `venue-calibrated-contribution-case` draft; `uv run --locked --project` against
  this checkout rejects it for missing `goal_contribution`. This confirms the
  omission guard on the real populated Goal, and the fact that global deployment
  has not occurred. No LEO task or research decision was changed.

End review: local delivery establishes entry/closeout omission checks and visible
retained goal decisions, including honest negative closure. For the final applied
paper objective this is enabling accountability only: target contribution, method
benefit, backend evidence and publication viability remain unchanged and unproven.
Next investment is a scoped deployment/versioning and live-draft migration, then
the already bounded contribution case; these source checks do not authorize a
research campaign or establish future semantic-review quality. Source-only delivery
must not be reported as installed enforcement in LEO.

## Publication-purpose guidance, 10 October 2026

The user requested goal-linked task contracts and end verification for a paper-directed
project. Update existing contract/result templates and research-task planning,
task-file and verification guidance: name the publication evidence obligation at
entry, and review its consequence for the claim or next investment at closeout.
The numeric criterion example uses existing Question alignment and review methods.
No schema, controller, hook shape, acceptance-case count or reviewer authentication
changes are included. Source provenance is in DISTILLED-SOURCES.md.

Relevant compatibility obligations: M1/A-01 (scaffold rejection and accepted contract
structure), M5/A-21/A-23 (initialization/resource guidance), and M8/A-40 (packaged
alignment instructions). This documentation-only change uses targeted source/resource
checks; installed-wheel rollout and new native-host use are not claimed.

Validation completed on 10 October:

- `uv run --locked python scripts/check_docs.py`: pass for repository-owned links,
  schemas and retained example inputs.
- Targeted pytest cases for scaffold placeholders, source/resource agreement,
  packaged alignment guidance, preserved customized initialization, exported
  workspace references and skill metadata/scripts: **25 passed**.
- skill-creator's `quick_validate.py`: the source research-task and the inspected
  LEO-local copy are valid.
- The LEO calibration task checks both actual draft contracts and newly added
  cross-project pointers, and retains its source/change evidence under
  `LEO/runs/publication-goal-workflow-calibration/`.

The first LEO draft used nonnumeric criterion suffixes and was rejected structurally;
numeric IDs were corrected before begin. This is an authoring correction, not a
parser defect. The new requirement is semantic review work: these compatibility
checks do not establish scientific benefit or future resistance to goal drift.

## Agent-citable paper records, 10 October 2026

At the user's request, research-literature now writes a short record file per paper
in place of the sectioned note: a provenance header and typed one-line records
(setting, result, null, verbatim limitation, defect, test, relation, lead), each
with an anchor, evidence basis and confidence. The overview, field map, method
narrative, experiments boilerplate and analyst reflection are removed; one clean
reader may take two to four papers on the same question. Research-synthesis cites
`<paper-id>#R<n>`, and research-question and research-ideation now say that reading
ideas stay as `test` or `lead` records. The
[source record](DISTILLED-SOURCES.md#reading-and-research-candidate-development) gives
the reason and what was retained.

- `uv run --locked pytest -q tests/test_skill_assets.py tests/test_research_skill_contracts.py tests/test_research_handoffs.py`:
  70 passed, 49 subtests passed.
- `quick_validate.py` on research-literature, research-synthesis, research-question
  and research-ideation: all valid.
- `uv run --locked python scripts/check_docs.py`: passed.
- `uv run --locked ruff check tests/test_research_skill_contracts.py` and
  `git diff --check`: passed.

These are structural checks; no reader has used the new template yet.

## Portable provenance references, 6 October 2026

CI runs `36582133682` and `36713873517` passed all tests and lint on all four
jobs, then failed documentation checks on links to untracked `.work/` captures
and sibling OR files. The local checkout supplied those files and hid the failure.
The documentation now retains those sources as labeled provenance paths, including
the newer LEO/playbook references, and keeps repository-owned links checkable.
The link checker and workflow are unchanged.

Checks on source `ab4a697` before this documentation-only repair:

- `uv run --locked pytest -q`: 312 passed, 49 subtests passed in 39.48 seconds
  on local macOS/Python 3.13.2.
- `uv run --locked ruff check src tests scripts`: passed.
- `uv build --out-dir .work/recent-change-check-20261006/dist`: passed.
- `uv run --locked scripts/smoke_package.py .work/recent-change-check-20261006/dist/rctl-0.5.1-py3-none-any.whl`:
  passed with 37 CLI invocations and a closed native experiment.

After the repair, `uv run --locked python scripts/check_docs.py` and the same
checker invoked with the project Python against a `git archive HEAD` extraction
overlaid with the three edited documentation files both passed: 344 local links,
100 JSON files, four schemas and 40 acceptance cases. `git diff --check` passed.
The clean extraction contains no sibling projects or local captures. Local evidence
is under `.work/recent-change-check-20261006/`. A pushed-commit CI run remains pending.

## Target-setting guidance, 6 October 2026

The user authorized a source change and commit to carry the target setting through
project/task templates and research-task's planning and review guidance. The
[source record](DISTILLED-SOURCES.md#target-setting-across-task-planning-and-review)
records the observed LEO failure and retained results. Substantial scenario selection
can use an analysis task; its output is a justified architecture/workload choice
and evaluation route, or the exact unresolved link. Existing alignment fields and
review criteria carry that relationship into implementation and closeout.

Use M1/A-01 for template compatibility, M5/A-21/A-23 for resource delivery and
preservation, and M8/A-40 for alignment guidance. Existing M7/M8 checks also cover
unfinished project guidance and the distinction between task assessment and
verification. Repair the affected authoring guidance if those checks fail.

The author applied the revised guidance to the retained LEO material:

| Inspected evidence | Review decision and continuation |
| --- | --- |
| C5 source loads whole image bands; planning records contain image dimensions and a Pi product specification, but no memory measurement or target data-center mapping. | Retain the source observations. The proposed target bottleneck is unresolved; identify the architecture/workload relationship before choosing a representative memory limit. A bounded feasibility result may report that gap. |
| The completed comparison reports 5/6 versus 3/6 integrations on development-exposed applications with a modeled resource envelope. | Retain that local result. It does not establish resource-driven adaptation or the target data-center workflow. Scope the claim and investigate the missing relationship without repeating completed integration runs merely to relabel them. |

Validation on 6 October 2026:

- `uv run --locked pytest -q tests/test_m1.py tests/test_init.py tests/test_m7.py
  tests/test_m8.py 'tests/test_skill_assets.py::test_skill_metadata_resources_and_script_syntax[research-task]'`:
  112 passed and two legacy Scope-placeholder checks failed. Restored the original
  contract marker and placed the new guidance beside it. Then
  `uv run --locked pytest -q tests/test_m1.py::test_v050_scaffold_placeholders_still_reject_acceptance
  tests/test_m1.py::test_new_draft_preserves_other_files_and_refuses_overwrite`:
  all five affected checks passed. Tests and parser behavior were unchanged.
- `uv run --locked python scripts/check_docs.py`: passed, 358 local links. The
  first run exposed an existing missing OR temporary retrieval file; preserved its
  historical path and stated its availability in Distilled Sources instead of
  presenting a broken link as available evidence.
- `uv build --wheel --out-dir .work/target-setting-20261006/dist`: passed.
  A `uv run --locked python` ZIP inspection compared each of the seven changed
  template/skill files with its `rctl/` wheel entry; all matched source bytes.
- `git diff --check`: passed.

Delivery is limited to the repository; package release and live-project upgrades
are separate work. See [Readiness](READINESS.md#limitations) for the scope of this
author walkthrough.

## Completed release preparation

Prepared v0.5.1 from the training migration (`1c098df`) and
comparison-template follow-up (`0140b19`). Restore route-entry granularity,
separate open-question ownership, explain evidence for living guidance, and
shorten shared comparison instructions using generic terminology. Read short
project guidance first and related history on demand. Preserve native scaffold
markers and existing invocation policies.

Use A-01/A-02 for draft compatibility and A-21/A-22/A-23/A-24/A-29 for resource
delivery and preservation, plus the full release checks. The version bump leaves
currentness behavior unchanged: closed tasks may show a version-only stale report
without losing historical closure. Runtime display changes and reminder coverage
are separate follow-ups. The
[review record](COMPARISON-REVIEW-FOLLOWUP.md) records decisions and validation.

## Current skill-source work

The writing follow-up separates paper-wide figure planning from individual figure
production and adds section references. The Method reference distills its source's
structure, equation, component, pseudocode, and novelty guidance into concise
writing essentials. The Experiments and References guides added on 2026-09-24
cover contribution-driven experimental reporting and bibliography preparation,
with conditional links from the writing skill. [Distilled Sources](DISTILLED-SOURCES.md)
records the source material and adaptations.

The standalone research-computation entrypoint is retired. Shared numerical checks
now live in research-theory's references and are read directly by the relevant
workflows; they add no required stage. The [catalog](RESEARCH-SKILLS.md#shared-computation-checks)
defines the new ownership and installation boundary. Use M5/A-23/A-24 for affected
resource and packaging checks, including removal of the retired entrypoint and
delivery of the shared reference. CLI behavior, schemas, and native acceptance
remain unchanged; release and global installation updates are separate work.

The 2026-09-24 reading/ideation simplification retires research-opportunity-mining.
Reading and synthesis retain useful exploratory thinking alongside their evidence;
ideation consumes the source material directly, checks decisive factual premises,
and identifies unresolved capabilities without a default candidate count or lens
quota. The reading reference distills the supplied seven-step guidance, and the
existing candidate template carries the causal explanation and uncertainty.
Historical seed files remain available without becoming a required intermediate.
Use M5/A-23/A-24 for resource, package, and handoff checks: verify removal of the
retired package, delivery of the reading reference, remaining invocation policies,
and compatibility with the existing evaluation validator. Native task records,
evaluation selection rules, and experiment execution remain unchanged.

Validation on 2026-09-24:

- `uv run --locked pytest -q tests/test_skill_assets.py tests/test_research_skill_contracts.py tests/test_research_handoffs.py`: 59 passed, 35 subtests passed.
- `uv run --locked python /Users/zhangbowen/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/<name>`: passed for research-literature, research-ideation, and research-synthesis.
- `uv run --locked python scripts/check_docs.py`: passed; `uv run --locked ruff check tests/test_research_skill_contracts.py` and `git diff --check` also passed.
- `uv build --wheel --out-dir .work/literature-ideation-simplification-20260924/dist`: passed. A ZIP resource inspection matched all 15 entrypoints to source, checked all nine files in the three affected packages and their local links, and confirmed both retired packages absent. The result is in `.work/literature-ideation-simplification-20260924/wheel-resource-check.txt`.

These are structural, handoff-execution, and distribution checks. Research quality
and agent adherence remain untested. This source validation preceded the
[local shared installation](RESEARCH-SKILLS.md#local-shared-installation); no
live-project merge was performed for this increment.

Before the user-requested local skill installation on 2026-09-24,
`uv run --locked pytest -q` passed all 301 tests and 35 subtests in 41.12 seconds.
Full lint (`uv run --locked ruff check src tests scripts`), documentation checks,
and structural validation of the remaining modified skill entrypoints also passed.
The subsequent shared-skill installation completed from source commit `452ed0e`;
all 14 user-level skills resolve to it and the two retired workflows' discovery
links were removed. The installed rctl CLI remains at the released 0.5.1 build.

On 2026-09-30 the seven-step reading guidance moved from research-literature's
separate reading reference into its skill and paper-note template; the reference
is removed. The template's section order now carries the reading order, and the
skill routes code inspection and reproduction. Overlapping note sections were then
merged (16 to 10 headings) without dropping test-locked or provenance fields.
A disposable trial with clean readers on three OR-project papers (notes kept outside
the project) produced 5,500–5,800-word notes; on one paper the previous template
with the same reader model produced 3,745 words. The template then gained
concision rules (one-line metadata, theorem statements without proof retracing,
one-line minor defects) rather than a fixed word budget; a rerun of that paper
produced 4,655 words and kept five of six previously found material defects.
`uv run --locked pytest -q
tests/test_skill_assets.py tests/test_research_skill_contracts.py
tests/test_research_handoffs.py` (70 passed, 49 subtests), `scripts/check_docs.py`,
the skill-creator validator, and `git diff --check` passed. These are structural
checks; the trial is a small single-run use check, not a quality evaluation. The shared installation links to this source
directory, so it follows the checked-out files without a separate copy step.

## CI smoke repair

The pushes of `3130531` and `e43442e` failed installed-wheel smoke on all four CI
jobs; pytest, lint, documentation checks, and build passed. The scale-control
template change in `3130531` modified one contract placeholder and added six
contract fields plus two result fields. `scripts/smoke_shared_skills.py` still
filled the older templates. The first seven unfilled placeholders stopped the
walkthrough before result authoring. The source checks above did not run the full
wheel smoke and therefore missed this failure.

The repair completes those fields with bounded synthetic-fixture values and
retains both unfilled-placeholder assertions. M5/A-23/A-24 cover this change.
The regular pytest suite now runs the same native experiment walkthrough,
including rejected unresolved/failed verification and successful negative closure.
The source distribution includes the helper required by this regression test.
Templates, runtime behavior, and shared installations are unchanged.

Validation on 2026-09-24:

- `uv run --locked pytest -q tests/test_skill_assets.py::test_experiment_templates_complete_native_smoke --tb=short`: reproduced the seven-placeholder failure before the fix, then passed.
- `uv run --locked pytest -q`: 302 passed, 35 subtests passed on Python 3.13.2.
- `uv run --locked ruff check src tests scripts`: passed.
- `uv build --out-dir .work/ci-smoke-fix-20260924/dist`: built the source distribution and its wheel. Archive inspection confirmed the regression test and smoke helper match source.
- `uv run --locked scripts/smoke_package.py .work/ci-smoke-fix-20260924/dist/rctl-0.5.1-py3-none-any.whl`: passed on Python 3.13.2; 37 CLI invocations, with the native experiment closed as `not_supported`.
- `UV_PROJECT_ENVIRONMENT=.work/ci-smoke-fix-20260924/py311 uv run --locked --python 3.11 scripts/smoke_package.py .work/ci-smoke-fix-20260924/dist/rctl-0.5.1-py3-none-any.whl`: passed on Python 3.11.11 with the same 37 invocations. The first attempt stopped at offline dependency installation; installing the wheel into a disposable environment populated the missing cache before retry.

Smoke output is retained under `.work/ci-smoke-fix-20260924/` in
`wheel-smoke-py313.txt` and `wheel-smoke-py311-retry.txt`; the initial Python 3.11
failure is in `wheel-smoke-py311.stderr`. These are local macOS execution checks.
The repair still needs a pushed-commit CI run to establish the full platform matrix.

## Included source increments

The September23 comparison-template follow-up adds project problem/method and
comparison-guidance scaffolds, scopes route decisions and control versions, and
updates native task authoring plus research-task references. Use A-21/A-22/A-24
for affected initialization/preservation/template checks. CLI, schemas, task
phases and host integration are unchanged. Source validation is distinct from
installed-wheel delivery and release; see
[COMPARISON-TEMPLATE-FOLLOWUP.md](COMPARISON-TEMPLATE-FOLLOWUP.md).

The 2026-09-21 source-management follow-up adds experiment-adapter-builder and
model-training-workflow, including their validators, fixtures and pinned source
audit. Use M5/A-23/A-24 for packaged resources and A-21/A-29 for task-only
init/export preservation. Preserve scientific instructions and native invocation
policies; redirect existing discovery links after package verification. The
[migration record](RESEARCH-SKILLS-MIGRATION.md#training-and-adapter-follow-up)
records the source cutover. Other auxiliary tools and live tasks stay outside scope.

The completed research-skill review follow-up repaired two rounds after source migration:
pilot/formal handoffs, human selection sizes, vault and installed-resource paths,
operation-specific completion, and computation/theory/writing evidence boundaries.
That increment kept research-computation as an optional lightweight helper and
preserved invocation policies, human selection, and native rctl acceptance. Its
standalone entrypoint is retired by the current source work above. Use M5/A-23/A-24 as the main
integration checks, plus A-22/A-29 for binding and packaged-asset regressions. The
[follow-up record](RESEARCH-SKILLS-FOLLOWUP.md) records changes and their checks.

The preceding migration consolidated 13 research workflows from agent-skills-private
and the independently installed research-rapid-test, preserving their source content
and existing installation identities. The
[catalog](RESEARCH-SKILLS.md) defines ownership and the
[migration record](RESEARCH-SKILLS-MIGRATION.md) records preservation and cutover.
Auxiliary tools, live tasks, shared installation configuration, and CLI deployment stay
outside this follow-up. The simplification increment below is committed at `87157e9`.

The governing-question alignment baseline is v0.5.0 at `82a5ec8`. The user
requested implementation of the [simplification plan](SIMPLIFICATION-REVIEW.md)
on 2026-09-14. This unreleased follow-up keeps lifecycle, schemas, and public CLI
syntax stable while shortening the packaged skill, sharing immutable task snapshots,
and using one reminder layout with both existing hook events.

Use M8/A-37–A-40 as the regression anchor, plus the affected discovery, context,
packaging, history-reuse, and real-host cases identified in the plan. The
[verification record](SIMPLIFICATION-VERIFICATION.md) separates automated behavior,
installed-package execution, and observed GPT-6-Astra use. Remaining installation,
review-input, and verification-protocol decisions stay outside this increment.

## Work by affected behavior

README defines document authority. Use PRD for scope, SPEC for behavior, CLI for
syntax/output, schemas for structural inputs, and INTEGRATION for skills and hooks.
Select the affected ACCEPTANCE cases before implementation. Update an owning
document and its examples/tests before changing its contract; resolve routine
internal choices within the authorized task.

Use uv and the locked project dependencies. Keep source and installed-package
behavior consistent: schemas, templates, and skills ship in the wheel. Parsing,
record publication, execution, currentness, and host delivery retain distinct owners.
Tests cross the supported read/lifecycle interfaces, use real local files and
subprocesses where those affect behavior, and preserve distinct regression coverage.

Run affected tests during development, then the full suite once before release,
plus lint, documentation checks, build, and installed-wheel smoke. The commands
are in [README](../README.md#run-the-local-cli). Record actual versions, commands,
results, and untested behavior. A hook fixture proves the payload contract; actual
host/model delivery and scientific adequacy need their respective evidence.

Shared installations, live research tasks, and host configuration are changed only
when the current task includes those targets. The simplification acceptance probes
use disposable local projects and invocation-local reviewed hook definitions.

## Release and deployment order

For authorized upgrades of actively used projects: complete local validation,
commit and push the release, then wait for the CI run on that exact commit to
succeed before installing or updating project assets. Build deployment artifacts
from that clean committed source and verify the installed code/assets against it.
After deployment, run scoped installation and reminder checks. If CI fails, fix
and validate a new commit before deployment. Local tests alone do not satisfy this
release gate; an explicit user request may authorize an experimental deployment.

## Changes from the original proposal

| Original proposal | v0.1 development baseline | Reason |
|---|---|---|
| SQLite state and events, row/material versions, migrations | One machine record per task; accepted contract revisions and actual check records | Target the demonstrated task boundary before database operations. |
| Content-addressed objects and general snapshots | Exact retained contract/result text; lightweight metadata observations of declared evidence | Detect ordinary drift without copying a scientific artifact store. |
| `context / record / verify / advance / report` plus broad supporting commands | The explicit command set in CLI, including begin/amend/verify/close | Give each operation one narrow meaning; no generic advance or status setter. |
| Separate in-review phase and default local approval for analysis | Review criteria inside verification; active/closed/cancelled phases | Scientific review is required when the contract calls for it; avoid automatic approval ceremonies. |
| Claude Code first | Codex first, anchored to the existing pilot | There is already host execution evidence to start from. |
| Full backup/restore subsystem | Whole-task copying when quiescent, followed by fresh verification | No database or immutable-object service to back up in v0.1. |
| Same-host concurrent writes, idempotency protocol | One writer per task and a detected-change recheck | Keep coordination proportional; stronger coordination needs its own observed use case. |
| New `.claude/skills/research-state` and installation merge machinery | Exported local `research-task` package and reviewed host bundle | Preserve shared skills and unrelated live configuration. |

Keep the original's useful semantics: closure needs evidence, successful execution is not scientific validity, negative findings may finish, historical acceptance has a scope, and a session can stop before the task closes.

## Historical milestones

The [release-evidence index](RELEASE-EVIDENCE.md) maps completed increments and
review follow-ups to their original verification records. M1–M8 and the v0.1 release
remain completed historical work; v0.6.0 deploys the goal-review increment and
intervening source changes.
The older development proposal remains historical and does not override this plan.
