# Paper note template

You are reading one paper for one target question. Follow the [reading method](references/reading-method.md), then record the evidence needed for the target question. Fill the evidence sections; add analyst reflection when useful. Anchor material claims and numbers to a section, page, figure, table, or equation and record their evidence basis and confidence or caveat. With partial text or an abstract, fill only what the available source supports and mark deeper sections `not assessable from available access`.

The scientific factual sections report only what the paper says. Metadata inherits the supplied provenance; preserve unresolved claims and source dates. Your own judgments and exploratory ideas belong in the `Analyst` sections. Keep author-stated limitations, observed failures, analyst inferences, and proposed mechanisms distinct.

```markdown
# <short-name>

Metadata: <title> / <authors> / <ID of version read>
Provenance: <register entry link, or directly supplied source>
Version read: <arXiv version/date, formal DOI, or supplied PDF identity>
Publication: <established status, venue/year/track; source/date or provenance link; unresolved claims>
Affiliations / research group: <author-to-institution mapping; explicitly sourced group or not established; source/page/date or provenance link>
Zotero key: <item-key / not_registered / unchecked>
Collection membership: <in_project / library_only / not_registered / unchecked; collection and check date/source, or provenance link>
Metadata status: verified | conflicting | unverified — <reason when not verified>
Access: full_pdf | partial_text | abstract_only
Source: <PDF path or URL>

## Research question
What problem is studied and why it matters. (abstract + introduction)

## Gap
What prior work is missing — the stated research gap. (introduction)

## Field map
How the authors categorize related work — the map of the field, not
sentence-by-sentence coverage. (related work)

## Method
Input -> core method -> Module A -> Module B -> Output.
Not "uses Transformer": state what exactly was changed vs prior work.

## Theoretical assumptions
What must hold for the method or claims to work.

## Experiments
- Dataset / scenario:
- Baselines:
- Metrics:
- Protocol / split:
- Sample size / seeds / uncertainty:
- Code / data / weights availability, as stated by the authors:

## Key results
For each result that can affect the target question:
- Claim or finding:
- Comparator:
- Exact value or qualitative result:
- Conditions, robustness, or failure boundary:
- Anchor: section/page/figure/table/equation
- Evidence basis: text | figure | table | equation
- Confidence / caveat:

## Ablations
Which modules are actually load-bearing, by how much.

## Limitations & future work
Author-stated only, with anchors. If absent after a full-text check, write
`not found after full-text check: <sections checked>`; with weaker access, write
`not assessable from available access`.

## Application scenario
Where this applies in practice, per the paper.

## Analyst: evidence-backed defects
For each material defect:
- Defect:
- Evidence: section/page/table/result
- Evidence basis: text | figure | table | equation
- Why it matters:
- Author acknowledged it: yes | no
- Status: observed failure | analyst inference
- Confidence / caveat:

Inspect unsupported conclusions, weak or missing baselines, missing ablations,
unrealistic assumptions, narrow datasets, leakage, metrics that hide failure,
and discrepancies between claims and results. Do not manufacture a fixed number
of defects. Report `no material defect established from this paper` when evidence
does not support one. Diagnose this paper's evidence without claiming that a defect
remains globally open. Keep possible improvements in the reflection below.

## Analyst: relation to target question
Your judgment: supports / limits / contradicts / direct overlap /
closest_candidate / mechanism neighbor / irrelevant. State why, the affected
part of the target question, and confidence. `closest_candidate` marks a plausible
neighbor; final closest-prior selection belongs to `$research-synthesis`.

Evidence quality for this question: briefly state the strongest support, the main
limitation, and what the paper cannot establish, linking the anchored results or
defects above. Consider applicable proof assumptions, metric validity, baseline
strength and resource comparability, evaluation scope and uncertainty, and claimed
versus checked resource availability. Distinguish access to released materials
from successful reproduction; runtime qualification belongs to later experiments.
Ground this judgment in the paper's evidence rather than venue or team reputation.
With insufficient access, state `not assessable from available access`.

## Analyst: reflection (when useful)
Briefly record your own approach to the problem and how it compares with the
authors' method, what the paper changed in your understanding, and questions or
alternatives worth pursuing. Link the observation behind an idea and distinguish
the proposed operation and expected effect from established findings. Name the
key assumption or capability still missing, including how any required information
would be obtained. A useful reflection may simply clarify a question; no improvement
idea or separate seed file is required.
```

Return the completed note as your final output — no commentary around it.
