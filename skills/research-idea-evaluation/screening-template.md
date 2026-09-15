# Portfolio screening template

```markdown
---
stage: screening_complete
portfolio: ideas.md
next_owner: human_shortlist
---

# Portfolio screening

## C1: <candidate title>

- Closest-prior status: <what supplied evidence establishes, or unknown>
- Surviving delta: <bounded difference still worth testing, or none found>
- Asset feasibility: <available, missing, or uncertain assets>
- Strongest concern: <main reason the route may fail>
- Evidence: <paper IDs, artifact paths, dataset links, or supplied observations>
- Screening signal: advance | hold | reject

## Human selection request

Select the screened candidate IDs you want evaluated and give your rationale. For a broad portfolio, 3–5 is a useful default; selecting only one or another explicit number is valid. You may override any signal. Invoke `$research-idea-evaluation` again with that choice to continue.
```

Cover every `ideas.md` candidate exactly once. Screening signals are advisory triage, not novelty verdicts or final selection.
