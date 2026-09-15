---
name: research-opportunity-mining
description: Derive evidence-bound paper-extension seeds using method substitution, module modification, input augmentation, scenario transfer, condition stress, and metric redesign. Invoke explicitly when paper notes should feed brainstorming; this helper never judges novelty or selects directions.
disable-model-invocation: true
---

# Research Opportunity Mining

Use paper evidence to produce atomic expansion inputs. This optional helper does not search literature, create complete candidates, rank seeds, or select a route.

## Workspace

Read an existing register and full-paper notes. Write one `opportunity-seeds.md` beside them, using `opportunity-template.md`. Do not edit source notes.

## Workflow

1. **Freeze inputs.** Record the target question and selected note paths. Abstract-only notes are not sufficient for deep method analysis.
2. **Reconstruct each paper.** Capture inputs, method modules, assumptions, outputs, and evaluation. Inspect a local PDF section only when the note lacks one required detail.
3. **Apply the requested lenses.** For broad opportunity mining, consider all six: `SUB` method substitution, `MOD` module modification, `INP` input augmentation, `XFR` scenario transfer, `ENV` condition stress, and `MET` metric redesign. If the user requests a specific lens or narrower scope, cover only that scope and state the omitted lenses as out of scope. Record `seeded`, `no_supported_seed`, or `not_assessable` for each considered lens; never force a seed.
4. **Write supported seeds.** Use stable IDs `O1..On`. Each seed records its paper anchor, lens, transformation, causal rationale, research question, and required assets.
5. **Hand off.** Set `stage: expansion_input` and `next_owner: research-ideation`, name `$research-ideation`, then stop.

Complete when every selected paper has coverage of the requested lenses (all six by default), every emitted seed has a paper anchor and causal rationale, and `opportunity-seeds.md` contains no novelty, ranking, readiness, or selection judgment.

## Lens guards

- `SUB`: connect the replacement capability to an observed bottleneck.
- `MOD`: anchor the weak module in an ablation, failure, or explicit assumption.
- `INP`: require information available at deployment; exclude solution or label leakage.
- `XFR`: change a scientific difficulty, not only the application noun.
- `ENV`: use a condition reachable in supported operation.
- `MET`: require a metric capable of changing a conclusion or operational decision.

Methods may come from the paper or a supplied concept. Label uncited mechanisms as unverified rather than inventing citations.
