# Research skills

rctl owns the 15 research workflow packages listed below under `skills/`, including
research-task, the migrated domain workflows, and research-rapid-test. Edit these
sources here.
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
| [research-ideation](../skills/research-ideation/SKILL.md) | Unranked, falsifiable research candidates at the requested scope | Automatic or explicit |
| [research-idea-evaluation](../skills/research-idea-evaluation/SKILL.md) | Screening, human shortlisting and independent deep evaluation | Explicit only |
| [research-rapid-test](../skills/research-rapid-test/SKILL.md) | Fast empirical pilots and bounded promote-or-drop decisions before formal experiments | Automatic or explicit |
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
paper note, guided by the [reading method](../skills/research-literature/references/reading-method.md).
Synthesis can retain tentative connections separately from its evidence-backed
answer. Developing complete research candidates belongs to research-ideation.

Ideation uses papers, anchored notes, experimental observations, and human ideas
directly. It has no default candidate count, lens quota, or per-paper coverage
table. The former mining lenses survive as optional thinking prompts. Historical
seed files remain usable as suggestions; premises used as evidence must be checked
against their underlying sources. No separate seed artifact is required, and live
research notes are not migrated by this source change.

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
package under the same skills root. Remove obsolete research-computation and
research-opportunity-mining discovery links during a shared-installation update;
source retirement alone does not remove those links.

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

Invoke packaged helpers from the actual installed skill directory, not a fixed
user-level path. For candidate-origin result validation, install research-experiment
and research-idea-evaluation as sibling packages under the same skills root; the
former's validator calls the latter's handoff validator. Supplied/problem-origin
experiments do not need that peer package. An absent peer produces an actionable
error, not an automatic installation. The official skill page was re-fetched through
smart-search on 2026-09-14 for this path-only integration follow-up.

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
| `research-ideation` | one full unranked `ideas.md` portfolio | packaged `research-idea-evaluation/scripts/validate-handoff.py` (`portfolio`) |
| `research-idea-evaluation` | `screening.md`, human-confirmed `shortlist.md`, `attacks/<candidate-id>.md`, `decision.md` | packaged `research-idea-evaluation/scripts/validate-handoff.py` (`screening`, `shortlist`, `decision`) |
| `research-rapid-test` | one `rapid-test.md`, minimal runnable code/commands and raw comparisons; in an rctl-managed project, a linked lightweight native task unless the user chooses note-only tracking | observed intervention/control evidence and bounded PROMOTE / ITERATE ONCE / DROP judgment; managed tasks use existing rctl verification/closure with small declared criteria, without formal experiment prerequisites |
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

Ideation develops `C#` candidates from the supplied material, distinguishing factual premises from hypotheses and naming missing capabilities. Evaluation first screens every candidate with bounded evidence, then preserves the human's informed selection verbatim in `shortlist.md`. Independent deep evaluation attacks exactly that shortlist and selects no more than two candidates or closes blocked. The packaged validator enforces portfolio and screening coverage, shortlist lineage, attack scope, dispositions, selection bounds, and method-experiment provenance.

Candidate breadth follows the question, material, and user request. If no candidate
can yet be formulated, record the unresolved premise in the existing work without
creating an empty evaluation handoff. An unknown closest prior remains explicit
until evaluation. The human shortlist may contain any nonempty explicit selection; 3–5 is
advice, not a validation limit. Selected evaluation results route to research-rapid-test
for early feasibility or research-experiment for formal validation. A later formal
experiment retains the original candidate selection even when a pilot intervened.
Human selection and evaluation's explicit-only invocation policy are unchanged.

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

Historical distillation and model-evaluation campaigns remain in agent-skills-private.
They are historical evidence, not the authority for the current packaged workflows.
