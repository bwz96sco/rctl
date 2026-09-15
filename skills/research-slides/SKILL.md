---
name: research-slides
description: Plan, produce, audit, or hand off evidence-grounded academic talks and slide decks. Use for paper-reading decks, lab meetings, thesis defenses, seminars, conference talks, speaker notes, and slide audits.
---

# Research Slides

Turn research evidence into a bounded academic talk: contract first, one message per slide, render then inspect.

## Workflow

1. **Lock the requested output.** Plan/handoff, speaker notes, audit, or deck production/revision; then audience, goal, talk type, time and slide budget, language, anonymity constraints, and evidence boundaries. Perform only the phases needed for that output.
2. **Inspect evidence and existing decks.** Papers, validated claims, writing and experiment artifacts, prior deck files, and project slide tooling before drafting. Missing evidence narrows the claim or routes back to its owner.
3. **Outline when planning or producing.** One main message per slide, with source basis, time budget, and asset need. Catalog exact paper figures, tables, and equations before any visual generation; never paste manuscript paragraphs onto slides.
4. **Produce only when requested.** Project-local slide tooling first when it owns the output; otherwise locate the installed `personal-slides` skill and read its `references/research-handoff-contract.md`. Apply it as a bounded internal production phase while this skill remains the evidence owner. Preserve exact scientific assets — figures, tables, equations, logos — unaltered. An audit inspects the existing deck and reports findings without editing it.
5. **Render and audit.** Render the actual deck and inspect every slide: claim support, anonymity, asset fidelity, readability at projector scale, placeholders, timing. No render, no visual QA claim. Speaker notes and spoken claims stay inside the same evidence bounds.

Complete against the requested output:

- **Plan/handoff:** deliver the evidence-grounded outline, timing, asset needs, and unresolved production inputs. A rendered deck is not required.
- **Speaker notes:** deliver notes tied to the supplied slides and evidence; an unchanged deck need not be rebuilt.
- **Audit:** deliver findings tied to the existing slides and actual renders where available; mark uninspected visual properties as unassessed.
- **Produce/revise:** deliver the requested deck with supported messages, preserved exact assets, and an audit of every actual rendered slide, or state the concrete blocker.

## Rules

- Slide control artifacts: read the project-relative `vault` binding in `.rctl/project.json`, otherwise retain the existing note convention. Reuse existing work; for a new note use `<vault>/slides/<topic-slug>/`, or `artifacts/research-slides/<topic-slug>/` without a note root. Deck outputs go to the project slide directory.
- Route figure creation to `research-figure`, claim boundaries to `research-experiment` and `research-writing`, paper-reading context to `research-literature`; `ppt-master` only as an explicit specialty route.
- Never invent numbers, citations, claims, affiliations, or renders.
