# Human shortlist template

Create only after `screening.md` validates and the human explicitly selects candidates from it.

```markdown
---
stage: shortlist_complete
portfolio: ideas.md
screening: screening.md
selected_candidate_ids: [C1, C4, C7]
decision_recorded_by: human_confirmed
next_owner: research-idea-evaluation
---

# Human shortlist

## Human rationale

<verbatim human wording>
```

Suggest 3–5 IDs for a broad portfolio, but preserve any nonempty explicit human selection, including a single candidate. An empty or inferred shortlist is invalid. Preserve the human's wording rather than replacing it with an agent summary. A screening signal never blocks a human override.
