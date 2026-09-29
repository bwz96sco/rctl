---
name: research-synthesis
description: Produce an evidence-bounded cross-paper answer in synthesis.md from a paper-discovery register and research-literature notes. Use when comparing findings, explaining contradictions, identifying closest prior work, mapping a field, or answering across a corpus.
---

# Research Synthesis

Turn a `$paper-discovery` register and its `$research-literature` notes into one argued answer to the existing target question. This skill compares the corpus; discovery and paper-local extraction stay with their owning skills.

## Contract

- **Inputs:** `register.md`, including the target question and corpus scope, plus `notes/<paper-id>.md` for in-scope register rows with `status=read`.
- **Output:** one `synthesis.md` beside `register.md`. It answers the existing target question or exploratory purpose; useful connections and hypotheses stay separate from evidence-backed conclusions. Develop research questions or approaches when requested; investment judgment belongs to explicit evaluation.
- **Always include:** the target question and scope, a direct answer, evidence coverage, issue-based cross-paper reasoning, and unresolved evidence or limitations.
- **Include when relevant or requested:** a field map, contradiction analysis, closest-prior comparison, or `Evidence-backed open problems`.

## Workflow

1. **Lock the evidence set.** Read the target question and scope from `register.md`, then match each in-scope `status=read` row to its note. Record included papers, read papers that do not bear on the question, and candidate, skimmed, blocked, conflicting, or unverified papers excluded from strong conclusions. Route a missing paper to `$paper-discovery` and a decisive missing extraction to `$research-literature`.
2. **Lead with the answer.** Open `synthesis.md` with the target question verbatim, the corpus scope, and a direct answer calibrated to the available evidence. State immediately when the corpus is too thin or incomplete for a strong answer.
3. **Compare by issue.** Organize the reasoning by shared mechanism, assumption, setting, or result rather than paper-by-paper summary. For an empirical contrast, identify the compared arms, their shared operations and what difference the comparison estimates before explaining an effect. Distinguish effects of changed operations from effects shared by both arms. Build comparison axes from the notes' field maps only when they improve the answer; a paper the axes cannot place shows that the map is incomplete.
4. **Trace and check the argument.** Every material synthesis claim names the contributing paper IDs and note anchors. For the few inferences on which the answer depends, compare the supporting passages and conditions with the conclusion, and identify the extra assumption or missing contrast. Check a decisive missing source when possible; otherwise keep the inference conditional and name the rival it leaves open. Before finalizing, carry any correction through the direct answer, issue discussion and open problems so they make the same bounded claim. Distinguish overlapping explanations from mutually exclusive outcome counts.
5. **Handle requested comparisons.**
   - For contradictions, classify each as `resolved`, `non-comparable`, or `unresolved`. A resolved contradiction names the evidence-backed deciding condition; a non-comparable one names the incompatible settings; an unresolved one names the missing evidence or deciding experiment without inventing a cause.
   - For closest prior work, compare `closest_candidate` papers across problem, method, inputs, data, evaluation, and claim. Name the closest paper or tied set, state exact overlap and differentiators, and keep the result blocked when a decisive candidate lacks full-text evidence. This is a prior-work comparison, not a novelty verdict.
   - For field mapping, merge only axes supported by the notes and show where coverage is empty or ambiguous.
6. **Expose open problems only when requested.** Add an `Evidence-backed open problems` section. Each item states the observed failure or untested boundary, evidence anchors, conditions under which it appears, and why the reviewed corpus does not resolve it.

Complete when the target question has a direct evidence-bounded answer; every in-scope read paper is used in the reasoning or listed as non-contributory with a reason; every material synthesis claim traces to paper IDs and note anchors; and excluded or unresolved evidence is visible. Requested contradiction, closest-prior, field-map, or open-problem work must also meet its step-specific requirements.

## Boundaries

- Treat an open-problem item as a corpus finding, not a novelty verdict, priority, readiness decision, or human selection.
- Leave `retain`, `hold`, `reject`, selection caps, and smallest-pilot gates to explicit evaluation.
- A thin corpus stays explicitly thin.
- Keep useful exploratory connections in a separate reflection within the same document, with their source basis and unverified assumptions. Develop questions or approaches in the existing discussion when requested. A resolved discrepancy can end the inquiry without manufacturing an open problem.
- Ideation may consume `synthesis.md`, but it can also start without synthesis.
