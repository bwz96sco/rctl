# Source Skill Map

training_problem: LoRA/QLoRA supervised fine-tuning with W&B tracking and tiny-overfit gate.
source_repo: https://github.com/Orchestra-Research/AI-Research-SKILLs.git
source_checked_at: 2026-06-17 commit 773a52944ba4747a18bd4ae9ade53fff041adcbc
selected_categories: 03-fine-tuning, 13-mlops, 10-optimization
selected_source_files_or_urls: 03-fine-tuning/peft/SKILL.md; 03-fine-tuning/axolotl/SKILL.md; 13-mlops/weights-and-biases/SKILL.md; 10-optimization/ml-training-recipes/SKILL.md
local_targets: training_plan.md; preflight_report.md; training_run_matrix.yaml; training_execution_log.md; model_training_handoff.md
used_concepts: LoRA rank/alpha defaults; QLoRA memory route; target module check; W&B config/artifact logging; tiny-overfit gate before main run.
waived_concepts: External benchmark values; W&B pricing/team setup; copied training code as command authority.
command_authority: Project training script `scripts/train_lora.py` and project config `configs/lora_fixture.yaml`; fixture commands are mock only.
open_questions: Replace mock artifact paths with real run paths before claim use.
