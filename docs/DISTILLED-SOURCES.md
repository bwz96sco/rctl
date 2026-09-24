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

## Limitations

The linked web texts were read through smart-search and the browser; the supplied
reading guide was read locally. Example images were not individually audited, and
the example papers' reported results were not independently verified. The OR
retrospective is user-supplied evidence; its underlying project files and experiments
were not independently re-audited for this change. These entries record guidance
provenance and adaptation; they do not establish how reliably an agent will follow
the resulting instructions.
