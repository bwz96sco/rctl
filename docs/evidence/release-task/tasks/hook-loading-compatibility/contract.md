---
schema_version: 1
task_id: hook-loading-compatibility
title: Assess retained Codex hook-loading compatibility observations
kind: analysis
criteria:
  - id: AC-01
    requirement: Derived delivery counts and the assessment follow the fixed three-route comparison rule using actual retained receipts and host outputs.
    evidence_refs: [evidence/analysis.json, result.md, evidence/inline/events.jsonl, evidence/inline/receipts.jsonl, evidence/inline/final.txt, evidence/project/events.jsonl, evidence/project/receipts.jsonl, evidence/project/final.txt, evidence/none/events.jsonl, evidence/none/receipts.jsonl, evidence/none/final.txt]
    failure_action: Correct the derived analysis or retain an inconclusive finding if the supplied evidence cannot establish the rule.
    method:
      type: command
      argv: [uv, run, --offline, --no-project, python, check_analysis.py]
      timeout_seconds: 10
      inputs: [check_analysis.py, analyze.py, evidence/analysis.json, result.md, evidence/inline/launch.json, evidence/inline/summary.json, evidence/inline/events.jsonl, evidence/inline/receipts.jsonl, evidence/inline/final.txt, evidence/project/launch.json, evidence/project/summary.json, evidence/project/events.jsonl, evidence/project/receipts.jsonl, evidence/project/final.txt, evidence/none/launch.json, evidence/none/summary.json, evidence/none/events.jsonl, evidence/none/receipts.jsonl, evidence/none/final.txt]
  - id: AC-02
    requirement: Evidence review establishes which loading route is supported by these launches, separates absent delivery from root cause, and bounds conclusions to the tested host and settings.
    evidence_refs: [contract.md, result.md, evidence/analysis.json, evidence/inline/launch.json, evidence/inline/events.jsonl, evidence/inline/receipts.jsonl, evidence/inline/final.txt, evidence/project/launch.json, evidence/project/events.jsonl, evidence/project/receipts.jsonl, evidence/project/final.txt, evidence/none/launch.json, evidence/none/events.jsonl, evidence/none/receipts.jsonl, evidence/none/final.txt]
    failure_action: Revise unsupported interpretation or leave the task active with the unresolved review stated.
    method:
      type: review
      reviewer: either
---

## Question

Do the retained real Codex CLI 0.153.4 launches establish that project-file hook configuration delivers the same selected-task reminder as invocation-local inline configuration under the tested isolated settings? This bounded analysis is part of the user's request to complete rctl's initial release.

## Scope

Analyze the supplied real host observations for three routes: inline is the baseline; project-file loading with its recorded project-trust override is the intervention; hooks disabled is the control. Each uses a separate root with the same synthetic task materials and the same no-tool-use delivery prompt. The subject of this analysis is actual host delivery, not the invented metrics inside the smoke task. The results already exist as retained observations; this is not a blinded prospective experiment.

For routes that emitted no receipt file, the retained input contains an explicitly normalized empty `receipts.jsonl`; the original launch summary and model output document the absence. These empty files are analysis inputs, not fabricated hook receipts.

The evaluation set is exactly the three supplied launches, one per route, without selection or retries. Derive per-route `exit_code`, `receipts_total`, event-count map `events`, sorted host `session_ids`, boolean `model_reports_task`, and boolean `delivery_complete`. `model_reports_task` requires the model final text to contain `retained-comparison`, `active`, `B0`, and `C1`. `delivery_complete` requires host exit 0, both SessionStart and UserPromptSubmit receipts, each receipt bound to that launch's session ID, and model-reported task information. Larger delivery coverage is better. The controls and the deterministic checker define the evaluator; raw receipts and final text remain the evidence.

Write `evidence/analysis.json` with `routes` keyed by inline/project/none and `assessment`. The comparison is `supported` only if inline and project both have complete delivery and the none control exits 0, has no receipts, and reports NO_RCTL_REMINDER. It is `not_supported` if inline and the control satisfy those conditions while project exits 0 without complete delivery. Otherwise use `inconclusive`. This assessment concerns parity of the tested loading routes, not whether research metrics improved.

## Constraints

Freeze this contract before deriving the analysis. Budget: one local standard-library analysis of the retained artifacts and its declared verification, across two fresh rctl-enabled host sessions. The first session writes a handoff; the second receives it and completes evidence review and guarded closeout. No new host-route probes, network research, training, remote jobs, or global configuration changes are authorized within this analysis task. Keep scripts, derived data, result, and review in this task. Preserve raw observations.

Review launch arguments, actual event streams, receipts, and model outputs before attributing delivery. A missing receipt plus NO_RCTL_REMINDER supports absent observed delivery under those flags; it does not establish why loading failed. One launch per route cannot establish reliability, other versions, ordinary persisted installation, resume/compaction, or comparative model performance. Use rctl for this task's lifecycle even if another skill assumes Trellis.

## Stop conditions

Stop after the fixed comparison and review. Negative and bounded inconclusive outcomes may close when the criteria pass. Missing or contradictory evidence remains unresolved; changing the comparison rule or conducting new probes requires an amendment or a separate task. A chat pause leaves the task active; only a successful `rctl close` is managed closure.
