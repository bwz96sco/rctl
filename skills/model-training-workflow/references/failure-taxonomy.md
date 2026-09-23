# Training Failure Taxonomy

## Use When

Use after a failed run, suspiciously good result, plateau, collapse, or repeated retry. Classify failure before another expensive run.

## Core Layers

| Layer | Symptoms | Next action |
|---|---|---|
| data | missing files, corrupt labels, leakage, split mismatch, transform mismatch | audit manifest, samples, label distribution, split IDs |
| tokenization / label space | unknown-token spikes, bad vocab, wrong blank/pad/eos handling | inspect encoded labels and decode round trips |
| architecture / capacity | cannot tiny-overfit, severe overfit, mismatch to target | reduce/increase model, use pretrained frontend, change route |
| loss / optimization | NaN/Inf, divergence, plateau, blank collapse, mode collapse | inspect LR, loss weights, gradients, logits, schedule |
| evaluation / decode | teacher-forced good but free-run bad, beam bug, metric mismatch | validate decode, metric, normalization, length policy |
| environment / runner | OOM, dependency drift, wrong checkpoint, failed sync | fix env, record state, retry with one delta |
| direction | capped/full split fails after sanity passes | stop, redesign, or choose differentiated model mechanism |

## Mandatory Diagnostics

- data counts, split identity, missing file count, sample visualization or text examples when applicable
- encode/decode round trip for labels or tokens
- tiny/two-batch overfit gate result
- capped or held-out preflight before full expensive run
- raw metric and normalized metric
- prediction examples, not only aggregate score
- loss curve and relevant health metrics
- checkpoint path, config path, git state, env snapshot

## Model Training Red Flags

- tiny overfit success treated as generalization evidence
- teacher-forced accuracy used as free-run claim
- metric improves but predictions are empty, too short, duplicated, or label-collapsed
- baseline differs by dataset, split, decode rule, checkpoint, tokenizer, or metric
- repeated continuation training after the same failure mode
- full run launched after capped gate fails
- OOM retry loops without changing memory driver or batch policy

## CTC / Sequence Decode Checks

For CTC, RNN-T, seq2seq, ASR/VSR/OCR, and pinyin/character targets:

- `blank_argmax_frac` or equivalent blank-dominance metric
- hypothesis length vs reference length distribution
- empty or too-short hypothesis rate
- free-run/greedy/beam metric separation
- teacher-forced accuracy vs free-run decode gap
- blank/pad/eos/id mapping
- per-token frequency and unknown-token count
- oracle length or decode cap only as diagnosis, not final fix

## Decision Rules

- implementation/environment failure -> fix one variable and rerun shortest useful gate
- evaluation failure -> audit metric/decode before training more
- optimization failure -> inspect health, gradients/logits, loss weights, LR, and checkpoint lineage
- direction failure -> stop current mechanism and update `model_training_handoff.md`
- repeated same-family failure -> redesign or route to ideation; do not continue with cosmetic tweaks

## Diagnostic Report Fields

```text
run_id:
failure_layer:
failure_type:
observed_signal:
evidence_paths:
fastest_falsification:
one_delta_retry:
stop_condition:
next_route:
claims_allowed:
claims_blocked:
```
