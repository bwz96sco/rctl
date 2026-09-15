# Evaluation decision template

```markdown
---
stage: converge_complete
portfolio: ideas.md
shortlist: shortlist.md
decision_status: selected | blocked
selected_candidate_ids: [C1] | []
next_owner: research-rapid-test | research-experiment | none
---

# Idea evaluation decision

## Candidate Dispositions

| Candidate ID | Disposition | Reason |
| --- | --- | --- |
| C1 | selected / rejected / blocked | <evidence-bound reason> |

## Experiment Brief: C1

- Baseline:
- Dataset and split:
- Metric:
- Intervention:
- Total budget:
- Abandonment rule:

## Lessons for a later expansion round

<optional; no new candidate IDs>
```

Use zero experiment briefs for blocked closure and exactly one brief per selected candidate.
Every ID in `selected_candidate_ids` must have disposition `selected`; no other row may use that disposition.
The brief describes the next bounded test: rapid-test for early feasibility, experiment for formal validation. Preserve the `Experiment Brief: C#` heading for existing handoff compatibility. A selected decision uses one of those two owners; a blocked decision uses `none`.
