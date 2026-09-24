# Paper Figure and Table Planning

Plan which figures and tables the paper needs, where they belong, and how they work with the text. Reuse the current outline and manuscript. `research-figure` handles the design, production, and inspection of individual figures and their panels.

## Select displays from the argument

Start from the paper's question and intended contributions, distinguishing established claims from hypotheses. Identify what a reader needs to understand or assess, then choose a figure, table, or prose. Figures can reveal structure, relationships, and patterns; tables support precise comparisons; simple facts may need only a sentence. Keep displays that have a clear job in the argument.

Use these roles as a menu, combining or omitting them as appropriate to the paper:

| Role | Reader question | Typical location |
|---|---|---|
| Motivation / teaser | What problem, observation, or limitation motivates the work, and what is the proposed insight? | Near the opening or in the Introduction. |
| Method or construction | What are the components, inputs, outputs, and relationships, and where is the contribution? | Method, Contribution, or benchmark construction. |
| Prior-work comparison | How does this work relate to the closest work on relevant, verified dimensions? | Related Work or benchmark introduction. |
| Main results | What evidence supports the central claim, under which comparison conditions? | Results; a table often suits multiple methods, datasets, and exact metrics. |
| Analysis or limitations | What explains the findings, when do they hold or fail, and what trade-offs remain? | Analysis or Discussion; secondary detail may go in an appendix. |

Keep displays needed to follow the central argument in the main paper, within venue constraints; place supporting detail in the appendix. Select comparisons for their relevance to the question; preserve neutral and unfavorable findings. A diagram explaining an idea does not establish its effectiveness, and broader benchmark coverage does not by itself establish superiority.

## Record a brief in the existing outline

For each planned display, record the following in a short paragraph or bullets. Reuse existing information and include only details relevant to the task; no separate registry or brief file is required.

- **Label and role:** use a stable identifier such as `fig:method-overview` or `tab:main-results`; let the manuscript determine numbering.
- **Reader question and message:** state what the reader should understand. When results are pending, record the question to answer rather than an anticipated favorable conclusion.
- **Content and sources:** identify necessary elements and relationships, or comparisons and metrics, with links to the actual evidence or method description. State what is available and what is missing. Leave detailed panel layout and visual encoding to figure production.
- **Placement:** identify the section, first textual reference, and main-paper or appendix location. Note size constraints when known; settle exact pagination during layout.
- **Text relationship:** specify how the preceding text introduces the display and how the following text interprets its significance and limits. Keep shared terminology consistent with the manuscript.
- **Caption draft:** provide the core sentence or a link to the manuscript caption, with information still needed.

## Develop the caption with the text

Draft the caption's core sentence before drawing. With available evidence, it may state a bounded observation. With missing results, describe the comparison or question. Add enough context for the figure or table and its caption to be understood together: what is displayed, relevant conditions, how to read it, and the supported takeaway and scope.

The caption explains the local display. The surrounding prose explains why it matters to the paper's question, relates it to other evidence, and develops the interpretation. Avoid repeating the caption sentence by sentence in the body.

Keep the canonical caption in the paper source. During production, `research-figure` completes and checks technical details against the actual display and evidence. Writing maintains its relationship to the argument and updates affected prose when the finished display changes the interpretation.

## Draft with placeholders

When drafting is requested, place a clearly marked placeholder in the manuscript's native figure or table environment, with a stable label and caption draft. In LaTeX, use a compilable box or table structure instead of referencing a nonexistent image file. Preserve the label and logical insertion point when the real asset arrives.

Treat evidence availability and asset completion separately:

- **Evidence available, asset unfinished:** write results and interpretation from the retained evidence; the placeholder reserves their display.
- **Evidence pending:** write the question, method, comparison design, and surrounding structure. Mark result-dependent sentences, numerical entries, and caption conclusions as pending in visible editorial notes or draft placeholders. Continue the parts that do not depend on those results.

Use placeholders to reserve content, not to simulate evidence with invented numbers or trends. Keep editorial notes distinguishable from manuscript prose. A draft can be delivered with explicit unresolved items; a submission-ready manuscript must replace or remove its placeholders and resolve the associated claims. Apply the main skill's build rules after changing buildable source; a successful build establishes neither completed figure inspection nor evidential support.

## Handoff and check the paper

For production, pass the existing brief, source links, manuscript location, and caption draft to `research-figure`. On return, integrate the actual asset and caption, preserve labels, and reconcile the surrounding claims with any reported mismatches. Let the evidence change the plan when necessary.

For whole-paper planning or integration, skim the title, abstract, planned or completed displays, and captions together. Check whether they communicate the question, contribution, evidence, and scope; remove needless repetition and expose missing support. Each retained display should have a textual reference and a clear interpretive role. For local work, check only the affected connections.

Keep plotting tools, detailed layout, colors, arrows, and decorative choices in figure production. Any shared terminology or visual meaning needed across the paper belongs in the brief. Plan uncertainty displays when the analysis supports them, rather than adding statistical content to fill space.
