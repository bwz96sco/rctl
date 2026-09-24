---
name: research-writing
description: Plan, write, and revise author-side research manuscripts from validated evidence. Use for paper arguments and outlines, paper-wide figure and table planning, section or LaTeX drafting, substantive revision, claim and citation audits, reviewer responses, rebuttals, and submission checks. Referee-side audits belong to research-review-case.
---

# Research Writing

Turn validated literature, experiment, and theory evidence into a coherent paper argument and the requested manuscript surface. Every claim stays inside its evidence; missing evidence narrows the claim, routes back to its owner, or blocks visibly.

## Workflow

1. **Lock the surface.** Read the supplied files, the paper repo, and current evidence before asking. Identify the paper type, audience, applicable venue constraints, and exact requested output — outline, draft, build, audit, revision, or rebuttal. Produce only that output.
2. **Establish the evidence boundary.** Which claims, numbers, equations, citations, figures, and reviewer statements are authoritative — from the literature register and notes, experiment artifacts, and theory proofs.
3. **Organize the requested work.** For an outline, full draft, or structural revision, use the [paper argument](#paper-argument) and [manuscript modules](#manuscript-modules). Place the main claims and their supporting sources in the relevant outline entries; keep missing support explicit. Read [figure-planning.md](references/figure-planning.md) when selecting or reorganizing the paper's figures and tables, drafting with placeholders, or integrating displays with the surrounding argument. For a local edit, inspect the affected argument and reuse the existing structure. Planning ends at the requested outline; drafting proceeds when requested.
4. **Draft, revise, or audit.** Preserve claims, numbers, equations, notation, citations, and qualifiers unless the requested revision and evidence support a change; make material changes explicit. For an audit, report findings without modifying manuscript files. For a rebuttal, map each reviewer issue to evidence, manuscript delta, and response delta. Read [academic-phrasebank.md](references/academic-phrasebank.md) when calibrating wording or rewriting Chinese into English.
5. **Validate the affected surface.** Verify claim strength, numbers, equations, citation support, display references, and logic. Check that the title, abstract, introduction, and conclusion agree with the supported contribution wherever the change affects them. After changing buildable LaTeX source, or when a build/submission check is requested, run the project build and record its actual command, result, and warnings. A read-only claim/prose audit needs no build; a standalone fragment without project context may be delivered as unbuilt.

Complete when the requested output is delivered or explicitly blocked, affected claims remain evidence-bound, technical content is preserved or deliberately changed, and missing evidence is visible.

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
| Support — Theoretical or Experimental | Present the proof or evaluation that answers the paper's claims, with assumptions, relevant comparisons, results, and uncertainty. Separate observed results from their interpretation. |
| Discussion | Interpret the findings in relation to the question and prior work; examine strengths, weaknesses, implications, and evidence-grounded future work. |
| Conclusion | Answer the original question with the supported contribution and its scope; introduce no new evidence or stronger claims. |
| References | Provide accurate, traceable bibliographic records for the sources cited in the manuscript. |

Keep detailed section guidance in `references/`, linked from its module row with a clear read condition. The shared wording resource remains separate from section-specific guidance.

## Rules

- Never invent claims, citations, experiments, figures, proofs, reviewer statements, or successful builds.
- No prose polish that makes an unsupported claim sound stronger; AI-style impressions never become authorship or integrity verdicts.
- No workflow state, ports, or prompt text in manuscript prose.
- Reuse the existing outline and notes. A writing request does not require a separate argument document or a complete set of section files.
- Writing artifacts: read the project-relative `vault` binding in `.rctl/project.json`, otherwise retain the existing note convention. Reuse existing work; for a new note use `<vault>/writing/<topic-slug>/`, or `artifacts/research-writing/<topic-slug>/` without a note root. LaTeX lives in the paper repo.
- `paper-search-cli` validates DOIs, arXiv IDs, and BibTeX; `zotero-cli` for library ops; `smart-search-cli` for venue rules and non-paper facts; referee-side audits route to `research-review-case`.
