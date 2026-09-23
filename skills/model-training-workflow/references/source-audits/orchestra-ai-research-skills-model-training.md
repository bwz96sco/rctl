# Orchestra AI Research Skills Model-Training Source Audit

Source: `https://github.com/Orchestra-Research/AI-Research-SKILLs.git`
Commit: `773a52944ba4747a18bd4ae9ade53fff041adcbc`
Checked at: `2026-06-17`
Records: `98`

## Status

This is a source-inspection audit, not a distillation approval. `model-training-workflow` remains local draft until selected records receive manual source read, local target mapping, route tests, and validation.

## Classification Counts

- `research-orchestration`: 6
- `tool-wrapper`: 18
- `training-adjacent`: 15
- `training-core`: 55
- `writing/figure`: 4

## Training-Core And Adjacent Sources

| classification | category | skill | path | score | local target |
|---|---|---|---|---:|---|
| training-core | 01-model-architecture | implementing-llms-litgpt | `01-model-architecture/litgpt/SKILL.md` | 12 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 01-model-architecture | mamba-architecture | `01-model-architecture/mamba/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 01-model-architecture | nanogpt | `01-model-architecture/nanogpt/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 01-model-architecture | rwkv-architecture | `01-model-architecture/rwkv/SKILL.md` | 11 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 01-model-architecture | distributed-llm-pretraining-torchtitan | `01-model-architecture/torchtitan/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 02-tokenization | huggingface-tokenizers | `02-tokenization/huggingface-tokenizers/SKILL.md` | 8 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 02-tokenization | sentencepiece | `02-tokenization/sentencepiece/SKILL.md` | 8 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 03-fine-tuning | axolotl | `03-fine-tuning/axolotl/SKILL.md` | 14 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 03-fine-tuning | llama-factory | `03-fine-tuning/llama-factory/SKILL.md` | 9 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 03-fine-tuning | peft-fine-tuning | `03-fine-tuning/peft/SKILL.md` | 12 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 03-fine-tuning | unsloth | `03-fine-tuning/unsloth/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-adjacent | 04-mechanistic-interpretability | nnsight-remote-interpretability | `04-mechanistic-interpretability/nnsight/SKILL.md` | 7 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-adjacent | 04-mechanistic-interpretability | pyvene-interventions | `04-mechanistic-interpretability/pyvene/SKILL.md` | 7 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-adjacent | 04-mechanistic-interpretability | sparse-autoencoder-training | `04-mechanistic-interpretability/saelens/SKILL.md` | 6 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-adjacent | 04-mechanistic-interpretability | transformer-lens-interpretability | `04-mechanistic-interpretability/transformer-lens/SKILL.md` | 6 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-adjacent | 05-data-processing | nemo-curator | `05-data-processing/nemo-curator/SKILL.md` | 7 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-adjacent | 05-data-processing | ray-data | `05-data-processing/ray-data/SKILL.md` | 6 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-core | 06-post-training | grpo-rl-training | `06-post-training/grpo-rl-training/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 06-post-training | miles-rl-training | `06-post-training/miles/SKILL.md` | 12 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 06-post-training | openrlhf-training | `06-post-training/openrlhf/SKILL.md` | 12 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 06-post-training | simpo-training | `06-post-training/simpo/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 06-post-training | slime-rl-training | `06-post-training/slime/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 06-post-training | torchforge-rl-training | `06-post-training/torchforge/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 06-post-training | fine-tuning-with-trl | `06-post-training/trl-fine-tuning/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 06-post-training | verl-rl-training | `06-post-training/verl/SKILL.md` | 11 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 08-distributed-training | huggingface-accelerate | `08-distributed-training/accelerate/SKILL.md` | 8 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 08-distributed-training | deepspeed | `08-distributed-training/deepspeed/SKILL.md` | 9 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 08-distributed-training | training-llms-megatron | `08-distributed-training/megatron-core/SKILL.md` | 9 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 08-distributed-training | pytorch-fsdp2 | `08-distributed-training/pytorch-fsdp2/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 08-distributed-training | pytorch-lightning | `08-distributed-training/pytorch-lightning/SKILL.md` | 9 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 08-distributed-training | ray-train | `08-distributed-training/ray-train/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-adjacent | 09-infrastructure | lambda-labs-gpu-cloud | `09-infrastructure/lambda-labs/SKILL.md` | 11 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-adjacent | 09-infrastructure | modal-serverless-gpu | `09-infrastructure/modal/SKILL.md` | 8 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-adjacent | 09-infrastructure | skypilot-multi-cloud-orchestration | `09-infrastructure/skypilot/SKILL.md` | 9 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-core | 10-optimization | awq-quantization | `10-optimization/awq/SKILL.md` | 15 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 10-optimization | quantizing-models-bitsandbytes | `10-optimization/bitsandbytes/SKILL.md` | 13 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 10-optimization | optimizing-attention-flash | `10-optimization/flash-attention/SKILL.md` | 11 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 10-optimization | gguf-quantization | `10-optimization/gguf/SKILL.md` | 9 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 10-optimization | gptq | `10-optimization/gptq/SKILL.md` | 14 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 10-optimization | hqq-quantization | `10-optimization/hqq/SKILL.md` | 11 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 10-optimization | ml-training-recipes | `10-optimization/ml-training-recipes/SKILL.md` | 15 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 11-evaluation | evaluating-code-models | `11-evaluation/bigcode-evaluation-harness/SKILL.md` | 8 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 11-evaluation | evaluating-llms-harness | `11-evaluation/lm-evaluation-harness/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 11-evaluation | nemo-evaluator-sdk | `11-evaluation/nemo-evaluator/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-adjacent | 12-inference-serving | llama-cpp | `12-inference-serving/llama-cpp/SKILL.md` | 7 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-adjacent | 12-inference-serving | sglang | `12-inference-serving/sglang/SKILL.md` | 7 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-adjacent | 12-inference-serving | tensorrt-llm | `12-inference-serving/tensorrt-llm/SKILL.md` | 9 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-adjacent | 12-inference-serving | serving-llms-vllm | `12-inference-serving/vllm/SKILL.md` | 7 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-core | 13-mlops | mlflow | `13-mlops/mlflow/SKILL.md` | 7 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 13-mlops | experiment-tracking-swanlab | `13-mlops/swanlab/SKILL.md` | 9 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 13-mlops | tensorboard | `13-mlops/tensorboard/SKILL.md` | 7 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 13-mlops | weights-and-biases | `13-mlops/weights-and-biases/SKILL.md` | 8 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-adjacent | 17-observability | langsmith-observability | `17-observability/langsmith/SKILL.md` | 6 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-adjacent | 17-observability | phoenix-observability | `17-observability/phoenix/SKILL.md` | 6 | candidate: model-training-workflow source-routing or experiment-adapter-builder |
| training-core | 18-multimodal | audiocraft-audio-generation | `18-multimodal/audiocraft/SKILL.md` | 8 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 18-multimodal | blip-2-vision-language | `18-multimodal/blip-2/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 18-multimodal | clip | `18-multimodal/clip/SKILL.md` | 9 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 18-multimodal | evaluating-cosmos-policy | `18-multimodal/cosmos-policy/SKILL.md` | 12 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 18-multimodal | llava | `18-multimodal/llava/SKILL.md` | 9 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 18-multimodal | fine-tuning-serving-openpi | `18-multimodal/openpi/SKILL.md` | 11 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 18-multimodal | fine-tuning-openvla-oft | `18-multimodal/openvla-oft/SKILL.md` | 14 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 18-multimodal | segment-anything-model | `18-multimodal/segment-anything/SKILL.md` | 9 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 18-multimodal | stable-diffusion-image-generation | `18-multimodal/stable-diffusion/SKILL.md` | 12 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 18-multimodal | whisper | `18-multimodal/whisper/SKILL.md` | 7 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 19-emerging-techniques | knowledge-distillation | `19-emerging-techniques/knowledge-distillation/SKILL.md` | 8 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 19-emerging-techniques | long-context | `19-emerging-techniques/long-context/SKILL.md` | 8 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 19-emerging-techniques | model-merging | `19-emerging-techniques/model-merging/SKILL.md` | 10 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 19-emerging-techniques | model-pruning | `19-emerging-techniques/model-pruning/SKILL.md` | 9 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 19-emerging-techniques | moe-training | `19-emerging-techniques/moe-training/SKILL.md` | 9 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |
| training-core | 19-emerging-techniques | speculative-decoding | `19-emerging-techniques/speculative-decoding/SKILL.md` | 9 | candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff |

## Full Inventory

| classification | category | skill | path | status |
|---|---|---|---|---|
| research-orchestration | 0-autoresearch-skill | autoresearch | `0-autoresearch-skill/SKILL.md` | waived_or_existing_owner |
| training-core | 01-model-architecture | implementing-llms-litgpt | `01-model-architecture/litgpt/SKILL.md` | pending_manual_review |
| training-core | 01-model-architecture | mamba-architecture | `01-model-architecture/mamba/SKILL.md` | pending_manual_review |
| training-core | 01-model-architecture | nanogpt | `01-model-architecture/nanogpt/SKILL.md` | pending_manual_review |
| training-core | 01-model-architecture | rwkv-architecture | `01-model-architecture/rwkv/SKILL.md` | pending_manual_review |
| training-core | 01-model-architecture | distributed-llm-pretraining-torchtitan | `01-model-architecture/torchtitan/SKILL.md` | pending_manual_review |
| training-core | 02-tokenization | huggingface-tokenizers | `02-tokenization/huggingface-tokenizers/SKILL.md` | pending_manual_review |
| training-core | 02-tokenization | sentencepiece | `02-tokenization/sentencepiece/SKILL.md` | pending_manual_review |
| training-core | 03-fine-tuning | axolotl | `03-fine-tuning/axolotl/SKILL.md` | pending_manual_review |
| training-core | 03-fine-tuning | llama-factory | `03-fine-tuning/llama-factory/SKILL.md` | pending_manual_review |
| training-core | 03-fine-tuning | peft-fine-tuning | `03-fine-tuning/peft/SKILL.md` | pending_manual_review |
| training-core | 03-fine-tuning | unsloth | `03-fine-tuning/unsloth/SKILL.md` | pending_manual_review |
| training-adjacent | 04-mechanistic-interpretability | nnsight-remote-interpretability | `04-mechanistic-interpretability/nnsight/SKILL.md` | pending_manual_review |
| training-adjacent | 04-mechanistic-interpretability | pyvene-interventions | `04-mechanistic-interpretability/pyvene/SKILL.md` | pending_manual_review |
| training-adjacent | 04-mechanistic-interpretability | sparse-autoencoder-training | `04-mechanistic-interpretability/saelens/SKILL.md` | pending_manual_review |
| training-adjacent | 04-mechanistic-interpretability | transformer-lens-interpretability | `04-mechanistic-interpretability/transformer-lens/SKILL.md` | pending_manual_review |
| training-adjacent | 05-data-processing | nemo-curator | `05-data-processing/nemo-curator/SKILL.md` | pending_manual_review |
| training-adjacent | 05-data-processing | ray-data | `05-data-processing/ray-data/SKILL.md` | pending_manual_review |
| training-core | 06-post-training | grpo-rl-training | `06-post-training/grpo-rl-training/SKILL.md` | pending_manual_review |
| training-core | 06-post-training | miles-rl-training | `06-post-training/miles/SKILL.md` | pending_manual_review |
| training-core | 06-post-training | openrlhf-training | `06-post-training/openrlhf/SKILL.md` | pending_manual_review |
| training-core | 06-post-training | simpo-training | `06-post-training/simpo/SKILL.md` | pending_manual_review |
| training-core | 06-post-training | slime-rl-training | `06-post-training/slime/SKILL.md` | pending_manual_review |
| training-core | 06-post-training | torchforge-rl-training | `06-post-training/torchforge/SKILL.md` | pending_manual_review |
| training-core | 06-post-training | fine-tuning-with-trl | `06-post-training/trl-fine-tuning/SKILL.md` | pending_manual_review |
| training-core | 06-post-training | verl-rl-training | `06-post-training/verl/SKILL.md` | pending_manual_review |
| tool-wrapper | 07-safety-alignment | constitutional-ai | `07-safety-alignment/constitutional-ai/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 07-safety-alignment | llamaguard | `07-safety-alignment/llamaguard/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 07-safety-alignment | nemo-guardrails | `07-safety-alignment/nemo-guardrails/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 07-safety-alignment | prompt-guard | `07-safety-alignment/prompt-guard/SKILL.md` | waived_or_existing_owner |
| training-core | 08-distributed-training | huggingface-accelerate | `08-distributed-training/accelerate/SKILL.md` | pending_manual_review |
| training-core | 08-distributed-training | deepspeed | `08-distributed-training/deepspeed/SKILL.md` | pending_manual_review |
| training-core | 08-distributed-training | training-llms-megatron | `08-distributed-training/megatron-core/SKILL.md` | pending_manual_review |
| training-core | 08-distributed-training | pytorch-fsdp2 | `08-distributed-training/pytorch-fsdp2/SKILL.md` | pending_manual_review |
| training-core | 08-distributed-training | pytorch-lightning | `08-distributed-training/pytorch-lightning/SKILL.md` | pending_manual_review |
| training-core | 08-distributed-training | ray-train | `08-distributed-training/ray-train/SKILL.md` | pending_manual_review |
| training-adjacent | 09-infrastructure | lambda-labs-gpu-cloud | `09-infrastructure/lambda-labs/SKILL.md` | pending_manual_review |
| training-adjacent | 09-infrastructure | modal-serverless-gpu | `09-infrastructure/modal/SKILL.md` | pending_manual_review |
| training-adjacent | 09-infrastructure | skypilot-multi-cloud-orchestration | `09-infrastructure/skypilot/SKILL.md` | pending_manual_review |
| training-core | 10-optimization | awq-quantization | `10-optimization/awq/SKILL.md` | pending_manual_review |
| training-core | 10-optimization | quantizing-models-bitsandbytes | `10-optimization/bitsandbytes/SKILL.md` | pending_manual_review |
| training-core | 10-optimization | optimizing-attention-flash | `10-optimization/flash-attention/SKILL.md` | pending_manual_review |
| training-core | 10-optimization | gguf-quantization | `10-optimization/gguf/SKILL.md` | pending_manual_review |
| training-core | 10-optimization | gptq | `10-optimization/gptq/SKILL.md` | pending_manual_review |
| training-core | 10-optimization | hqq-quantization | `10-optimization/hqq/SKILL.md` | pending_manual_review |
| training-core | 10-optimization | ml-training-recipes | `10-optimization/ml-training-recipes/SKILL.md` | pending_manual_review |
| training-core | 11-evaluation | evaluating-code-models | `11-evaluation/bigcode-evaluation-harness/SKILL.md` | pending_manual_review |
| training-core | 11-evaluation | evaluating-llms-harness | `11-evaluation/lm-evaluation-harness/SKILL.md` | pending_manual_review |
| training-core | 11-evaluation | nemo-evaluator-sdk | `11-evaluation/nemo-evaluator/SKILL.md` | pending_manual_review |
| training-adjacent | 12-inference-serving | llama-cpp | `12-inference-serving/llama-cpp/SKILL.md` | pending_manual_review |
| training-adjacent | 12-inference-serving | sglang | `12-inference-serving/sglang/SKILL.md` | pending_manual_review |
| training-adjacent | 12-inference-serving | tensorrt-llm | `12-inference-serving/tensorrt-llm/SKILL.md` | pending_manual_review |
| training-adjacent | 12-inference-serving | serving-llms-vllm | `12-inference-serving/vllm/SKILL.md` | pending_manual_review |
| training-core | 13-mlops | mlflow | `13-mlops/mlflow/SKILL.md` | pending_manual_review |
| training-core | 13-mlops | experiment-tracking-swanlab | `13-mlops/swanlab/SKILL.md` | pending_manual_review |
| training-core | 13-mlops | tensorboard | `13-mlops/tensorboard/SKILL.md` | pending_manual_review |
| training-core | 13-mlops | weights-and-biases | `13-mlops/weights-and-biases/SKILL.md` | pending_manual_review |
| tool-wrapper | 14-agents | evolving-ai-agents | `14-agents/a-evolve/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 14-agents | autogpt-agents | `14-agents/autogpt/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 14-agents | crewai-multi-agent | `14-agents/crewai/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 14-agents | langchain | `14-agents/langchain/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 14-agents | llamaindex | `14-agents/llamaindex/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 15-rag | chroma | `15-rag/chroma/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 15-rag | faiss | `15-rag/faiss/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 15-rag | pinecone | `15-rag/pinecone/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 15-rag | qdrant-vector-search | `15-rag/qdrant/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 15-rag | sentence-transformers | `15-rag/sentence-transformers/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 16-prompt-engineering | dspy | `16-prompt-engineering/dspy/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 16-prompt-engineering | guidance | `16-prompt-engineering/guidance/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 16-prompt-engineering | instructor | `16-prompt-engineering/instructor/SKILL.md` | waived_or_existing_owner |
| tool-wrapper | 16-prompt-engineering | outlines | `16-prompt-engineering/outlines/SKILL.md` | waived_or_existing_owner |
| training-adjacent | 17-observability | langsmith-observability | `17-observability/langsmith/SKILL.md` | pending_manual_review |
| training-adjacent | 17-observability | phoenix-observability | `17-observability/phoenix/SKILL.md` | pending_manual_review |
| training-core | 18-multimodal | audiocraft-audio-generation | `18-multimodal/audiocraft/SKILL.md` | pending_manual_review |
| training-core | 18-multimodal | blip-2-vision-language | `18-multimodal/blip-2/SKILL.md` | pending_manual_review |
| training-core | 18-multimodal | clip | `18-multimodal/clip/SKILL.md` | pending_manual_review |
| training-core | 18-multimodal | evaluating-cosmos-policy | `18-multimodal/cosmos-policy/SKILL.md` | pending_manual_review |
| training-core | 18-multimodal | llava | `18-multimodal/llava/SKILL.md` | pending_manual_review |
| training-core | 18-multimodal | fine-tuning-serving-openpi | `18-multimodal/openpi/SKILL.md` | pending_manual_review |
| training-core | 18-multimodal | fine-tuning-openvla-oft | `18-multimodal/openvla-oft/SKILL.md` | pending_manual_review |
| training-core | 18-multimodal | segment-anything-model | `18-multimodal/segment-anything/SKILL.md` | pending_manual_review |
| training-core | 18-multimodal | stable-diffusion-image-generation | `18-multimodal/stable-diffusion/SKILL.md` | pending_manual_review |
| training-core | 18-multimodal | whisper | `18-multimodal/whisper/SKILL.md` | pending_manual_review |
| training-core | 19-emerging-techniques | knowledge-distillation | `19-emerging-techniques/knowledge-distillation/SKILL.md` | pending_manual_review |
| training-core | 19-emerging-techniques | long-context | `19-emerging-techniques/long-context/SKILL.md` | pending_manual_review |
| training-core | 19-emerging-techniques | model-merging | `19-emerging-techniques/model-merging/SKILL.md` | pending_manual_review |
| training-core | 19-emerging-techniques | model-pruning | `19-emerging-techniques/model-pruning/SKILL.md` | pending_manual_review |
| training-core | 19-emerging-techniques | moe-training | `19-emerging-techniques/moe-training/SKILL.md` | pending_manual_review |
| training-core | 19-emerging-techniques | speculative-decoding | `19-emerging-techniques/speculative-decoding/SKILL.md` | pending_manual_review |
| writing/figure | 20-ml-paper-writing | academic-plotting | `20-ml-paper-writing/academic-plotting/SKILL.md` | waived_or_existing_owner |
| writing/figure | 20-ml-paper-writing | ml-paper-writing | `20-ml-paper-writing/ml-paper-writing/SKILL.md` | waived_or_existing_owner |
| writing/figure | 20-ml-paper-writing | presenting-conference-talks | `20-ml-paper-writing/presenting-conference-talks/SKILL.md` | waived_or_existing_owner |
| writing/figure | 20-ml-paper-writing | systems-paper-writing | `20-ml-paper-writing/systems-paper-writing/SKILL.md` | waived_or_existing_owner |
| research-orchestration | 21-research-ideation | brainstorming-research-ideas | `21-research-ideation/brainstorming-research-ideas/SKILL.md` | waived_or_existing_owner |
| research-orchestration | 21-research-ideation | creative-thinking-for-research | `21-research-ideation/creative-thinking-for-research/SKILL.md` | waived_or_existing_owner |
| research-orchestration | 22-agent-native-research-artifact | ara-compiler | `22-agent-native-research-artifact/compiler/SKILL.md` | waived_or_existing_owner |
| research-orchestration | 22-agent-native-research-artifact | ara-research-manager | `22-agent-native-research-artifact/research-manager/SKILL.md` | waived_or_existing_owner |
| research-orchestration | 22-agent-native-research-artifact | ara-rigor-reviewer | `22-agent-native-research-artifact/rigor-reviewer/SKILL.md` | waived_or_existing_owner |
