---
name: research-ideation
description: Expand a research question into a broad unranked portfolio of mechanism-distinct, falsifiable ideas from problems, paper opportunities, imported methods, datasets, observations, or human interests. Hands the full portfolio to explicit evaluation.
---

# Research Ideation

Own expansion. For broad exploration, default to roughly 12–20 distinct candidates; honor a user-specified smaller scope or count. Hand the full requested portfolio to the explicit `$research-idea-evaluation` skill. Screening, human shortlisting, deep attacks, and winner selection belong to evaluation.

## Workspace

Read the project-relative `vault` binding in `.rctl/project.json`; when unbound, retain the project's existing note convention. Reuse an existing idea directory; for a new one use `<vault>/ideas/<topic-slug>/`, or `artifacts/research-ideation/<topic-slug>/` without a note root. Write `ideas.md` with `ideas-template.md`.

## Workflow

1. **Freeze the frame.** Record the target question verbatim, constraints, non-goals, and supplied interests.
2. **Inventory available seeds.** Accept any mixture of paper problems, `opportunity-seeds.md`, imported methods, datasets, observations, prior null results, and human suggestions. No source type is mandatory or privileged.
3. **Expand independently.** Generate initial routes before inspecting closest-prior evidence in detail. Use problem-first, method-first, dataset-first, and mixed combinations supported by the supplied inputs.
4. **Reopen with evidence.** Inspect available literature and seed artifacts, then add or materially revise routes suggested by their mechanisms and boundaries. Route a required new paper search to `$paper-discovery` and full-paper evidence checks to `$research-literature`, without making either a prerequisite for rough generation.
5. **Build the portfolio.** Write stable `C1..Cn` cards for the requested breadth. Each needs a research hook, source combination, mechanism, expected claim, cheapest falsification test, kill condition, and major uncertainty. Merge only true duplicates. Keep distinct mechanisms separate and unranked.
6. **Hand off the full portfolio.** Set `stage: expand_complete` and `next_owner: research-idea-evaluation`. Do not ask the human to choose among unevaluated candidates.
7. **Validate the handoff.** Locate the installed `research-idea-evaluation` directory from the host's skill path; `<evaluation-skill>` below means that actual directory, not a fixed user-level location. Run `uv run --no-project python "<evaluation-skill>/scripts/validate-handoff.py" portfolio <idea-root>`. Running this structural helper does not invoke evaluation. After it passes, name the exact explicit invocation `$research-idea-evaluation` for portfolio-wide screening and stop.

Complete when `ideas.md` contains the requested unranked portfolio, the source inventory is visible, and the validated portfolio is waiting for explicit evaluation.

## Rules

- Unknown novelty stays unknown until evaluation.
- A problem, method, dataset, or opportunity seed is input evidence, not a candidate by itself.
- Do not require checkpoints, readiness pilots, synthesis, or literature files before generation.
- Reject hidden compute, information leakage, unfair baselines, and cosmetic renaming during construction; leave comparative scientific judgment to evaluation.
- Do not invent exact performance targets without a prior result, operational requirement, or pilot basis.
- For broad exploration, aim for at least four lenses with no single lens dominating roughly one third of the portfolio. A user-specified narrow scope overrides these diversity targets.
- When known, name the closest prior as an arm in the candidate's falsification test and state `runnable`, `reimplemented`, or `blocked`. Otherwise record `unknown` and the missing comparison; evaluation owns verification of the closest prior and its feasibility. A test the closest prior would also pass does not isolate the candidate. Do not invent a prior to complete a card.
- Enter one source-inventory row per distinct source item, not one row per file; record an unused part as `declined: <reason>`.
