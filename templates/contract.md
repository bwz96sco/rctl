---
schema_version: 1
task_id: replace-task-id
title: "<Bounded question or deliverable>"
kind: exploration
# task new enables the following block when research/PROGRAM.md has a completed Goal.
# Replace "<Primary task evidence file>" in the generated goal criterion.
# goal_contribution:
#   obligation: "<The project goal obligation addressed by this task>"
#   expected_output: "<The decisive output for that obligation>"
#   decision_use: "<How favorable, unfavorable or inconclusive findings change the next investment>"
#   review_criterion: AC-02
criteria:
  - id: AC-01
    requirement: "<What evidence must establish before this task can close>"
    evidence_refs: ["result.md"]
    failure_action: "<What to correct, obtain, or leave unresolved if this criterion fails>"
    method:
      type: review
      reviewer: either
---

# Task contract

## Question

- Question: <The governing task question.>
- Origin and related history: <The origin of the request and, for new experiments, what related history leaves unanswered. Add the optional Question alignment section after this one when a broader project question governs the task.>

## Scope

<Included work, expected deliverable, starting evidence, and boundaries. For experiments, cite related routes, the substantive difference or reopen condition, and the decision new evidence would change.>

For an applied study, explain which part of the target problem this task answers
and what the chosen data or testbed represents. When target relevance is part of
the claim, cite the scenario brief and declare a review criterion for the conditions
preserved by the case and the supported conclusion. If the setting is unresolved,
specify the choice this task will inform.

For comparisons, distinguish complete-method benefit from conditional ablation or
diagnosis; name fixed control versions, generated/shared information and the primary
endpoint.

For paper-directed work, state the publication purpose: the brief's named claim or
evidence obligation, the decisive output, and how favorable, unfavorable or
inconclusive findings change the next investment. An enabling task names its
downstream experiment and observable handoff. Include Question alignment and a
required review criterion citing the brief, result and primary evidence to judge
this consequence. Early selection/calibration tasks may leave the claim provisional.

## Constraints

<Existing authorization, resources/budget, data boundaries, and any fixed comparison rules.>

For comparisons, distinguish development exposure, test-time feedback and final
evaluation; preserve total per-arm effort and control versions.

## Stop conditions

<When to stop, what would require an amendment or a new task, and whether negative or inconclusive closure is acceptable.>
