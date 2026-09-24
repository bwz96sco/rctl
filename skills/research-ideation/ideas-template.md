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

## Source inventory

| Source type | Artifact or supplied input | Used by candidates |
| --- | --- | --- |
| paper / reading note / method / dataset / experiment / human suggestion | <source anchor or supplied idea; mark interpretation or unchecked premise> | C1, C4 |

## C1: <candidate title>

- Research hook: <why researchers should care>
- Source combination: <anchored observations or supplied ideas; distinguish facts from interpretations>
- Mechanism: <concrete operation, why it could address the problem, and how it obtains the needed information>
- Expected claim: <bounded added capability if it works>
- Cheapest falsification test: <test that capability from the declared starting inputs>
- Closest prior arm: <known prior as an arm in the test above, or unknown with the missing comparison> - runnable / reimplemented / blocked / unknown
- Kill condition: <result that rejects the tested mechanism; distinguish unsuitable cases or missing inputs that leave it untested>
- Major uncertainty: <most consequential unverified assumption or capability still to be developed>

## Evaluation handoff

Invoke `$research-idea-evaluation` to screen every candidate before any human shortlist. No ranking or winner has been assigned.
```

Include sources used by the candidates, with specific passages or observations
where they matter. Match candidate breadth to the request and material; the
template imposes no count or lens quota. Record a consequential premise correction
alongside the affected candidate rather than creating another review document.
