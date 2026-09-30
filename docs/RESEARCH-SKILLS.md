# Research skills

rctl owns the 16 research workflow packages listed below under `skills/`, including
research-task, the migrated domain workflows, and research-rapid-test. Edit these
sources here.
As of 2026-09-29, `research-question` and `research-ideation` remain source
packages but are uninstalled from this user's shared skill directory. Their source
descriptions and earlier installation records below are retained for reference.
The duplicate ideation links under `~/.gemini/config/skills/` and
`~/.claude/skills/` are also removed; Antigravity's directory aliases follow the
shared removal. Retained skills no longer route to either removed entrypoint.
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
| [research-literature](../skills/research-literature/SKILL.md) | Full-paper reading, anchored notes, criticism and exploratory reflection | Automatic or explicit |
| [research-synthesis](../skills/research-synthesis/SKILL.md) | Evidence-bounded answers and comparisons across papers | Automatic or explicit |
| [research-question](../skills/research-question/SKILL.md) | Research-question formation from observations, goals, contradictions and technical capabilities | Source retained; uninstalled locally |
| [research-ideation](../skills/research-ideation/SKILL.md) | Alternative methods and investigations answering a clear research question | Source retained; uninstalled locally |
| [research-idea-evaluation](../skills/research-idea-evaluation/SKILL.md) | Question-value assessment and investigation investment judgment | Explicit only |
| [research-rapid-test](../skills/research-rapid-test/SKILL.md) | Bounded observations resolving an empirical investment uncertainty | Automatic or explicit |
| [research-experiment](../skills/research-experiment/SKILL.md) | Bounded experiment contracts, runner evidence and scientific checks | Automatic or explicit |
| [experiment-adapter-builder](../skills/experiment-adapter-builder/SKILL.md) | Stable project runner commands, queues, monitoring and evidence rules | Explicit only in Codex; native policy preserved |
| [model-training-workflow](../skills/model-training-workflow/SKILL.md) | Training setup, launch guards, monitoring, diagnosis and experiment handoff | Explicit only in Codex; native policy preserved |
| [research-theory](../skills/research-theory/SKILL.md) | Formulation, derivation, proofs, counterexamples and proof audits | Automatic or explicit |
| [research-figure](../skills/research-figure/SKILL.md) | Evidence-bearing figures, diagrams and caption audits | Automatic or explicit |
| [research-slides](../skills/research-slides/SKILL.md) | Academic talk planning, production boundaries and slide audits | Automatic or explicit |
| [research-writing](../skills/research-writing/SKILL.md) | Author-side manuscripts, revisions, rebuttals and submission checks | Automatic or explicit |
| [research-review-case](../skills/research-review-case/SKILL.md) | Referee-side evidence audits without paper verdicts | Automatic or explicit |

Remaining names and invocation policies are preserved. Research-idea-evaluation
remains explicit-only. The two training/adapter packages also retain
`allow_implicit_invocation: false` in their Codex metadata; their frontmatter retains
its original automatic-discovery default for other hosts.

## Reading and candidate development

The standalone `research-opportunity-mining` skill was retired on 2026-09-24.
Reading now includes independent thinking and exploratory reflection in the same
paper note, whose [template](../skills/research-literature/note-template.md) sections follow the reading order.
Synthesis can retain tentative connections separately from its evidence-backed
answer. Reading can serve an exploratory purpose without requiring an already
precise new research question.

Research-question develops worthwhile, scoped questions through optional routes
for failures, successes, contradictions, scenario/assumption changes, measurement
ambiguity and technical capabilities. It can finish with question statements before
methods or experiment counts exist. It uses an existing record or `questions.md`
when durable development is requested; ordinary reflections stay in their notes.

Ideation develops ways to answer a clear supplied or referenced question, including
algorithms, measurements, empirical designs and theoretical approaches. Direct entry
does not require an upstream question file, synthesis or evaluation. Evaluation can
assess a question in its existing record without requiring a solution portfolio;
investigation decisions retain their existing `C#` format and validator. These are
separate responsibilities, not mandatory consecutive stages.

There is no default candidate count, lens quota or per-paper coverage table. The
former mining lenses remain optional prompts; the retired gap/seed-collection
workflow is not restored. Historical seed files remain suggestions whose factual
premises need their underlying sources. Live research notes are not migrated.

## Shared computation checks

The standalone `research-computation` skill was retired on 2026-09-23. Its useful
execution and numerical-validity guidance now lives in the shared
[computation checks](../skills/research-theory/references/computation-checks.md)
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

The source migration redirected 15 shared links to this checkout's `skills/<name>/`.
The remaining workflows retain their discovery paths under
`~/.agents/skills/`; Antigravity projections through that shared directory continue
to use the same sources. Editing the checkout updates these linked packages; a
wheel installation alone does not update them. New installations can use the host's
normal skill installer against the individual repository paths. Do not create a
second global research-task copy alongside the project-local one.

The shared computation reference is packaged with research-theory. Copy-based
installations using that reference need research-theory beside the consuming
package under the same skills root. The local installation below removes the
obsolete research-computation and research-opportunity-mining discovery links;
source retirement alone does not remove installed links.

Research-rapid-test retains its existing Codex discovery path at
`~/.codex/skills/research-rapid-test`, now a symlink to this checkout's package.
This follow-up preserves its Codex-only installation; no duplicate is added under
`~/.agents/skills` and no other host installation is introduced.

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
user-level path. For candidate-origin result validation, install research-experiment
and research-idea-evaluation as sibling packages under the same skills root; the
former's validator calls the latter's handoff validator. Supplied/problem-origin
experiments do not need that peer package. An absent peer produces an actionable
error, not an automatic installation. The official skill page was re-fetched through
smart-search on 2026-09-14 for this path-only integration follow-up.

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

The [bounded use-check record](../.work/question-skill-split-20260928/review.md)
contains four initial SWE-2 High responses and three repeats after one focused
revision. Question-only completion, direct ideation and old-format handoffs work
in these examples. Scientific reasoning remains mixed: unsupported capability
claims, overattribution and prerequisite-first prioritization still occur. This
records implementation and its observed limits, not improved research quality.
The [project implementation record](../../OR/research/plans/2026-09-28-research-question-skill-split.md#implementation-record)
keeps the scope and completion judgment alongside the original authorization.

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

In particular, research-slides resolves personal-slides through its installed skill
location before reading `references/research-handoff-contract.md`; the two source
directories no longer need to be siblings. External CLI availability, credentials,
datasets, and model access are not supplied by moving a skill.

## Durable artifact contracts

Workflows use compact Markdown artifacts. Historical distillation tables remain in
agent-skills-private; their old pack paths are not runtime contracts.

| Local owner | Current durable surface | Mechanical gate |
|---|---|---|
| `paper-discovery` | one repository-level Zotero collection and `zotero-collection.md`; question-scoped `register.md` following the packaged register template, with publication/affiliation provenance, search coverage, Zotero item keys and verified membership | workflow contract tests plus Zotero re-read after writes |
| `research-literature` | reading-state updates in `register.md`, plus `notes/<paper-id>.md` tied to the version read and source provenance, with evidence-quality assessment and useful analyst reflection | workflow contract tests |
| `research-synthesis` | `synthesis.md`, with optional evidence-backed open problems and separately labelled exploratory reflection | workflow contract tests |
| `research-question` | question statements in chat or an existing topic record; `questions.md` for new durable development | source/resource checks and scoped use checks; no mandatory question-state validator |
| `research-ideation` | one unranked `ideas.md` portfolio of approaches, with an inline or referenced parent question | packaged `research-idea-evaluation/scripts/validate-handoff.py` (`portfolio`) |
| `research-idea-evaluation` | question assessment in its existing record; investigation assessment in compact `decision.md`, with historical staged records retained | solution portfolios use the packaged handoff validator (`decision`, historical `screening`/`shortlist`); question-only assessments do not require those artifacts |
| `research-rapid-test` | one `rapid-test.md`, minimal runnable code/commands and raw observations; in an rctl-managed project, a linked lightweight native task unless the user chooses note-only tracking | claim-appropriate evidence and bounded PROMOTE / ITERATE ONCE / DROP judgment; managed tasks use existing rctl verification/closure with small declared criteria, without formal experiment prerequisites |
| `research-experiment` | rctl `contract.md`, runner-owned execution evidence, and native `result.md` | domain structure/lineage validator plus rctl execution checks and evidence-based reviews before guarded closure |
| `experiment-adapter-builder` | project-local experiment adapter with runner references and reusable run/campaign templates | packaged adapter validator and synthetic fixture; structure only |
| `model-training-workflow` | training plan, source map, preflight, run matrix, execution log, optional diagnosis and handoff | packaged training validator and synthetic fixtures; structure only |
| `research-theory` | derivations, proofs, counterexamples, and supporting numerical checks in the existing artifact | proof status in the skill; numerical validity checked separately |
| `research-figure`, `research-slides`, `research-writing` | requested plan, notes, audit, asset, deck, or manuscript surface | render/build checks only for the applicable requested operation |
| `research-review-case` | anchored case findings plus optional `cases.md` | finding and no-verdict rules in the skill |
| `rctl init` and project-local `research-task` | missing project scaffold, optional vault association, workspace/migration guidance | rctl initializer tests and installed-wheel walkthrough in the rctl repository |

Human-readable state is required. There is no suite-wide requirement for a separate HTML report, provenance hash, manifest, numbered evidence pack, registry, queue, or campaign wrapper; selected runner/training workflows retain their own evidence requirements. Write only the surface requested by the user or needed for durable continuation.

For new durable notes, use the project-relative `vault` binding in `.rctl/project.json`;
when unbound, retain the existing note convention, then use the skill's artifact
fallback if none exists. Continue existing topic artifacts instead of moving or
duplicating them to fit a directory example. Computation checks normally remain in
their calling task or trial rather than creating a separate note.

Question formation develops the inquiry; ideation develops `C#` approaches to a
clear question, separating observations from hypotheses and identifying the next
consequential uncertainty.
Methods, measurements, and explanations are examples, not mandatory portfolio slots.
Evaluation triages the whole portfolio, records actual human choice or an agent
recommendation, obtains independent criticism for potential investments, and makes
the affirmative case for at most two next investigations or closes blocked.

Candidate breadth follows the question, material, and user request. If no candidate
can yet be formulated, record the unresolved premise in the existing work without
creating an empty evaluation handoff. An unknown closest prior remains explicit
until evaluation. New evaluations use `decision_format: compact`; selection and
review provenance live in the decision rather than requiring repeated invocation
and shortlist documents. Screening-only requests can still use `screening.md`.
Historical decisions without the format marker retain their staged contract and
are not silently migrated. The validator checks coverage, nonempty required
sections, review/selection IDs, and downstream lineage, not scientific quality or
execution authority.

Selected decisions route to research-rapid-test for a bounded empirical observation,
research-experiment for formal validation, or research-theory for a derivation/proof.
Both `Investigation Brief` and historical `Experiment Brief` headings are supported.
A later formal experiment retains the original candidate selection even when a
pilot intervened. Evaluation's explicit-only invocation policy is preserved;
continuing an explicitly delegated workflow needs no repeated ID-selection ceremony.

Existing numbered packs, campaign roots, and HTML reports remain readable historical inputs. Deleted pack validators and report commands are not current interfaces and must not be recommended for new work.

## Validation and maintenance

Run the affected skill tests with uv. The normal suite covers native invocation
policy, packaged resources, domain handoffs and result lineage; installed-wheel
smoke exercises the packaged research-experiment templates and validator through
actual rctl verification and negative closure. Structural checks do not establish
scientific validity or prove that every workflow has been exercised by a model.

```sh
uv run pytest tests/test_skill_assets.py tests/test_research_skill_contracts.py tests/test_research_handoffs.py tests/test_training_skill_assets.py -q
uv run scripts/check_docs.py
uv build
uv run scripts/smoke_package.py dist/rctl-0.5.1-py3-none-any.whl
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
