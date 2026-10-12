# Source Skill Map

training_problem: Diagnose multimodal/ASR training collapse with CTC blank domination signal.
source_repo: https://github.com/Orchestra-Research/AI-Research-SKILLs.git
source_checked_at: 2026-06-17 commit 773a52944ba4747a18bd4ae9ade53fff041adcbc
selected_categories: 18-multimodal, 10-optimization, 13-mlops
selected_source_files_or_urls: 18-multimodal/whisper/SKILL.md; 10-optimization/ml-training-recipes/SKILL.md; 13-mlops/weights-and-biases/SKILL.md
local_targets: preflight_report.md; training_run_matrix.yaml; training_diagnostic_report.md; model_training_handoff.md
used_concepts: audio length/quality checks; VRAM/model-size checks; loss explosion and plateau debug; gradient and prediction logging; artifact lineage.
waived_concepts: Whisper transcription CLI as training command; external performance numbers as local evidence.
command_authority: Project ASR/VSR training script `scripts/train_ctc.py`; fixture commands are mock only.
open_questions: Real blank-rate threshold must be calibrated on project tokenizer and validation split.
