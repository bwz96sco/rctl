---
schema_version: 1
task_id: replace-task-id
title: "<Bounded experiment question>"
kind: analysis
criteria:
  - id: AC-01
    requirement: "<Execution check for the frozen comparison, with declared inputs>"
    evidence_refs: ["result.md"]
    failure_action: "<Correct the named execution failure or leave the task unresolved>"
    method:
      type: command
      argv: ["<Bounded validation executable>", "<arguments>"]
      timeout_seconds: 30
      inputs: ["<Checker and helper/input paths>"]
  - id: AC-02
    requirement: "<Inspect evidence for comparability, failures, aggregation, and bounded claim>"
    evidence_refs: ["result.md"]
    failure_action: "<Correct evidence gaps or narrow the claim within the agreement>"
    method:
      type: review
      reviewer: either
---

# Experiment contract

## Question

- Question: <bounded question>
- Origin type: <supplied|problem|candidate>
- Origin ID: <stable-id-or-C#>
- Experiment role: <bounded-role; problem_validation for a problem origin>
- Null or anti-win condition: <operationalized negative result>

## Scope

- Baseline and source: <baseline and provenance>
- Intervention: <one bounded change>
- Dataset and split: <fixed data and split>
- Metric and evaluator: <definition, direction, evaluator>
- Seeds and aggregation policy: <seeds, aggregation, selection and claim rule>
- Expected evidence locations: <runner and task-relative evidence paths>

## Constraints

- Total budget: <supplied total and allocation; mark unresolved allocation>
- Authorization and data boundaries: <existing authorization and storage policy>

## Stop conditions

<Up to six bounded stop, kill, relaunch, or fallback rules; distinguish smoke from scientific runs.>
<State whether bounded negative or inconclusive results satisfy the criteria.>

## Run Matrix

| Run | Role | Configuration | Seeds | Budget | Expected evidence | Contract revision |
| --- | --- | --- | --- | --- | --- | --- |
| <run> | <smoke or claim-carrying> | <config> | <seeds> | <budget> | <path> | 1 |

## Amendments

Use rctl amend before dependent work; retain prior agreement in rctl's revision history.
Describe changed values, reason, and comparability impact here. None at initial revision.
