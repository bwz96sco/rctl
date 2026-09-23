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
- Null or anti-win condition: <operationalized negative result; distinguish insufficient coverage or precision>

## Scope

- Comparison purpose: <complete-method benefit, conditional ablation, diagnosis/problem validation, or control screen>
- Baseline and source: <fixed ID/version, provenance and settings; distinguish main, published and enhanced controls>
- Intervention: <one bounded change>
- Information boundary: <shared raw inputs/tools, private generated records, permitted feedback and any diagnostic assistance>
- Dataset and split: <fixed data, development exposure and held-out split>
- Metric and evaluator: <primary endpoint, separate secondary/diagnostic metrics, direction and evaluator>
- Seeds and aggregation policy: <seeds, aggregation, selection and claim rule>
- Expected evidence locations: <runner and task-relative evidence paths>

## Scale assessment

- Decision and population: <opportunity, mechanism, performance or publication claim; target population>
- Independent units and repeats: <original cases/clusters, coverage, arms and repeats; distinguish variants>
- Worthwhile effect or precision: <decision-changing difference or uncertainty; for deterministic tests, required coverage>
- Scale rationale: <compatible pilot evidence or assumption range; miss risk, expected signal, paired/clustered power or supplied reproduction protocol, as applicable>
- Execution capacity: <cases × arms × repeats and likely calls/runtime, including screening, fresh controls, retries and review>
- Decision limits: <positive, negative and inconclusive outcomes; planned batches/analyses and budget stop; no automatic sample growth>

## Constraints

- Total budget: <supplied total and comparable per-arm generation/execution allowances; mark unresolved allocation>
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
Describe changed values, reason, and comparability impact here. Added enhanced controls
retain distinct versions and the original main comparison. None at initial revision.
