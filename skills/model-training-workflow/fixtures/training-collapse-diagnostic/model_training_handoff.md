# Model Training Handoff

## verdict

debug

## strongest_evidence

Fixture has metrics, predictions, and diagnostic report showing blank-collapse-shaped failure.

## weakest_evidence

Evidence is mock. Real project must verify tokenizer, loss, decode, and data checks.

## baseline_relation

Failed mock run worse than mock baseline on blank_rate and val_cer.

## claims_supported

Workflow can classify and route a collapse-shaped failure.

## claims_blocked

Real root cause and fix effectiveness.

## reusable_artifacts

`skills/model-training-workflow/fixtures/training-collapse-diagnostic/`

## research_experiment_target

After real one-delta retry, hand off result audit and claim boundary to `research-experiment`.

## project_adapter_updates

Add queue and monitor adapter only if repeated remote debug jobs are needed.

## next_action

Run one-delta debug retry in real project context.
