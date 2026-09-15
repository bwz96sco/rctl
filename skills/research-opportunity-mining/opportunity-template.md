# Opportunity seed template

Write one `opportunity-seeds.md` for the selected paper notes.

```markdown
---
stage: expansion_input
target_question: "<verbatim target>"
source_notes:
  - <path>
next_owner: research-ideation
---

# Paper opportunity seeds

## Lens coverage

Requested scope: <all six lenses by default, or the user's narrower scope>

| Paper | SUB | MOD | INP | XFR | ENV | MET |
| --- | --- | --- | --- | --- | --- | --- |
| <paper-id> | seeded / no_supported_seed / not_assessable | ... | ... | ... | ... | ... |

## O1: <short seed title>

- Source anchor: <paper id plus note section/page/table/figure>
- Lens: SUB / MOD / INP / XFR / ENV / MET
- Transformation: <what changes>
- Causal rationale: <why this could change the result>
- Research question: <question opened by the transformation>
- Required assets: <data, code, environment, or none>

## Handoff

Novelty, ranking, readiness, and selection: not assessed
Next owner: `$research-ideation`
```

Repeat cards only for supported seeds. Coverage rows preserve abstentions without creating empty cards. For a narrow request, omit out-of-scope columns or label them out of scope; they are not evidence that no seed exists.
