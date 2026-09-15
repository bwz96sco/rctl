---
name: research-figure
description: Create, revise, audit, or integrate evidence-bearing research figures, plots, diagrams, and captions from traceable sources. Use for paper or slide figures, reproducible plots, figure audits, and caption bounds.
---

# Research Figure

Turn traceable evidence into a bounded display: every value, arrow, and caption claim comes from source data or evidence — never invented.

## Workflow

1. **Lock the contract.** Operation (create, revise, audit, integrate), reader job, the bounded claim the figure carries, source evidence, target surface (paper or slide), and format. For an audit, inspect the supplied asset and available provenance and deliver findings; production steps apply only when creation or changes are requested.
2. **Choose the production route when needed.** Project plotting and LaTeX scripts take precedence; then matplotlib, SVG, TikZ, or Mermaid whenever exact labels, data, topology, or geometry can be expressed directly. Route AI illustration or style transfer to `autofigure-edit`, result-data boundaries to `research-experiment`, narrative to `research-writing`.
3. **Build from source data.** Plots and tables come from the actual data files, with the reproducible generation script kept next to the asset. Diagrams come from an editable source or structured spec. For paired or blocked comparisons keep pairing IDs; state `n`, units, center/spread, and metric definitions.
4. **Inspect the render.** Script success or valid format never establishes visual correctness. Check readability at target scale, clipping, labels, hierarchy, and fidelity to source values. No render, no inspection claim.
5. **Bound the caption.** What is shown, what to notice, the bounded takeaway, scope limits. A caption adds no claim the evidence does not support.

An audit completes with evidence-anchored findings and explicitly uncheckable items; missing generation sources limit reproducibility claims, not permission to rebuild or edit the asset. Creation or revision completes with the requested asset, source and claim boundaries, a reproducible generation route, and inspection of the actual render. For caption-only or integration work, deliver and check the affected surface without regenerating an unchanged figure.

## Rules

- Durable figure work: read the project-relative `vault` binding in `.rctl/project.json`, otherwise retain the existing note convention. Reuse existing work; for a new note use `<vault>/figures/<slug>/`, or `artifacts/research-figure/<slug>/` without a note root. Final assets live in the paper repo.
- Prefer vector for plots and formal diagrams; raster only for photos, screenshots, or generated imagery.
- Failed renders and failed checks stay visible; never hide them with design.
