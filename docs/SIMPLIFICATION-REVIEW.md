# rctl Simplification Review and Implementation Plan

Status: first increment implemented and locally validated on 2026-09-14; outcomes
and the observed instruction repair are in [the verification record](SIMPLIFICATION-VERIFICATION.md).
Baseline: v0.5 at `82a5ec8` (`Fix governing question alignment regressions`).
Deferred decisions below remain planned. This document does not override the product,
behavior, CLI, schema, or acceptance authority defined in [README](../README.md).

## Decision and objective

Make a bounded post-v0.5 simplification increment for GPT-6-Astra. Prioritize the
packaged research-task skill and reminders that the model actually consumes in a
research project. Cleanup of rctl's own development instructions, internal code,
and historical navigation supports that work but has a different audience.

The intended improvement is that Astra can select the right task, recover its
agreement and next action, and complete authorized work with fewer irrelevant
instructions and repeated reads. Keep rctl's core independent of models and hosts;
no model detection or model-specific runtime mode is needed.

OpenAI's [Astra guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
recommends progressive disclosure and fewer fixed recipes, while also recommending
clear completion conditions and persistence. That supports a smaller instruction
surface together with rctl's explicit completion contract. Use the codebase-design
criterion of a small Interface hiding useful behavior; source line count alone
does not establish a benefit.

## Behavior to retain

- `contract -> begin -> verify -> close`, exact retained agreements and results,
  explicit amendments, reopen cycles, and historical closure.
- Separate task phase, check verdict, scientific assessment, and currentness.
  Negative and bounded inconclusive results can satisfy their completion criteria.
- Actual declared check execution, attributed evidence review, ordinary evidence
  change detection, and atomic record publication.
- Explicit task selection, project guidance when no task is selected, and durable
  handoffs with a concrete next action and blockers.
- Accepted governing question, declared test and non-claim scope, and history reuse
  before a new experiment or material change of direction.
- Freedom to choose methods within the agreement. Existing user authorization
  remains sufficient; preparing a contract does not add an approval ceremony.
  Managed completion still requires successful `close`.

The first increment keeps record/input schemas, lifecycle rules, review-input
requirements, public command syntax, and hook response envelopes unchanged. It
does not introduce orchestration, remote execution, or an additional task system.

## Disposition of the original proposals

| Proposal | Decision | Implementation scope |
|---|---|---|
| 1. One concise reminder | First increment, with both events retained | One layout with the existing budget caps; remove appended contract/handoff excerpts. Decide event retirement separately. |
| 2. Root skill as a router | First increment | Route detailed workflows on demand, retain essential command examples and rctl-specific conventions. |
| 3. Codex installation lifecycle | Deferred | Clarify the primary route before considering a plugin or CLI redesign. The internal `hook codex` command is not a user setup step. |
| 4. Derived task snapshot | First increment, limited to the reminder work | One internal typed snapshot consumed by status, context, and discovery projections. |
| 5. Verification authoring and versioning | Two separate deferred decisions | Keep current review input for now; separately design verification compatibility across package versions. |
| 6. Behavior-based documentation and tests | Small navigation cleanup now; broader moves later | Keep historical evidence paths, and reorganize only tests touched by the new Interface. |

## First-increment implementation sequence

Use **M8, A-37 through A-40**, as the existing milestone and regression anchor.
Reuse the additional acceptance cases below for affected behavior. Existing pass
records remain historical evidence, not proof that the new increment passes.
Keep this work separately reviewable from the v0.5 release closeout.

### 1. Simplify the packaged research-task skill

Primary files: [root skill](../skills/research-task/SKILL.md), its
[workspace reference](../skills/research-task/references/workspace.md), and
[task-file examples](../skills/research-task/references/task-files.md).

- Keep task selection, document authority, completion rules, and a small
  intent-to-reference map in the root. Keep the trigger for history reuse before
  experimental planning and the requirement to respect declared non-claim scope.
- Retain concise examples for the common lifecycle commands. Keep global-option
  ordering, project-relative CLI paths versus task-relative evidence paths, and
  the fact that a failed verification may still save a report. Use targeted help
  for unfamiliar syntax, not as a repeated prerequisite for known commands.
- Route initialization and maintenance to `references/workspace.md`; route file
  authoring to `references/task-files.md`. Move planning/history detail and
  verification/closeout detail into focused references where needed. Add a
  reference only when it replaces root content with a clear operation-specific
  destination; do not create one file per command.
- Keep scientific methods with the domain skills and keep rctl's lifecycle rules
  in one place. Remove duplicate generic planning, testing, and approval advice.
- Ensure the references travel with both the wheel and exported skill. A research
  project must not need this development checkout to follow its installed skill.

Deletion target: detailed workflows currently loaded by every skill activation,
and repeated explanations retained in more than one reference. The root currently
has about 1,306 English words; use that as a baseline, not a target word quota.

Acceptance: A-20 and A-34 for bounded planning behavior, A-23/A-29 for packaged
assets, and A-40 for alignment guidance. If the shorter root causes missed history,
incorrect commands, or repeated help/reference navigation, repair the routing or
restore the specific useful example.

### 2. Unify task projections and shorten reminders

Primary files: [records](../src/rctl/records.py),
[context](../src/rctl/context.py), [discovery](../src/rctl/discovery.py), and
[CLI rendering](../src/rctl/cli.py). Change integration code only where it consumes
the shared projection.

Before changing output, update the relevant sections of [SPEC](SPEC.md),
[CLI](CLI.md), [INTEGRATION](INTEGRATION.md), and [ACCEPTANCE](ACCEPTANCE.md).
In particular, SPEC currently requires extended contract/handoff excerpts. Make
their removal explicit while preserving the required recovery information.

- Introduce an internal typed, immutable `TaskSnapshot` for one read's derived
  task state and diagnostics. Reuse existing parsing, handoff, and currentness
  logic behind it; lifecycle mutations and check execution keep their owners.
- Produce status JSON/text, discovery rows, and reminder projections from that
  snapshot. Renderers perform no additional filesystem reads and do not mutate
  the snapshot. Preserve complete status data and separately bounded context data.
  Each new call reads fresh state; add no snapshot store or cross-call cache.
- Use one concise reminder layout with the existing 8,000- and 2,000-character
  caps. Keep both `SessionStart` and `UserPromptSubmit`, their selection rules,
  and their response shape. Different caps do not need different content formats.
- Keep identity/revision, governing question, declared alignment, verdict,
  assessment/currentness, relevant historical closure, project guidance, warnings,
  reported blockers/next action, lifecycle action, and source paths visible.
  Preserve the distinction between reported progress and machine acceptance.
- Remove the appended full contract and handoff excerpts. Preserve useful field
  prioritization and explicit truncation markers. When the working contract has
  drifted, point to the retained governing text as well as the drift warning;
  following a source must not substitute the edited draft for the accepted scope.
- Preserve project-only and damaged-task behavior, legacy-record readability,
  and bounded context JSON. Replace overlapping tests as their callers move to
  the snapshot; keep coverage of every distinct observable failure.

Deletion target: the separate extended-excerpt branch, repeated task-state
interpretation, and renderer code that constructs a modified copy of status.
The snapshot should concentrate existing behavior, not become a general framework.

Acceptance: A-11/A-12/A-16, A-25/A-27, A-31 through A-33, and A-37 through A-40.
Missing accepted scope, contradictory projections, lost warnings/next steps, changed
record semantics, or hidden damaged tasks require a fix before proceeding.

### 3. Validate Astra use and finish the documentation

Run the three bounded cases below with GPT-6-Astra against the fixed v0.5 baseline
and the candidate, using disposable local projects and the same supplied evidence.
Record the exact host version, model/reasoning settings, launch procedure, delivered
context, relevant source reads, and observed continuation. Use extra help calls and
repeated document reads to diagnose regressions; do not build a scoring framework
or repeat runs merely to obtain a favorable result.

| Case | Required observation | Failure and response |
|---|---|---|
| Recover concrete work | A first session saves a realistic long handoff; a distinct fresh session receives the reminder and performs its named next step using source files as needed. | The next step is lost or needs transcript reconstruction; repair the summary or skill routing. Covers A-18/A-30. |
| Preserve a narrow negative and reuse history | A current passing negative can close. A fresh session reads the aligned result and, when asked for a follow-up proposal, cites related evidence and a distinct question/decision without starting extra execution. After actual automatic compaction it still identifies the accepted scope, what the result does not decide, and relevant project guidance. | A local result becomes a project-level rejection, or the proposal repeats a route without justification; repair the declaration or planning guidance. Covers A-07/A-20/A-34/A-35/A-38/A-39. |
| Respect verification state | A result/evidence change makes verification stale and closure is rejected; a handoff-only change preserves applicability. Astra follows the named corrective action within the agreement. | A stale result is closed or a handoff triggers unnecessary verification; fix state derivation or instructions. Covers A-03/A-08. |

Use local synthetic or already public evidence that reproduces the OR scope-drift
relationship; this plan requires no edits to live OR or Pinyin VSR tasks. Hook
receipts establish delivery, executed CLI checks establish runtime behavior, and
inspection of the actual continuation establishes the evidence-based judgment.
Presence of a sentence in a payload alone does not establish model behavior.

Then shorten current navigation in [README](../README.md) and
[DEVELOPMENT](DEVELOPMENT.md), and add a release-evidence index if it removes the
repeated milestone recital. Keep historical verification documents at their current
paths. Route [AGENTS.md](../AGENTS.md) development reading by the affected change,
preserving document authority and the existing proportionate-check rule. These
development instructions are separate from the skill installed in research projects.

Complete the affected tests during each implementation step. Before finishing the
increment, run the full suite once, lint, document checks, build, and installed-wheel
smoke. Repair the named regression rather than broadening the work:

```sh
uv run pytest
uv run ruff check src tests scripts
uv run scripts/check_docs.py
uv build
uv run scripts/smoke_package.py dist/rctl-VERSION-py3-none-any.whl
```

Replace `VERSION` with the actual built version. Tests detect behavioral regressions;
lint detects code defects; the document check detects broken local references and
structural inconsistencies; build/smoke detect missing assets and checkout-only
behavior. Keep actual commands, outcomes, evidence paths, and unresolved cases in a
new increment verification record; do not rewrite old verification results.

## First-increment completion conditions

- The root skill routes detailed work and retains enough command knowledge to
  avoid routine rediscovery; all required references ship with the package.
- Status, context, and discovery consume one derived task-state Interface. Both
  hooks use one concise layout and continue reading fresh state.
- Accepted question/alignment, warnings, handoff continuation, and verification
  applicability survive realistic bounded reminders without full-document injection.
- The three Astra cases and affected automated/package checks have observed
  evidence. The authoritative documents describe the resulting behavior consistently.
- Superseded instruction and renderer paths are removed, while distinct regression
  coverage and historical verification records remain discoverable.

The first increment is complete without retiring a hook event, adopting a plugin,
changing review schemas, or moving the entire test suite. Release and live rollout
follow the existing [deployment order](DEVELOPMENT.md#release-and-deployment-order)
when those actions are in scope.

## Deferred decisions

### Retire per-prompt delivery only after testing freshness

The [official hook contract](https://developers.openai.com/codex/hooks) says that
`SessionStart` with source `compact` runs before the next model request, including
mid-turn automatic compaction. It does not establish prompt-to-prompt freshness
after a handoff, contract, or project-guidance update.

After the first increment, test startup, resume, and automatic-compaction recovery
without `UserPromptSubmit`, plus a same-session update followed by the intended
explicit `rctl context` refresh. Only remove the event when the workflow reliably
receives the updated state before dependent work. Otherwise retain the two events;
do not add a daemon, change-detection cache, or another delivery mode to force removal.

### Simplify installation when it removes operator work

First document one primary supported setup/update route using actual delivery and
trust evidence. Evaluate plugin packaging or a consolidated command family only if
it replaces existing steps. Do not count the internal hook command as a setup choice,
or retire a supported route before its replacement works. Select A-17, A-21/A-23,
A-28/A-29, and real-host cases for that separate increment.

### Design verification compatibility separately from review authoring

For version compatibility, keep `rctl_version` as provenance and consider an explicit
verification protocol version. Define how old reports without that field are read,
which changes invalidate closure, and how incompatible reports request verification.
Documentation, packaging, or host-only releases should not automatically invalidate
scientific checks. This changes current SPEC behavior; select A-03/A-06/A-08/A-09
and A-19, with explicit old-report compatibility fixtures, before implementation.

For review authoring, retain task/revision/criterion binding, reviewer source,
rationale, exact review input, and actual evidence inspection. A later design may
reduce repeated path entry, but must distinguish contract-required evidence from
the author's declared review evidence. Automatically unioning required references
does not establish that they were inspected; repeated manual entry does not prove
inspection either. Keep the existing input schema until that meaning is designed
and A-05/A-06 cover it. The protocol-version change does not depend on this redesign.

### Reorganize remaining tests when their behavior is touched

Group active tests by lifecycle, documents, verification, context, discovery, and
integration as those areas change. Remove an old test only when its distinct failure
is still covered through the supported Interface. Avoid a repository-wide rename
or duplicate suite solely to make the cleanup look complete.

## Sources

Official pages were checked through smart-search on 2026-09-14. The Astra page
supports instruction cleanup and explicit completion conditions; the hooks page
establishes the event contract, not success of a proposed delivery change.

```sh
smart-search search "site:developers.openai.com GPT-6 Astra skills prompts" --format markdown
smart-search fetch "https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra.md" --format markdown
smart-search fetch "https://developers.openai.com/codex/hooks" --format markdown
```

Local baseline: [PRD](PRD.md), [SPEC](SPEC.md), [CLI](CLI.md),
[INTEGRATION](INTEGRATION.md), [ACCEPTANCE](ACCEPTANCE.md),
[review schema](../schemas/reviews.schema.json), and
[M8 verification](M8-VERIFICATION.md), plus the source files linked above.

## Limitations

The first increment has local automated, package, and bounded real-host evidence;
it does not establish a general measured model improvement or deployed release.
Existing host evidence retains its recorded version and scope. The v0.5 release
remains pending. No event retirement,
compatibility migration, shared-skill update, or live project upgrade is included.
