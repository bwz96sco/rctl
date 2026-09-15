# Idea portfolio template

```markdown
---
stage: expand_complete
target_question: "<verbatim target>"
next_owner: research-idea-evaluation
---

# Idea portfolio

## Frame

- Constraints:
- Non-goals:
- Human interests:
- Lens coverage: <count per lens>

## Source inventory

| Source type | Artifact or supplied input | Used by candidates |
| --- | --- | --- |
| problem / paper opportunity / method / dataset / observation / human suggestion | <path or short description> | C1, C4 / none |

## C1: <candidate title>

- Lens: transfer / contradiction / untested-assumption / scaling-regime / diagnostic / dataset / residual-attack
- Research hook: <why researchers should care>
- Source combination: <inputs combined>
- Mechanism: <what changes and why>
- Expected claim: <bounded claim if it works>
- Cheapest falsification test: <decisive minimum test>
- Closest prior arm: <known prior as an arm in the test above, or unknown with the missing comparison> - runnable / reimplemented / blocked / unknown
- Kill condition: <result that rejects the mechanism>
- Major uncertainty: <largest unknown>

## Evaluation handoff

Invoke `$research-idea-evaluation` to screen every candidate before any human shortlist. No ranking or winner has been assigned.
```

Enter one source-inventory row per distinct source item, not one row per file. A
multi-part source such as a synthesis contributes one row per contradiction, gap,
or finding; a part that produced no candidate is recorded as
`declined: <reason>` in the candidate column.
