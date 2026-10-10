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

For comparisons, distinguish complete-method benefit from conditional ablation or
diagnosis; name fixed control versions, generated/shared information and the primary
endpoint.

The project's research guidance says what Scope must state about the target setting
and the paper obligation; `goal_contribution` records that obligation when the
project has a completed Goal.

## Constraints

<Existing authorization, resources/budget, data boundaries, and any fixed comparison rules.>

For comparisons, distinguish development exposure, test-time feedback and final
evaluation; preserve total per-arm effort and control versions.

State only the exclusions this task's question needs. An earlier task's or plan's
boundaries, such as a selection round's "no simulator", do not carry over.

## Stop conditions

<When to stop, what would require an amendment or a new task, and whether negative or inconclusive closure is acceptable.>
