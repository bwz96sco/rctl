---
name: research-ideation
description: Develop alternative ways to answer a clear research question, including methods, measurements, empirical designs and theoretical approaches. Use when the user wants candidate solutions or investigations. Forming or reframing the question belongs to research-question; investment judgment belongs to explicit evaluation.
---

# Research Ideation

Own investigation design. Develop substantively different ways to answer a supplied
or referenced research question. A method may be an algorithm, measurement procedure,
empirical contrast or theoretical approach; a new algorithm is not compulsory. Match
breadth to the request and available material, without a candidate-count or contribution
quota. Hand the unranked portfolio to explicit `$research-idea-evaluation`.

Use a clear user-supplied question directly. A question record, synthesis or earlier
evaluation is not a prerequisite. When the work instead concerns what is worth
studying, use `$research-question`. Ordinary reading reflections stay with their
paper notes. A material reframing during design returns to question formation;
preserve what changed rather than silently substituting a more convenient question.

## Workspace

Read the project-relative `vault` binding in `.rctl/project.json`; when unbound, retain the project's existing note convention. Reuse an existing idea directory; for a new one use `<vault>/ideas/<topic-slug>/`, or `artifacts/research-ideation/<topic-slug>/` without a note root. Write `ideas.md` with `ideas-template.md`.

## Workflow

1. **Establish the question being answered.** Record the active user request and the supplied question, with a source link or `Q#` when available. Preserve its object, scope and requested perspective, including corrections to inherited metrics or methods. State a reasonable bounded interpretation when sufficient; use `$research-question` if the question itself needs development. Do not make a clear question repeat upstream stages.
2. **Use the available material directly.** Accept papers and anchored reading notes, imported methods, datasets, experimental observations, prior results, and human suggestions. No source type is mandatory or privileged. Reuse historical idea or seed files as suggestions; return to their underlying sources before treating a premise as factual evidence.
3. **Develop alternative approaches.** Vary the causal operation, information source, representation, comparison or proof strategy where this changes what can be learned. For explanatory work, turn rival accounts into distinguishable predictions; for measurement, develop ways to observe the relevant distinction; for performance, specify why an operation could address the bottleneck. Existing methods may be sufficient instruments. Compare materially different approaches before committing to machinery; merge cosmetic variants.
4. **Check premises and revise.** Separate reported facts, interpretations, and proposed contributions. Check a decisive source passage when its meaning affects the candidate; an unchecked premise stays uncertain. For a method, explain its operation and where the needed information comes from. For a measurement or explanation, explain the relevant distinction and how it could be independently observed. Route needed searches to `$paper-discovery` and full-paper checks to `$research-literature`; rough generation needs no prerequisite literature campaign.
5. **Build the portfolio.** Write stable `C1..Cn` cards using the template: parent question, potential contribution and reader consequence, evidence, proposed investigation, closest prior or rival, first discriminating observation, and major uncertainty. Several approaches can answer one question. If the user supplied several questions, preserve those associations. Before handoff, explain the substantive alternatives considered and any narrowing from the request. A shortlist limit governs developed cards, not the alternatives considered. Known instruments do not make their combination novel.
6. **Hand off the full portfolio.** Set `stage: expand_complete` and `next_owner: research-idea-evaluation`. Run `uv run --no-project python "<evaluation-skill>/scripts/validate-handoff.py" portfolio <idea-root>` using the actual installed evaluation-skill directory. This checks structure, not scientific merit. For an ideation-only request, name the explicit evaluation invocation and stop. If the user already explicitly included evaluation in the work, continue within that scope without another selection ceremony; the handoff grants no experiment budget.

Complete when the unranked portfolio preserves the question and explains how the
proposed approaches could answer it, their differences from relevant alternatives,
and their decisive uncertainties. Available artifacts and a runnable contrast establish
feasibility, not scientific value. If no approach can be formulated, report the missing
capability in the existing work. This does not itself refute the question's value.
A validated portfolio is still unevaluated until substantive evaluation occurs.

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
