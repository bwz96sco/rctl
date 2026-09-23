# Preflight Report

## data_checks

Fixture JSONL has `instruction` and `response` fields; train/val IDs disjoint; 40 total rows.

## tokenization_or_label_checks

Tokenizer path matches base model. Assistant-only labels checked; ignored prompt tokens use `-100`; decode round trip passes on two rows.

## model_and_checkpoint_checks

Base model path recorded. LoRA target modules include attention projections and MLP projections; trainable parameter ratio expected below 1%.

## environment_checks

Fixture env: `python=3.12`, `torch` mocked, `transformers` mocked, `peft` mocked. Real env must record `uv pip freeze` or equivalent.

## gpu_or_runtime_checks

Fixture runtime marks GPU unavailable. Real run needs CUDA device, VRAM, precision, and batch-size check.

## dependency_docs_checked

Checked Orchestra PEFT, Axolotl, W&B, and ML training recipes source files at pinned commit.

## metric_sanity

Validation NLL lower is better. Exact format match uses deterministic 8-prompt fixture.

## smoke_or_dry_run_gate

Dry run command creates mock W&B offline dir and mock checkpoint manifest.

## blockers

No fixture blocker. Real run blocked until dataset license and compute budget are confirmed.

## unknowns

Real GPU memory and final dataset scale unknown.
