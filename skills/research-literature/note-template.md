# Paper note template

You are reading one paper for a target question or exploratory reading purpose. A precise new research question need not already exist. Fill the sections in order; it is the reading order: overview, field map, the method and its support, leads, and the analyst sections after reading. Before studying the method closely, briefly consider how you would approach the problem. Keep extraction concise without repeating the paper section by section, and reserve most of your effort for thinking after reading in the `Analyst` sections. Let length follow the paper's importance to the target question; save space by not restating the paper, not by dropping evidence.

Factual sections report only what the paper says; your judgments, inferences, and proposed ideas belong in the `Analyst` sections. Metadata inherits the supplied provenance: write one line per field, link the provenance rather than restating it, and preserve unresolved claims and source dates. Anchor material claims and numbers to a section, page, figure, table, or equation and record their evidence basis and confidence or caveat. With partial text or an abstract, fill only what the available source supports and mark deeper sections `not assessable from available access`.

```markdown
# <short-name>

Metadata: <title> / <authors>
Provenance: <register entry link, or directly supplied source>
Version read: <arXiv version/date, formal DOI, or supplied PDF identity>
Publication: <established status, venue/year/track; source/date or provenance link; unresolved claims>
Affiliations / research group: <author-to-institution mapping; explicitly sourced group or not established; source/page/date or provenance link>
Zotero key: <item-key / not_registered / unchecked>
Collection membership: <in_project / library_only / not_registered / unchecked; collection and check date/source, or provenance link>
Metadata status: verified | conflicting | unverified — <reason when not verified>
Access: full_pdf | partial_text | abstract_only
Source: <PDF path or URL>

## Overview
From the abstract, figures, and tables before detailed reading:
- Type of work: method | theory | empirical study | benchmark | system | survey
- Research question: the specific problem in the authors' formulation, why it
  matters, and where it applies; anchor (usually the abstract or the turn in the
  introduction)
- Central idea:
- Main reported result:

## Field map and gap
How the authors group prior and compared approaches and what each achieved — the
map of the field, not sentence-by-sentence coverage. Then the gap: the difficulty
that remains and the evidence given that the problem actually occurs.
(introduction, related work, compared methods)

## Method
Input -> core method -> Module A -> Module B -> Output.
Not "uses Transformer": state what exactly was changed vs prior work and which
stated difficulty each change addresses; do not describe every component.
Assumptions: what must hold for the method or claims to work. State theorems by
their claims and assumptions; retrace a proof only where a step is disputed,
and record that step as a defect.

## Experiments
- Dataset / scenario:
- Baselines:
- Why these datasets and baselines, as stated by the authors:
- Metrics:
- Protocol / split:
- Sample size / seeds / uncertainty:
- Code / data / weights availability, as stated by the authors:

## Key results
For each result that can affect the target question, including ablations that
show which components carry the effect:
- Claim or finding:
- Comparator:
- Exact value or qualitative result:
- Conditions, robustness, or failure boundary:
- Anchor: section/page/figure/table/equation
- Evidence basis: text | figure | table | equation
- Confidence / caveat:

## Limitations & future work
Author-stated only, with anchors. If absent after a full-text check, write
`not found after full-text check: <sections checked>`; with weaker access, write
`not assessable from available access`.

## Analyst: leads to follow
Concepts, techniques, or cited works you needed but could not resolve from this
paper, or that are worth reading next for the target question, each with its
anchor and why it matters. Write `none` when nothing remains.

## Analyst: evidence-backed defects
For each material defect:
- Defect:
- Evidence: section/page/table/result
- Evidence basis: text | figure | table | equation
- Why it matters:
- Author acknowledged it: yes | no
- Status: observed failure | analyst inference
- Confidence / caveat:

Question the authors' framing, assumptions, and solution rather than following
them. Look for an asserted but undemonstrated problem, unsupported conclusions,
weak, missing, or unequally resourced baselines or ablations, assumptions that
fail in the intended setting, narrow datasets, leakage, metrics that hide
failure, and claims that exceed the results. Distinguish failure to establish a
claim from evidence against it. Give full fields only to defects that affect the
target question or the paper's main claims; list minor issues one line each
with anchors. Report only defects the evidence supports, or
`no material defect established from this paper`; diagnose this paper without
claiming that a defect remains globally open. Improvements belong in the
reflection.

## Analyst: relation to target question
Your judgment: supports / limits / contradicts / direct overlap /
closest_candidate / mechanism neighbor / irrelevant. State why, the affected
part of the target question, and confidence. `closest_candidate` marks a plausible
neighbor; final closest-prior selection belongs to `$research-synthesis`.

Evidence quality for this question: the strongest support, the main limitation,
and what the paper cannot establish, linking the anchored results or defects
above. Distinguish claimed release of materials from checked access and from
successful reproduction. Judge by the paper's evidence rather than venue or team
reputation. With insufficient access, state `not assessable from available access`.

## Analyst: reflection
If this problem were yours, how would you approach it? Compare your approach
with the authors': where each obtains its information, what each can resolve,
and what costs or limitations follow. Do not present a familiar method as your
own idea. Record what the paper changed in your understanding and the questions
or alternatives worth pursuing. For an alternative, link the observation behind
it, separate the proposed operation and expected effect from established
findings, and name the key assumption or capability still missing, including how
required information would be obtained. A different module name alone is not an
alternative. A useful reflection may simply clarify a question; no improvement
idea is required.
```

Return the completed note as your final output — no commentary around it.
