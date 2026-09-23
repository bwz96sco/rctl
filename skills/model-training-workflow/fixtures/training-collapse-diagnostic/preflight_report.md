# Preflight Report

## data_checks

Mock clips have duration, transcript, frame_count, and split fields. Train/val IDs disjoint.

## tokenization_or_label_checks

Blank token ID recorded. No transcript is empty. Label length is less than input frame length for all mock rows.

## model_and_checkpoint_checks

Checkpoint path recorded. Decoder vocab size equals tokenizer vocab size. Blank ID inside vocab range.

## environment_checks

Fixture env only. Real env must record CUDA, torch, ffmpeg/audio stack, and exact config.

## gpu_or_runtime_checks

Fixture runtime marks GPU unavailable. Real run records VRAM, mixed precision, batch size, and audio chunk length.

## dependency_docs_checked

Checked Whisper, ML training recipes, and W&B source files at pinned Orchestra commit.

## metric_sanity

CER lower is better. Blank_rate high means degenerate CTC output. Decode samples required for every eval.

## smoke_or_dry_run_gate

Mock one-batch forward and decode sanity artifacts exist under `artifacts/mock/ctc/`.

## blockers

No fixture blocker. Real run blocked until blank ID and tokenizer mapping are verified.

## unknowns

Real project may use non-CTC loss; then collapse taxonomy needs remap.
