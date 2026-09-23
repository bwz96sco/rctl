# Orchestra AI Research Skills Model-Training Review

Source: `https://github.com/Orchestra-Research/AI-Research-SKILLs.git`
Commit: `773a52944ba4747a18bd4ae9ade53fff041adcbc`
Review date: `2026-06-17`
Status: selected manual review complete for v1 activation.

## Reviewed Sources

| source file | useful concepts | local targets | waived concepts |
|---|---|---|---|
| `03-fine-tuning/peft/SKILL.md` | LoRA/QLoRA choice, rank/alpha defaults, target modules, adapter save/eval, OOM fixes | `training_plan.md`, `preflight_report.md`, `training_run_matrix.yaml`, `training_diagnostic_report.md` | copy-paste training code, benchmark numbers as local evidence |
| `03-fine-tuning/axolotl/SKILL.md` | YAML-driven fine-tuning, FSDP/context-parallel checks, dataset format routing, chat template/masking checks | `source_skill_map.md`, `preflight_report.md`, `training_run_matrix.yaml` | Axolotl API docs as default command authority |
| `13-mlops/weights-and-biases/SKILL.md` | run config, metric logging, checkpoint/artifact lineage, offline mode, predictions table | `training_execution_log.md`, `model_training_handoff.md` | W&B pricing/team setup, UI report generation |
| `18-multimodal/whisper/SKILL.md` | ASR model size/VRAM, language/audio constraints, long-audio limits, hallucination risks | `preflight_report.md`, `training_diagnostic_report.md` | transcription CLI as training command |
| `10-optimization/ml-training-recipes/SKILL.md` | tiny-overfit gate, loss explosion debug, LR/batch/precision checks, OOM order, metric by domain | `training_plan.md`, `training_run_matrix.yaml`, `training_diagnostic_report.md` | source scaling numbers as project-specific claims |
| `03-fine-tuning/axolotl/references/dataset-formats.md` | JSONL/tokenized/conversation dataset choices, chat template and role masking checks, `max_steps` for streaming | `preflight_report.md`, `training_plan.md` | full Axolotl dataset docs import |

## V1 Decision

Activate `model-training-workflow` as workflow controller only. It may route training setup/debug work, create evidence packs, and call validators. It must not run expensive training or treat external examples as local results.

## Required Runtime Boundaries

- External Orchestra sources are reference inputs.
- Project commands, configs, datasets, checkpoints, logs, and metrics remain authority.
- Fixture logs are mock evidence for validator tests only.
- Real claims require actual run artifacts and handoff through `research-experiment`.
