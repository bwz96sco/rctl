---
name: research-ideation
description: Develop research questions and candidate contributions from evidence, anomalies, methods, resources, or human ideas. Use when exploring research directions, including methods, measurements, and explanations. Hands unranked candidates to explicit investment evaluation.
---

# Research Ideation

Own candidate development. Match breadth to the question, available material, and user request; there is no default candidate count or contribution-type quota. Develop questions worth answering and ways to answer them. Hand the unranked portfolio to explicit `$research-idea-evaluation`; comparative investment judgment belongs there. Ordinary reading and exploratory reflection stay with the work that prompted them.

## Workspace

Read the project-relative `vault` binding in `.rctl/project.json`; when unbound, retain the project's existing note convention. Reuse an existing idea directory; for a new one use `<vault>/ideas/<topic-slug>/`, or `artifacts/research-ideation/<topic-slug>/` without a note root. Write `ideas.md` with `ideas-template.md`.

## Workflow

1. **Frame the inquiry.** Record the active user question verbatim and its requested perspective, including corrections to an earlier goal. Distinguish that request from the project's inherited default metric or method. When the user asks to expand research objects or measures, develop those objects and what existing measures conflate before proposing interventions. A past failure can motivate this inquiry; it does not determine its scope.
2. **Use the available material directly.** Accept papers and anchored reading notes, imported methods, datasets, experimental observations, prior results, and human suggestions. No source type is mandatory or privileged. Reuse historical idea or seed files as suggestions; return to their underlying sources before treating a premise as factual evidence.
3. **Expand questions and explanations.** Use problem-first, method-first, dataset-first, or mixed entry points. An unexplained contrast, a missing observable, a theoretical boundary, or an operational difficulty can motivate a candidate. Sketch competing explanations before committing to machinery. A candidate may contribute a method, measurement, finding, or formulation; these are examples, not slots to fill.
4. **Check premises and revise.** Separate reported facts, interpretations, and proposed contributions. Check a decisive source passage when its meaning affects the candidate; an unchecked premise stays uncertain. For a method, explain its operation and where the needed information comes from. For a measurement or explanation, explain the relevant distinction and how it could be independently observed. Route needed searches to `$paper-discovery` and full-paper checks to `$research-literature`; rough generation needs no prerequisite literature campaign.
5. **Build the portfolio.** Write stable `C1..Cn` cards using the template: question, potential contribution and reader consequence, evidence, proposed investigation, closest prior or rival, first discriminating observation, and major uncertainty. Keep distinct questions, hypotheses, observables, and mechanisms separate; merge cosmetic variants. Before handoff, compare the portfolio with the requested perspective: briefly explain the substantive alternatives considered and any narrowing. A shortlist limit governs developed cards, not which research objects may be considered. Known methods may be useful instruments without making their combination novel.
6. **Hand off the full portfolio.** Set `stage: expand_complete` and `next_owner: research-idea-evaluation`. Run `uv run --no-project python "<evaluation-skill>/scripts/validate-handoff.py" portfolio <idea-root>` using the actual installed evaluation-skill directory. This checks structure, not scientific merit. For an ideation-only request, name the explicit evaluation invocation and stop. If the user already explicitly included evaluation in the work, continue within that scope without another selection ceremony; the handoff grants no experiment budget.

Complete when the unranked portfolio addresses the requested scope and exposes what could be learned beyond existing knowledge, why it could matter, and which premise remains uncertain. Available artifacts and a runnable contrast establish feasibility, not this completion criterion. If no candidate can be formulated, report the unresolved question in the existing work rather than creating an empty portfolio. A validated portfolio is still unevaluated until substantive evaluation occurs.

## Expansion prompts

Ask what current observations conflate, which competing explanations predict
different outcomes, what changes over a process or resource budget, or which
important condition existing evidence does not cover. A method change is useful
when it follows from such a question. A new metric needs a defined construct,
independent validity evidence, and a consequential use. Apply only prompts that
help the inquiry; no per-paper coverage table is needed.

## Rules

- Unknown novelty stays unknown until evaluation.
- Distinguish the source observation from the candidate's hypothesis. A paper citation supports only what the cited passage establishes.
- Do not require checkpoints, readiness pilots, synthesis, or literature files before generation.
- Reject hidden compute, information leakage, unfair baselines, and cosmetic renaming during construction; leave comparative scientific judgment to evaluation.
- Do not invent exact performance targets without a prior result, operational requirement, or pilot basis.
- Name the key unestablished premise or capability in the major uncertainty. If several capabilities are uncertain, identify the one whose resolution most changes investment. Supplying a correct target, component, or diagnosis tests conditional use, not its automatic production.
- Match falsification and continuation conditions to the claim. A tie on final performance does not reject an independently declared measurement question; a favorable secondary measure does not replace a failed primary claim. Distinguish a scientific kill condition from absent opportunity or insufficient information.
- Name the closest prior or strongest rival when known, and the observation that could distinguish it. For an executable comparison, state `runnable`, `reimplemented`, `blocked`, or `unknown`. Otherwise identify the prior claim or alternative explanation. Evaluation owns verification; unknown novelty stays unknown.
- Link the sources actually used by candidates. Explain a discarded premise when its correction changes the proposal; unused material needs no coverage ledger.
