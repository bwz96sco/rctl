---
name: research-ideation
description: Develop mechanism-distinct, falsifiable research candidates from questions, paper evidence, methods, datasets, experimental observations, or human ideas. Use when asked to develop research directions or candidate methods, with breadth matched to the request. Hands the unranked candidates to explicit evaluation.
---

# Research Ideation

Own candidate development. Match breadth to the question, available material, and user request; there is no default candidate count or lens quota. Hand the resulting unranked portfolio to the explicit `$research-idea-evaluation` skill. Screening, human shortlisting, deep attacks, and winner selection belong to evaluation. Ordinary reading and exploratory reflection stay with the work that prompted them.

## Workspace

Read the project-relative `vault` binding in `.rctl/project.json`; when unbound, retain the project's existing note convention. Reuse an existing idea directory; for a new one use `<vault>/ideas/<topic-slug>/`, or `artifacts/research-ideation/<topic-slug>/` without a note root. Write `ideas.md` with `ideas-template.md`.

## Workflow

1. **Freeze the frame.** Record the target question verbatim, constraints, non-goals, and supplied interests.
2. **Use the available material directly.** Accept papers and anchored reading notes, imported methods, datasets, experimental observations, prior results, and human suggestions. No source type is mandatory or privileged. Reuse historical idea or seed files as suggestions; return to their underlying sources before treating a premise as factual evidence.
3. **Expand independently.** Generate initial routes before inspecting closest-prior evidence in detail. Use problem-first, method-first, dataset-first, and mixed combinations supported by the supplied inputs.
4. **Check premises and revise.** Separate reported facts, interpretations, and proposed mechanisms. Check a decisive source passage when its meaning affects the candidate; an unchecked premise stays uncertain. Ask whether the proposed operation could affect the cited problem and where its required information comes from. Revise routes using the evidence. Route needed paper searches to `$paper-discovery` and full-paper checks to `$research-literature`, without making a literature campaign a prerequisite for rough generation.
5. **Build the portfolio.** Write stable `C1..Cn` cards for the requested breadth. Each needs a research hook, source combination, mechanism, expected claim, cheapest falsification test, kill condition, and major uncertainty. Merge only true duplicates. Keep distinct mechanisms separate and unranked.
6. **Hand off the full portfolio.** Set `stage: expand_complete` and `next_owner: research-idea-evaluation`. Do not ask the human to choose among unevaluated candidates.
7. **Validate the handoff.** Locate the installed `research-idea-evaluation` directory from the host's skill path; `<evaluation-skill>` below means that actual directory, not a fixed user-level location. Run `uv run --no-project python "<evaluation-skill>/scripts/validate-handoff.py" portfolio <idea-root>`. Running this structural helper does not invoke evaluation. After it passes, name the exact explicit invocation `$research-idea-evaluation` for portfolio-wide screening and stop.

Complete when `ideas.md` contains the unranked candidates developed within the requested scope, their source basis is visible, and the validated portfolio is waiting for explicit evaluation. If no candidate can yet be formulated, report the unresolved problem or premise in the existing work and stop without creating an empty evaluation handoff.

## Expansion prompts

When useful, consider replacing a method at an observed bottleneck, changing a
component, adding information available in use, transferring to a different
scientific difficulty, stressing a reachable condition, or changing a metric
that affects the conclusion. Apply only prompts that help the question; they
require no per-paper coverage table. Preserve distinct mechanisms rather than
cosmetic variants.

## Rules

- Unknown novelty stays unknown until evaluation.
- Distinguish the source observation from the candidate's causal hypothesis. A paper citation supports only what the cited passage establishes.
- Do not require checkpoints, readiness pilots, synthesis, or literature files before generation.
- Reject hidden compute, information leakage, unfair baselines, and cosmetic renaming during construction; leave comparative scientific judgment to evaluation.
- Do not invent exact performance targets without a prior result, operational requirement, or pilot basis.
- Name the key unestablished capability in the major uncertainty. If the method needs a reliable target, correct component, or diagnosis, explain how it would obtain one; assuming it is supplied bounds the claim to using that information.
- When known, name the closest prior as an arm in the candidate's falsification test and state `runnable`, `reimplemented`, or `blocked`. Otherwise record `unknown` and the missing comparison; evaluation owns verification of the closest prior and its feasibility. A test the closest prior would also pass does not isolate the candidate. Do not invent a prior to complete a card.
- Link the sources actually used by candidates. Explain a discarded premise when its correction changes the proposal; unused material needs no coverage ledger.
