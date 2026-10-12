# Research skills

rctl owns the seven research workflow entrypoints listed below under `skills/`.
Edit these sources here. Specialized guidance, optional templates and helper
fixtures live with their owning entrypoint rather than registering extra skills.
On 2026-10-12, `research-question`, `research-ideation` and
`research-idea-evaluation` were removed from source and from every installed
skill directory ([record](#october12-ideation-retirement)); the research playbook
now supplies candidate moves and the Gate 0 review. Earlier installation records
below that mention them are history.
The [migration record](RESEARCH-SKILLS-MIGRATION.md) records the source snapshot,
preserved uncommitted changes, checks, and installed-link cutover.
The subsequent [review follow-up](RESEARCH-SKILLS-FOLLOWUP.md) records the authorized
workflow fixes and distinguishes mechanical checks from independent skill-use trials.
Source material and adaptation decisions for new workflow guidance are recorded in
[Distilled Sources](DISTILLED-SOURCES.md). Keep skill references focused on the
instructions needed to perform their tasks.

## Managed workflows

| Skill | Responsibility | Invocation |
|---|---|---|
| [research-task](../skills/research-task/SKILL.md) | Task agreements, handoffs, verification and guarded closure | Automatic or explicit; project-local |
| [paper-discovery](../skills/paper-discovery/SKILL.md) | Question-scoped paper pools and project Zotero collection curation | Automatic or explicit |
| [research-literature](../skills/research-literature/SKILL.md) | Anchored full-paper records and evidence-bounded cross-paper answers | Automatic or explicit |
| [research-experiment](../skills/research-experiment/SKILL.md) | Experiments, pilots and training, with project runner documentation | Automatic or explicit |
| [research-figure](../skills/research-figure/SKILL.md) | Evidence-bearing figures, diagrams and caption audits | Automatic or explicit |
| [research-slides](../skills/research-slides/SKILL.md) | Academic talk planning and scientific content verification | Automatic or explicit |
| [research-writing](../skills/research-writing/SKILL.md) | Manuscripts, rebuttals, submission audits and mathematical claim checks | Automatic or explicit |

The seven retained entrypoints keep their names and automatic/explicit invocation
policies. The two former explicit-only training/adapter entrypoints are retired;
their references are loaded through the experiment skill when relevant.

## Consolidation, 12 October 2026

After the first boundary revision, the user requested a necessity review before
further rewriting, then authorized consolidation. Keep an independent entrypoint
when it supplies a distinct task contract or recurring domain verification; use a
reference for a specialization that shares its owner's inputs and completion.
This reduces 13 entrypoints to seven without deleting the useful domain guidance.

| Retired entrypoint | Current owner and guidance |
| --- | --- |
| `research-rapid-test` | research-experiment: [rapid tests](../skills/research-experiment/references/rapid-tests.md) |
| `model-training-workflow` | research-experiment: [training](../skills/research-experiment/references/training.md) |
| `experiment-adapter-builder` | research-experiment: [project adapters](../skills/research-experiment/references/project-adapters.md) |
| `research-synthesis` | research-literature: [cross-paper synthesis](../skills/research-literature/references/synthesis.md) |
| `research-theory` | research-writing: [mathematical claims](../skills/research-writing/references/theory.md) |
| `research-review-case` | research-writing: [manuscript audits](../skills/research-writing/references/manuscript-audit.md) |

Research-slides remains: audience, talk purpose, timing and evidence-grounded
academic narration are a useful domain contract. An available
`presentations:Presentations` skill can produce and render the requested deck;
its implementation responsibilities do not replace academic talk planning.
Research-figure retains individual figure/caption provenance and verification;
paper-wide figure planning stays with writing. Existing project-specific runner
adapters remain useful and are not retired by this source consolidation.

Optional adapter/training templates, validators and fixtures now ship under
research-experiment. The fictional demo uses `entrypoint.md`, staged as `SKILL.md`
only in a temporary validator fixture, so recursive discovery sees only the seven
real entrypoints. The obsolete external source-catalog audit and its controller
are removed from the skill payload; commit `cdd09a5` retains their history. The
preceding uncommitted draft is backed up under
`.work/skill-consolidation-20261012/` in this checkout.

Contracts retain evidence, budgets and any agreed review requirements. Methods,
tool selection and iteration order follow the assignment. The paper-record format,
rctl CLI, schemas and task lifecycle are unchanged. This is a repository source
revision; global discovery links and copy installations are not migrated. Sources
are recorded in [Distilled Sources](DISTILLED-SOURCES.md#skill-necessity-and-consolidation-12-october-2026),
validation in [Development](DEVELOPMENT.md#skill-consolidation-12-october-2026),
and installation/behavioral limits in [Readiness](READINESS.md#limitations).

## Contract and verification revision, 12 October 2026

The first boundary-focused draft changed seven entrypoints: training, adapter
creation, rapid-test, experiment, discovery, reading and synthesis. They establish
the requested input/scope, evidence and completion conditions while leaving
methods, batching, tool choice and iteration order to the assignment.
The [source and adaptation record](DISTILLED-SOURCES.md#skill-contract-and-verification-boundaries-12-october-2026)
records the user request and official guidance behind the revision.

Training no longer requires six pack files or an external source-catalog mapping.
Tiny/capped runs become prerequisites only through the current agreement.
Adapters may keep facts inline or link to existing project documents instead of
creating a fixed reference/template tree. Rapid-test budgets and retries follow
the bet. Discovery chooses routes for coverage; reading chooses its reader
configuration; synthesis can use supplied anchored sources. The compact paper
record format, all 13 names and invocation policies were preserved in that draft.
The consolidation above supersedes its entrypoint layout.

Optional templates retain domain examples. The training-pack helper checks a
completed handoff and run references, reusing an execution log when present; the
adapter helper checks entrypoint metadata and declared local references. These
checks establish structure, not successful execution or scientific validity.
Task guidance also places evidence generation before read-only verification;
required independent/operator review still follows the accepted agreement.

At that stage, source-linked installations saw the edits through existing links.
No global CLI installation, host configuration or live-project skill copy is
updated by this revision. Validation is recorded in
[Development](DEVELOPMENT.md#skill-boundary-revision-12-october-2026), with
behavioral limits in [Readiness](READINESS.md#limitations).

## Reading and candidate development

The standalone `research-opportunity-mining` skill was retired on 2026-09-24.
Since 2026-10-10, reading produces one compact
[record file](../skills/research-literature/note-template.md) per paper for agents
to cite: typed one-line records (setting, result, null, verbatim limitation, defect,
test, relation, lead), each with an anchor, evidence basis and confidence. It has no
overview, field-map, method-narrative or reflection prose; field maps belong to
synthesis, and ideas raised by reading stay as `test` or `lead` records. Synthesis
can retain tentative connections separately from its evidence-backed answer.
Reading can serve an exploratory purpose without requiring an already precise new
research question.

Question formation, approach development and investment judgment have no
dedicated skills. The research playbook (`research-playbook/story-construction.md`
and `checklist.md`) supplies candidate moves, stage decisions and the Gate 0 review;
rctl tasks govern the resulting work. Ideas noticed while reading stay as `test` or
`lead` records.

There is no default candidate count, lens quota or per-paper coverage table; the
retired gap/seed-collection workflow is not restored. Historical seed files,
`ideas.md` portfolios and `decision.md` records remain readable history whose
factual premises need their underlying sources. Live research notes are not
migrated.

## Shared computation checks

The standalone `research-computation` skill was retired on 2026-09-23. Its useful
execution and numerical-validity guidance now lives in the shared
[computation checks](../skills/research-experiment/references/computation-checks.md)
reference. Theory, experiment, rapid-test, and training workflows read it only for
an unresolved computation question. Reading it does not invoke the theory workflow.

Numerical counterexamples stay with theory; experiment and trial owners interpret
their results; project runners own execution and monitoring. A small standalone
calculation can be answered directly. Existing computation notes remain usable,
and checks normally stay in their calling task or trial without a new report.

## Source, packaging and installation

The wheel and source distribution include all these skill packages. Project `init`,
`doctor`, `update export`, and `integration codex export` continue to manage only
`research-task`; they do not install or overwrite a global research suite. Domain
skills remain separate from the CLI's lifecycle and acceptance authority.

The original source migration redirected 15 shared links to this checkout's
`skills/<name>/`. Surviving source-linked packages expose later edits; a wheel
installation alone does not update global discovery. The consolidation does not
remove links to retired source directories or migrate copy-based installations.
New installations can use the host's normal skill installer against the seven
current repository paths. Do not create a second global research-task copy
alongside the project-local one.

The shared computation reference is packaged with research-experiment. Copy-based
installations using it from writing's mathematical guidance need research-experiment
beside research-writing under the same skills root. The historical installation
below removes the
obsolete research-computation and research-opportunity-mining discovery links;
source retirement alone does not remove installed links.

Before consolidation, research-rapid-test retained its Codex discovery path at
`~/.codex/skills/research-rapid-test`, linked to this checkout's former package.
That follow-up preserved its Codex-only installation. Its standalone source
entrypoint is now retired; this change does not alter host installation paths.

The [official Codex skill documentation](https://developers.openai.com/codex/skills)
states that user skills are discovered under `~/.agents/skills` and symlinked skill
folders are followed. This was fetched through smart-search on 2026-09-14. The
migration changes source ownership, not hook configuration or trust. The same page
was re-fetched on 2026-09-21 for the training/adapter follow-up, confirming symlink
discovery and the meaning of `allow_implicit_invocation: false`.
It was re-fetched through smart-search on 2026-09-23 for the computation retirement
and on 2026-09-24 for the reading/ideation change:
a skill requires `SKILL.md`; references are supporting files, and symlink targets
are followed during discovery.
The September28 question-skill split rechecked the same official page through
smart-search: shared user skills, symlink following and explicit-only invocation
remain supported. The new `~/.agents/skills/research-question` link points to this
checkout's `skills/research-question/`; the five edited existing packages retain
their source links and invocation policies.

Invoke packaged helpers from the actual installed skill directory, not a fixed
user-level path. The research-experiment result validator needs no peer package.

### Local shared installation

On 2026-09-24, the user authorized committing and installing the accumulated skill
changes. Source commit `452ed0e2fa0f5f9f477b8e6871f71e815988e946` contains the
writing references, figure ownership changes, shared computation checks, and
reading/ideation simplification. The installation retains the existing local
source-link arrangement: 13 workflows under `~/.agents/skills/` and
research-rapid-test under `~/.codex/skills/`.

Removed the computation and opportunity-mining links from `~/.agents/skills/`
and `~/.gemini/config/skills/`, four physical links in total. The existing
`~/.gemini/antigravity/skills/` and `~/.gemini/antigravity-cli/skills/` root aliases
follow the shared directory, so their retired entries disappear with it.

Installation checks confirmed all 14 user-level skills resolve to the committed
sources, all 103 installed files match source, and all 14 entrypoint resource
links resolve. The 13 shared workflows also resolve through all three existing
Antigravity paths. Both retired names are absent from all five checked discovery
roots, and no global research-task copy was introduced. Removed link targets and
the verification output are retained in `.work/skills-installation-20260924/`.

This updates shared skill discovery and resources. The installed rctl CLI remains
the previously released 0.5.1 wheel; live-project copies and task records were not
changed. Source, package, and installation checks do not establish research quality
or fresh-host agent adherence.

### September28 question-skill split

The new question package is installed through the shared source link described
above. Six relevant installed paths, resource links and invocation policies were
checked. The focused suite passes 70 tests and 49 subtests, and a returned ideation
portfolio passes the unchanged handoff validator.

The bounded use-check record (`.work/question-skill-split-20260928/review.md`)
contains four initial SWE-2 High responses and three repeats after one focused
revision. Question-only completion, direct ideation and old-format handoffs work
in these examples. Scientific reasoning remains mixed: unsupported capability
claims, overattribution and prerequisite-first prioritization still occur. This
records implementation and its observed limits, not improved research quality.
The project implementation record
(`OR/research/plans/2026-09-28-research-question-skill-split.md#implementation-record`)
keeps the scope and completion judgment alongside the original authorization.
These paths identify an untracked local capture and a sibling project's record;
their availability is described in [Distilled Sources](DISTILLED-SOURCES.md#limitations).

Commit `4f72f6e` preserves this first implementation. The subsequent authorized
adjustment turns premise checking into a final source-to-inference check and
separates question value from next-step order in evaluation. A preference for an
inexpensive audit is a judgment to examine, not by itself a factual defect. Source
contradictions and unsupported inferences remain distinct from disagreements over
reader value. The installed source links also expose these later working edits.
Follow-up validation again passes 70 tests and 49 subtests, the documentation
check (344 local links, 100 JSON files, four schemas) and diff whitespace checks.
All three adjusted entrypoints resolve through their installed source links.
No new behavioral comparison was run; the proposed reasoning benefit remains
untested.

### September30 Claude link repair

The user authorized repairing `~/.claude/skills/`. Its 17 research-related links
still pointed to the former agent-skills-private package paths and no longer
resolved. The 12 skills installed under `~/.agents/skills/` now link to this
checkout's packages; the five links for retired research-computation,
research-opportunity-mining, research-project-setup, research-quest and
research-quest-admin are removed. Research-ideation, research-question,
research-rapid-test and research-task are not added, preserving the
installation scope above. All 12 links resolve, their entrypoint names match
and their local resource links exist; no broken link remains in that directory.
Before/after link lists and the check output are in
`.work/claude-skill-links-20260930/`.

### October12 ideation retirement

The user asked whether the ideation skills still had a use now that rctl controls
research state and the research playbook supplies ideas, and chose to retire all
three. The research-question, research-ideation and research-idea-evaluation source
packages are removed; the last commit containing them is `2727853`. The remaining
discovery links to research-idea-evaluation under `~/.agents/skills/`,
`~/.claude/skills/` and `~/.gemini/config/skills/` are removed; no link to the other
two remained. Research-experiment drops the `candidate` origin and `--decision`
option, which needed the evaluation package's validator; no rctl-era task contract
used that origin. Research-rapid-test and research-synthesis no longer route to
evaluation. The evaluation attack review, the one step without a playbook
equivalent, became item 9 of the playbook's "Before Gate 0" checklist
(`research-playbook` commit `36192b2`). Coverage and sources are recorded in
[Distilled Sources](DISTILLED-SOURCES.md#ideation-retirement-12-october-2026).
The packaged 0.6.5 wheel still contains the three packages until a later release;
shared installations follow the source links.

## Related skills outside this migration

The original selection covered 13 private-repository workflows, followed by
research-rapid-test. The 2026-09-21 follow-up adds experiment-adapter-builder and
model-training-workflow because they own research execution workflows. Ownership
follows responsibility, not a research-* name prefix. Auxiliary skills remain in
agent-skills-private: paper-search-cli, zotero-cli, slurm-hpc-runner, autofigure-edit,
personal-slides, and upscayl-paper. General helpers such as smart-search-cli, obsidian-cli, nlm-skill,
and oracle-cli also retain their existing ownership.

Other relevant installed skills are not sourced from that repository:

- `paper-search` and `or-llm-agent`: separate packages under `~/.agents/skills/`.
- `matt:research` and the host-provided Deep Research skill: separate general
  research/documentation capabilities, not members of this workflow migration.

Research-slides previously required personal-slides. It now uses project tooling
or an available presentation-production skill for the requested artifact; its
academic planning and content checks remain local. External CLI availability, credentials,
datasets, and model access are not supplied by moving a skill.

## Durable artifact contracts

Workflows use compact Markdown artifacts. Historical distillation tables remain in
agent-skills-private; their old pack paths are not runtime contracts.

| Local owner | Current durable surface | Mechanical gate |
|---|---|---|
| `paper-discovery` | one repository-level Zotero collection and `zotero-collection.md`; question-scoped `register.md` following the packaged register template, with publication provenance (affiliations when relevant), search coverage, Zotero item keys and verified membership | workflow contract tests plus Zotero re-read after writes |
| `research-literature` | version-specific anchored paper records cited as `<paper-id>#R<n>`; cross-paper assignments produce `synthesis.md` or the requested answer, with tentative connections labelled separately | workflow contract tests; source-to-claim inspection |
| `research-experiment` | requested pilot/training/experiment evidence; native `contract.md` and `result.md` for managed work; optional reusable project adapters | experiment validator and declared rctl checks for managed experiments; adapter/training helpers check structure only; scientific judgment remains separate |
| `research-writing` | requested manuscript, rebuttal, proof or anchored audit findings; retain proved/refuted/not_proved/blocked proof status | source-to-claim and proof inspection; build checks for affected typeset output; audit findings do not issue an unsolicited paper verdict |
| `research-figure` | requested evidence-bearing asset, caption or figure audit | inspect rendered output, labels, sources and caption consistency |
| `research-slides` | requested academic talk plan, notes, deck or content audit | audience/time/evidence checks; actual renders for produced decks |
| `rctl init` and project-local `research-task` | missing project scaffold, optional vault association, workspace/migration guidance | rctl initializer tests and installed-wheel walkthrough in the rctl repository |

Human-readable state is required. There is no suite-wide requirement for a separate HTML report, provenance hash, manifest, numbered evidence pack, registry, queue, or campaign wrapper; selected runner/training workflows retain their own evidence requirements. Write only the surface requested by the user or needed for durable continuation.

For new durable notes, use the project-relative `vault` binding in `.rctl/project.json`;
when unbound, retain the existing note convention, then use the skill's artifact
fallback if none exists. Continue existing topic artifacts instead of moving or
duplicating them to fit a directory example. Computation checks normally remain in
their calling task or trial rather than creating a separate note.

Existing numbered packs, campaign roots, and HTML reports remain readable historical inputs. Deleted pack validators and report commands are not current interfaces and must not be recommended for new work.

## Validation and maintenance

Run the affected skill tests with uv. The normal suite covers native invocation
policy, packaged resources and experiment result structure; installed-wheel
smoke exercises the packaged research-experiment templates and validator through
actual rctl verification and negative closure. Structural checks do not establish
scientific validity or prove that every workflow has been exercised by a model.

```sh
uv run --locked pytest tests/test_skill_assets.py tests/test_research_skill_contracts.py tests/test_experiment_result.py tests/test_training_skill_assets.py -q
uv run --locked python scripts/check_docs.py
uv build
uv run --locked python scripts/smoke_package.py dist/rctl-0.6.5-py3-none-any.whl
```

### Behavioral checks

Choose the check from the claim being made; a passing result at one level does not
establish the next. Use the existing change record for requests, material scope,
outputs, judgments and limits rather than creating a suite-wide scoring system.

| Check | Setup and supported conclusion |
| --- | --- |
| Package compatibility | Asset, policy, resource and handoff checks establish structural compatibility. |
| Workflow use | Give the host a natural request and paths to real, bounded materials; let it select the skill and load relevant resources. Allow the source-reading and verification tools that the workflow actually needs, within the task's side-effect scope. Inspect resource reads and the delivered artifact. A test with skill bodies injected into the prompt establishes supplied-instruction use, not automatic discovery. |
| Substantive reasoning | Compare the consequential factual claims and inferences with sources. Separately judge whether the questions preserve the requested perspective and explain what answering them would teach beyond known work. Cite concrete defects or reader-value reasons; low cost, an audit design or lack of a new algorithm is not itself a negative result. |
| Comparative improvement | Compare the declared old and new versions on the same requests, materials, model, tools and resource allowance. Include materials not used to edit the skill and repeats when response variation matters. Review outputs with version labels hidden where practical, preserving reviewer identity, reasons and disagreements. Same-case correction checks alone do not establish a version benefit. |

Keep synthetic scenarios for isolated boundary checks. Real-material checks also
exercise ambiguity, source retrieval and closest-prior reasoning. Set the call/time
allowance and what the observations could change before starting. A small comparison
can reveal a specific improvement or regression; broader reliability and research
productivity claims need evidence at that scale. Returning plausible questions is
distinct from establishing their novelty, value or eventual publication outcome.

Historical distillation and model-evaluation campaigns remain in agent-skills-private.
They are historical evidence, not the authority for the current packaged workflows.
