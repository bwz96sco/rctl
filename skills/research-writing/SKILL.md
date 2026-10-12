---
name: research-writing
description: Write or revise research manuscripts and rebuttals, formulate or verify mathematical claims, and audit submissions against evidence.
---

# Research Writing

Develop the requested manuscript, rebuttal, proof or audit from traceable evidence.
Every claim stays inside its evidence; missing support narrows the claim, routes
back to its owner, or blocks visibly.

## Starting contract

Establish the requested surface and role: outline, draft, revision, rebuttal,
submission check, mathematical formulation/proof or referee-side audit. Use supplied
files and project evidence to identify applicable paper type, audience, venue
constraints and authoritative claims,
numbers, equations, citations and reviewer statements. Reuse existing structure
for a local edit; a new outline or separate argument document is optional.

For whole-paper planning, use the [paper argument](#paper-argument) and relevant
[manuscript modules](#manuscript-modules). Use [figure planning](references/figure-planning.md)
when selecting/reorganizing displays or working with placeholders. An outline
request ends with an outline; drafting and deck production follow their own scope.

- A referee-side audit uses [manuscript audit guidance](references/manuscript-audit.md),
  returns findings and preserves the source. Authoring/repair is a separate request.
- A load-bearing mathematical claim uses [proof checks](references/theory.md) when
  formulation, derivation or proof validity is part of the work.
- Wording calibration or Chinese-to-English revision can use
  [academic phrasebank](references/academic-phrasebank.md).

## Completion and verification

Check affected claims, numbers, equations, citation support, display references
and logic against evidence. Preserve technical content and qualifiers unless an
explicit change is supported; report material changes. Check agreement among the
title, abstract, introduction and conclusion when the edit affects their contribution.
For a rebuttal, connect each addressed reviewer issue to evidence and the actual
manuscript/response changes.

After editing buildable LaTeX or for a requested build/submission check, run the
project build and report its actual command, result and warnings. Read-only audits
need no build; a standalone fragment may be delivered as unbuilt. Complete when
the requested output is delivered or explicitly blocked, affected claims stay
evidence-bound and missing support is visible. Managed closure uses research-task.

## Paper argument

For whole-paper planning, connect these questions into an argument. Reuse the answers already established in the project; unresolved points remain visible in the outline.

1. **Why does problem X matter?** Identify the scientific or practical stakes and who or what is affected.
2. **What have A, B, and C established?** Organize relevant prior work by its answers, approaches, and evidence, including the closest work.
3. **What remains unresolved?** Identify a supported limitation, scope boundary, or unanswered question. Describe prior work fairly; a new contribution need not imply that earlier work is defective.
4. **What does D contribute?** State the central idea and concrete contribution: a method, observation, benchmark, analysis, theory, or another appropriate form.
5. **Why could D address that gap?** Explain the mechanism or reasoning. Distinguish the rationale from an advantage already demonstrated by evidence.
6. **What supports D?** Connect claims to theoretical or experimental support. Claims of empirical advantage need relevant comparisons against A, B, and C under stated conditions, including neutral or unfavorable findings. Other paper types need evidence suited to their contribution.
7. **Where is D strong, and where does it fall short?** State demonstrated benefits, trade-offs, assumptions, limitations, and the scope of the conclusion.
8. **What follows from D?** Derive future work from the remaining uncertainty or limitation; keep proposed work distinct from completed results.

## Manuscript modules

Use these responsibilities to organize the outline. Adapt headings, order, and combined or split sections to the paper type, venue, and existing manuscript. The presentation order does not prescribe the drafting order. Consult only module references relevant to the current task as they are added here.

| Module | Responsibility |
|---|---|
| Title | Identify the subject and central contribution at the scope the evidence supports. |
| Abstract | Summarize the problem or gap, contribution, main supported finding, and its bounded significance. Read [abstract.md](references/abstract.md) when drafting, revising, or auditing an abstract. |
| Introduction | Establish importance, situate prior knowledge, expose the gap, and state the paper's answer and contributions. Read [introduction.md](references/introduction.md) when drafting, revising, or auditing an introduction. |
| Related Work | Explain the closest approaches and findings, their relation to the present question, and the supported distinctions from D. Read [related-work.md](references/related-work.md) when drafting, reorganizing, or auditing related work. |
| Contribution — Method, Observation, Benchmark, Analysis, etc. | Explain what D is, its central idea, and the definitions, assumptions, or construction needed to understand it. Choose descriptive section headings for the actual contribution. Read [method.md](references/method.md) when drafting, revising, or auditing a method description. |
| Support — Theoretical or Experimental | Present the proof or evaluation that answers the paper's claims, with assumptions, relevant comparisons, results, and uncertainty. Separate observed results from their interpretation. Read [experiments.md](references/experiments.md) when planning, drafting, revising, or auditing an experimental section. |
| Discussion | Interpret the findings in relation to the question and prior work; examine strengths, weaknesses, implications, and evidence-grounded future work. |
| Conclusion | Answer the original question with the supported contribution and its scope; introduce no new evidence or stronger claims. |
| References | Provide accurate, traceable bibliographic records for the sources cited in the manuscript. Read [bibliography.md](references/bibliography.md) when adding or cleaning bibliographic entries, normalizing citation metadata, or checking the reference list before submission. |

Keep detailed section guidance in `references/`, linked from its module row with a clear read condition. The shared wording resource remains separate from section-specific guidance.

## Rules

- Never invent claims, citations, experiments, figures, proofs, reviewer statements, or successful builds.
- No prose polish that makes an unsupported claim sound stronger; AI-style impressions never become authorship or integrity verdicts.
- No workflow state, ports, or prompt text in manuscript prose.
- Reuse the existing outline and notes. A writing request does not require a separate argument document or a complete set of section files.
- Writing artifacts: read the project-relative `vault` binding in `.rctl/project.json`, otherwise retain the existing note convention. Reuse existing work; for a new note use `<vault>/writing/<topic-slug>/`, or `artifacts/research-writing/<topic-slug>/` without a note root. LaTeX lives in the paper repo.
- Use `paper-search-cli` for identifier/BibTeX checks, `zotero-cli` for library operations, and `smart-search-cli` for venue rules and non-paper facts.
