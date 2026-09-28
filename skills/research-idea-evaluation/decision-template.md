# Compact investment decision template

```markdown
---
stage: converge_complete
decision_format: compact
portfolio: ideas.md
selection_basis: human | agent_recommendation
decision_status: selected | blocked
selected_candidate_ids: [C1] | []
reviewed_candidate_ids: [C1] | []
next_owner: research-rapid-test | research-experiment | research-theory | none
---

# Research investment decision

## Selection basis

<Actual request or human choice and rationale, or the scope delegated to the agent.
Explain whether the portfolio retains the requested perspective and what the
selected observation would add beyond existing knowledge. Distinguish an agent
recommendation from human selection, a prerequisite probe from a paper direction,
and both from execution authority.>

## Candidate Dispositions

| Candidate ID | Disposition | Evidence, closest prior, and reason |
| --- | --- | --- |
| C1 | selected / rejected / blocked | <source-linked triage and decisive uncertainty; cover every portfolio candidate> |

## Independent Review: C1

<Completed review from attack-template.md, or a precise link and attributed summary.
Include a section for each reviewed ID, including a reviewed candidate not selected.>

## Investment Case: C1

- Question, contribution, and reader consequence:
- Evidence versus unestablished premise:
- Why the next expenditure is worthwhile after considering the review:
- Strongest prior or rival and what would make further investment unattractive:

## Investigation Brief: C1

- Next uncertainty and discriminating observation:
- Claim-appropriate comparison, inputs, and private/generated evidence:
- Outcome or measurement; independent evaluation evidence:
- Units, coverage, and scale rationale, or proof obligation:
- Existing authority and total time/call allowance:
- Continue / concrete rescue / stop / inconclusive outcomes and claims not tested:
```

Select at most two candidates; a blocked decision has no selections and owner
`none`. Cover the whole portfolio in dispositions and the reviewed subset in
independent reviews. Every selected ID needs an investment case and investigation
brief; no positive result or novel mechanism is required in advance.

Keep this in one decision note. Structural validation checks coverage and lineage,
not the quality of the investment judgment or whether authority is sufficient.
Historical staged decisions and their `Experiment Brief: C#` headings remain
supported without migration.
