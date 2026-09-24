---
name: research-figure
description: Create, revise, audit, or integrate individual research figures and captions from traceable sources. Use for paper or slide plots, diagrams, reproducible rendering, and figure or caption audits. Whole-paper figure planning belongs to research-writing.
---

# Research Figure

Turn traceable evidence into a bounded display: every value, arrow, and caption claim comes from source data or evidence — never invented.

Work at the level of a figure and its panels. `research-writing` owns paper-wide figure selection, narrative roles, planned manuscript locations, and draft placeholders.

## Workflow

1. **Establish the figure brief.** Use a supplied writing brief or the user's direct request to identify the operation (create, revise, audit, integrate), reader question, planned content, source evidence or method description, target surface (paper or slide), size, and format. Read surrounding text and a caption draft when available. A diagram may explain a structure or process without establishing an empirical result. A paper plan or separate brief file is not a prerequisite. For an audit, inspect the supplied asset and available provenance and deliver findings; production steps apply only when creation or changes are requested.
2. **Design the figure and choose the production route.** Choose panels, visual encodings, layout, and hierarchy that answer the reader question. Project plotting and LaTeX scripts take precedence; then matplotlib, SVG, TikZ, or Mermaid whenever exact labels, data, topology, or geometry can be expressed directly. Route AI illustration or style transfer to `autofigure-edit`, result-data boundaries to `research-experiment`.
3. **Build from source data.** Plots and tables come from the actual data files, with the reproducible generation script kept next to the asset. Diagrams come from an editable source or structured spec. For paired or blocked comparisons keep pairing IDs; state `n`, units, center/spread, and metric definitions.
4. **Inspect the render.** Script success or valid format never establishes visual correctness. Check readability at target scale, clipping, labels, hierarchy, and fidelity to source values. No render, no inspection claim.
5. **Complete and check the caption.** Start from the supplied draft when present. Explain what is shown, what to notice, the supported takeaway, and scope limits. Check panel labels, visual encodings, units, metric definitions, sample counts, and error bars or intervals as applicable against the actual figure and sources. A caption adds no claim the evidence does not support.

## Completion and writing handoff

An audit completes with evidence-anchored findings and explicitly uncheckable items; missing generation sources limit reproducibility claims, not permission to rebuild or edit the asset. Creation or revision completes with the requested asset, source and claim boundaries, a reproducible generation route, and inspection of the actual render. For caption-only or integration work, deliver and check the affected surface without regenerating an unchanged figure. Standalone figure work can deliver a complete caption directly.

For manuscript work, keep the canonical caption in the paper source; provide proposed replacement text when editing is outside the request. Figure work owns its factual agreement with the display; `research-writing` owns its relationship to the surrounding argument. When integration is requested, use the planned manuscript slot and preserve the existing figure label when replacing a placeholder.

Compare the finished figure and caption with the supplied brief and surrounding text. Report unsupported intended takeaways or other mismatches with the relevant evidence and suggested wording changes. Return asset/source locations and checks actually performed; hand broader narrative or figure-plan changes back to `research-writing`. The observed evidence governs this handoff, including neutral or unfavorable results.

## Rules

- Durable figure work: read the project-relative `vault` binding in `.rctl/project.json`, otherwise retain the existing note convention. Reuse existing work; for a new note use `<vault>/figures/<slug>/`, or `artifacts/research-figure/<slug>/` without a note root. Final assets live in the paper repo.
- Prefer vector for plots and formal diagrams; raster only for photos, screenshots, or generated imagery.
- Failed renders and failed checks stay visible; never hide them with design.
