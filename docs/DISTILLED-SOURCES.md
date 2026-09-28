# Distilled Sources

Record source material used to develop this project's workflow guidance here. Use
this document when reviewing or extending that guidance. Skill references contain
the current operational instructions; source history and adaptation notes belong
in this record.

For each new distillation, retain the source link and read date, the ideas adopted,
the adaptations made, and links to the affected files. Extend this document as
sources are used.

## Paper figure and table planning

- **Source:** [Paper Figure Guide (Chinese)](https://dy8q0bnq8y.feishu.cn/wiki/OGpcw6zaRiQ6OwkNxfYcl7IKnBh).
- **Read:** 2026-09-23.
- **Applied to:** [Figure planning reference](../skills/research-writing/references/figure-planning.md).

**Retained:** plan around the reader's question and a one-sentence figure purpose;
distinguish motivation, method, comparison, result, and analysis roles; keep module
names consistent with the text; use tables when exact main-result comparisons
matter.

**Adapted:** the roles form a menu for paper-wide planning, with figures, tables,
and prose chosen according to their job. Stable placeholder labels, provisional
captions, separate evidence and asset readiness, and the writing/figure handoff
implement the user's drafting workflow. Tool, color, and decoration suggestions
remain optional production choices. Any claimed advantage depends on the evidence,
including neutral or unfavorable findings.

## Abstract writing

- **Source:** [How to Write a Paper: Abstract (Chinese)](https://dy8q0bnq8y.feishu.cn/wiki/Tz2pwvxTyiBK0zkCVszcZmJ3nwd).
- **Read:** 2026-09-23.
- **Applied to:** [Abstract reference](../skills/research-writing/references/abstract.md).

**Retained:** present the abstract as a concise statement of contribution; connect
context, problem, methodology, and results; emphasize the scientific problem and
central idea; select concrete results that answer that problem.

**Adapted:** the source calls its approach the five-sentence principle and lists
four functional components. The reference retains those components with flexible
sentence allocations governed by venue requirements. Structural or mechanistic
problem statements require support. Evidence boundaries, provisional drafting,
and applicability beyond the illustrated method and benchmark papers follow the
writing workflow.

## Introduction writing

- **Source:** [How to Write a Paper: Introduction (Chinese)](https://dy8q0bnq8y.feishu.cn/wiki/ULATwBu2MiLqqRkXxV6c2S7AnPd).
- **Read:** 2026-09-23.
- **Applied to:** [Introduction reference](../skills/research-writing/references/introduction.md).

**Retained:** connect the research area, relevant prior work, a specific unresolved
issue, and this paper's work; explain prior achievements before the gap; give each
paragraph one core point with a topic sentence; make contributions concrete and
verifiable. The suggested four-to-six-paragraph outline includes a contribution
summary and an optional roadmap.

**Adapted:** expand the abstract's argument with context and support rather than
expanding its sentences mechanically. Treat paragraph counts, opening topic
sentences, and two-to-four contribution items as adaptable guidance. Use selective
prior work in the introduction and reserve fuller comparisons for Related Work
where present. Evidence requirements for gap and novelty claims, applicability to
different contribution types, and provisional drafting follow the writing workflow.

## Related Work writing

- **Source:** [How to Write a Paper: Related Work (Chinese)](https://dy8q0bnq8y.feishu.cn/wiki/CLSAwWm6qifjwQkTd82czgMNnYf).
- **Read:** 2026-09-23.
- **Applied to:** [Related Work reference](../skills/research-writing/references/related-work.md).

**Retained:** the opening's core questions about research context, major
approaches, each approach's achievements and remaining gaps, and the present work's
relationship to prior work. Organize by research direction or method category;
synthesize each group through its shared idea, representative work, characteristics,
and relation to the present paper. Distinguish motivation in the introduction from
fuller research positioning. Describe extension, complement, contrast, unification,
or re-evaluation as appropriate. Use comparison tables with relevant, defensible
dimensions rather than features selected only to favor the present work.

**Adapted:** condense the opening questions into a connected purpose statement.
Treat the group structure and relationship types as flexible guidance.
Extend the source's objective tone with explicit support for category-wide and
novelty claims, scope-aware comparisons, and distinctions between unknown and
absent table properties. Provisional drafting and evidence requirements follow
the writing workflow. Table planning reuses the existing figure-planning reference;
the source's phrase examples are not duplicated in this section guide because
wording guidance has a separate shared reference.

## Method writing

- **Source:** [How to Write a Paper: Methods (Chinese)](https://dy8q0bnq8y.feishu.cn/wiki/CtiAwh1eOiqOfCkPKVLc0WsxnZg).
- **Read:** 2026-09-23, including the full rendered text through cmux.
- **Applied to:** [Method reference](../skills/research-writing/references/method.md).

**Retained:** move from overview to formulation, components, optimization, and use;
coordinate the overview with the method figure; define notation before technical
details; explain each component's purpose, inputs, operation, outputs, and rationale.
Equations need motivation, symbol explanations, and a stated role. Pseudocode
complements prose, and concise novelty explanations connect differences from prior
work to their purpose and the consequences of removing a component.

**Adapted:** follow the established Abstract, Introduction, and Related Work
references: state the section's purpose, organize substantive guidance by writing
decision, and finish with a short draft check. Merge overlapping source questions
and omit sentence templates. The outline is a useful default, adapted to the
method. Figure planning and placeholders link to the existing reference; the main
writing skill supplies the evidence boundary for expected and observed effects.

## Experiments writing

- **Source:** the user-supplied `/Users/zhangbowen/Downloads/如何写论文-Experiments.md` (Chinese).
- **Read:** 2026-09-24, in full from the local file.
- **Applied to:** [Experiments reference](../skills/research-writing/references/experiments.md).

**Retained:** choose a contribution-driven structure from setup, main results,
ablation, analysis, cases or visualization, robustness or generalization, and cost.
Describe datasets, baselines, metrics, implementation, training and inference,
repetition, statistics, and fairness. Main results explain the central comparison
and its uneven gains; ablations connect design choices to their measured
contribution; analysis explains behavior across conditions; cases make output
quality, task difficulty, and failures understandable. Direct readers to displays,
select consequential observations, interpret their meaning, and report anomalies.

**Adapted:** use the source's structure as a menu, preserving its warning against
adding experiments merely for volume. Expand the robustness and cost headings only
enough to explain their purpose. Treat ablations as bounded evidence about design
choices rather than automatic proof of a mechanism. Interpret the source's advice
to soften abnormal findings as calibrated uncertainty with explicit consequences,
not minimization of unfavorable results. Existing figure planning owns captions
and placeholders; writing uses retained evidence and does not authorize new runs.

## Bibliography preparation

- **Source:** the user-supplied `/Users/zhangbowen/Downloads/如何写论文-Reference.md` (Chinese).
- **Technical check:** [Overleaf's BibTeX guide](https://www.overleaf.com/learn/latex/Bibliography_management_with_bibtex), retrieved through smart-search; confirms standard entry types and style-dependent field handling.
- **Read:** 2026-09-24, including the full local source.
- **Applied to:** [References guide](../skills/research-writing/references/bibliography.md).

**Retained:** review each imported entry; use a consistent author/year/keyword key
convention; select the correct publication type; check core fields; protect title
acronyms and names; preserve correct author metadata; normalize venue names and
capitalization; verify edition ordinals, volume, issue, and pages; and remove
duplicate works before submission.

**Adapted:** correct the source's `@arcticle` typo to `@article`. Keep working
citation keys unless cleanup calls for renaming. Let the venue style govern field
retention and author-list truncation instead of universally deleting URL or
publisher fields or manually replacing known authors with “et al.” Preserve
proceedings volume information in its appropriate field and use article identifiers
or absent pagination where applicable. Protect necessary title terms while allowing
ordinary style capitalization. Rendered-list checks complement metadata review;
the guide does not assert a single proceedings-name pattern for every conference.

## Computation checks

- **Source:** the former `skills/research-computation/SKILL.md` at rctl commit `3130531`; its earlier role is recorded in the [source register](SOURCES.md).
- **Read:** 2026-09-23.
- **Applied to:** [Shared computation checks](../skills/research-theory/references/computation-checks.md).

**Retained:** bounded execution or inspection; reuse of current evidence; actual
job state separate from output validation; numerical checks selected for the
question; and distinctions between fresh computation, reused or remote execution,
parsed outputs, digitized values, and hypotheses.

**Adapted:** retire the independent skill and its artifact-routing convention.
Keep one shared reference under research-theory for existing workflows to read
directly. Make convergence checks concrete through termination status, residuals,
feasibility tolerances, or optimality gaps where relevant. Standalone calculations
remain direct work, and numerical checks do not introduce a proof or experiment
workflow. Runner, experiment, and theory owners keep their existing responsibilities.

## Reading and research candidate development

- **Sources:** the user-supplied `/Users/zhangbowen/Downloads/如何读论文？.md` (Chinese seven-step reading guidance); the user's OR usage retrospective supplied in the conversation on 2026-09-24; and the former `skills/research-opportunity-mining/SKILL.md`, read before its retirement.
- **Read:** 2026-09-24.
- **Applied to:** [Reading method](../skills/research-literature/references/reading-method.md), [paper note](../skills/research-literature/note-template.md), [synthesis](../skills/research-synthesis/SKILL.md), and [ideation](../skills/research-ideation/SKILL.md).

**Retained:** overview through the abstract and displays; a precise research
question; prior approaches and their remaining difficulties; independent thought
before close method reading; comparison with the authors' approach; critical
analysis of support and selective code reading or reproduction; following needed
background; and reflection beyond extraction. The former mining lenses remain
available as optional prompts for developing candidates.

**Adapted:** translate the suggested reading/thinking time split into space for
reflection rather than a fixed ratio. Keep tentative alternatives in the same
note, distinct from reported facts and supported defects. New paper discovery,
cross-paper synthesis, and experiment execution retain their owners. Retire the
independent mining package, seed template, and lens-coverage requirement. Remove
ideation's default candidate count, diversity quotas, and unused-input ledger;
use existing candidate fields to distinguish source observations, proposed causal
operations, information requirements, and missing capabilities. Historical seeds
are suggestions whose factual premises need their original sources, not another
evidence layer. The OR retrospective motivates these changes without making its
project-specific terminology part of the shared guidance.

## Research questions and investment evaluation

- **Sources:** the user's OR retrospective and requested plan on 2026-09-27; the retained [Pro consultation](../../OR/note/OR-research/ideas/research-ideation-validation-pro-2026-09-27/consultation.md), its exact prompt/response, and the [EoH/BehaveSim interpretation](../../OR/note/OR-research/literature/eoh-behavesim-research-questions-2026-09-27/synthesis.md).
- **Read:** 2026-09-27. These local source links are provenance, not runtime dependencies.
- **Applied to:** ideation, idea evaluation, rapid-test, and their handoff templates/validator.

**Retained:** source checks, honest novelty uncertainty, independent criticism,
fixed comparison identities, private generated evidence for complete methods,
scale reasoning, cumulative allowances, and distinctions between stopping
investment and refuting a scientific claim.

**Adapted:** develop research questions and contributions beyond mandatory method
modifications. Require an affirmative reason for the next expenditure after review,
and match the first observation to the uncertainty and claim. Measurement and
explanatory contributions need independent validity and usefulness, not an
automatic final-performance gate. Keep a compact decision with actual selection
basis rather than repeated human-ID ceremonies. Retain legacy artifact validation
and explicit invocation policy. Pro's advice motivates these changes; it does not
establish that the skill wording caused historical failures or that a proposed
direction is publishable.

**September27 application correction:** the subsequent OR portfolio selected a
conditional diagnosis/repair probe after the user had requested EoH/BehaveSim-like
expansion of research objects and measures. The installed packages already pointed
to the revised source; this was not a stale-installation incident. The original
workflow permitted the desired framing but the generated portfolio narrowed it,
and its independent review ranked only those supplied candidates. Sources are the
[retained decision](../../OR/note/OR-research/ideas/or-paper-claims-2026-09-27/decision.md)
and the user's [scope correction](../../OR/research/plans/2026-09-27-ideation-validation-workflow.md#scope-correction-restore-research-object-and-measurement-expansion).
Sharpen the existing framing/handoff and evaluation steps: preserve the active
request, inspect portfolio scope before ranking, explain what a favorable result
would teach beyond prior work, and connect an affordable prerequisite to a
worthwhile parent question. Give independent reviewers that active request and
permission to return the portfolio for further development. Rapid-test reductions
preserve the selected research object. These are focused instruction changes;
no new schema, lifecycle stage, coverage quota or approval ceremony is introduced.

**Application check:** 69 focused skill/contract/handoff tests and 47 subtests pass;
these validate structure, not research judgment. One clean-context SWE-2 High
[forward-use response](../.work/ideation-scope-forward-20260927/review.md) returned
the narrowed portfolio to development and identified the lost perspective. It
still suggested an optional cheap probe and redundant clarification; these were
not adopted. The [assessment](../.work/ideation-scope-forward-20260927/audit.json)
records the residual problems and inference limit. This single clarified-context
example does not establish a causal improvement or reliable compliance. No new
scientific trial was launched.

## Limitations

The linked web texts were read through smart-search and the browser; the supplied
reading and writing guides were read locally. Example images were not individually
audited, and the example papers' reported results were not independently verified. The OR
retrospective is user-supplied evidence; its underlying project files and experiments
were not independently re-audited for this change. These entries record guidance
provenance and adaptation; they do not establish how reliably an agent will follow
the resulting instructions.
