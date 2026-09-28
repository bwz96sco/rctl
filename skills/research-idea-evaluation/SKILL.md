---
name: research-idea-evaluation
description: Evaluate research candidates for the next investment using prior work, reader value, independent criticism, and a discriminating first observation. Invoke explicitly after ideation; recommend up to two candidates or no investment.
disable-model-invocation: true
---

# Research Idea Evaluation

Own investment judgment. Evaluate the question and the next expenditure, including
whether a successful result would change an intended reader's belief or practice.
Generating replacement candidates belongs to `$research-ideation`. Surviving an
attack is evidence about objections, not an affirmative reason to invest.

## Workspace

Continue beside `ideas.md`. For a new evaluation, use one `decision.md` with
[decision-template.md](decision-template.md): portfolio triage, selection basis,
investment cases, independent reviews, and next-investigation briefs. Link long
existing reviews rather than duplicate them. Its `decision_format: compact`
distinguishes this record from historical staged evaluations.

## Workflow

1. **Read the request and evidence.** Validate `ideas.md` with `uv run --no-project python "<evaluation-skill>/scripts/validate-handoff.py" portfolio <idea-root>`, using this skill's actual installed directory. Compare the portfolio's framing with the active user request, including its requested research objects and measures. If the portfolio silently substituted a narrower engineering question, return it to candidate development before ranking; picking the best supplied candidate cannot establish adequate scope. Identify any user-selected candidates or reserved human choice. Existing authority, not a new invocation ceremony, determines whether work can continue.
2. **Triage every candidate.** Give each a bounded disposition with evidence: what the closest prior establishes, the surviving question, and the main reason to investigate, reframe, or park it. Check decisive prior passages and missing assets only where they could change that judgment. Unknown novelty is not novelty; an exact combination not found is not enough to invest. Established methods can still answer a consequential new question.
3. **Choose what merits deeper review.** Honor the user's selection; otherwise explain the prospective scientific claim and what even a favorable observation would add beyond the closest prior, then assess the next expenditure. An unknown cause, available failure or cheap contrast alone does not supply this case. A prerequisite probe is worthwhile when its result changes investment in an identified, worthwhile parent question; label that narrower role. Benefit need not be established in advance. Ask for human judgment when reader value, scope, or substantive ambiguity remains consequential. If selection is delegated, make and attribute the recommendation; “continue” advances an agreed stage but grants no new budget.
4. **Obtain independent criticism.** For candidates that may receive investment, use a clean subagent with the active user request, requested perspective, candidate frame/card, relevant raw evidence/prior paths, and [attack-template.md](attack-template.md), without the generator's preferred verdict. Ask it to check scope fidelity and scientific value as well as the decisive assumption and strongest rival; allow a return to candidate development. Scale depth to the next expenditure. Record reviewer identity/source and scope in `Independent Review: C#`. If independent review is unavailable, report that limit rather than label self-review independent; keep an unreviewed recommendation provisional.
5. **Make the affirmative case.** For each selected candidate, explain reader value, evidence making investigation credible, the strongest rival, and the observation that would change investment. Verify any method flaw, measurement-validity gap, or alternative explanation that controls this judgment. Both outcomes need not make a paper, but the proposed falsification or contrast must inform the next decision. Do not require benefit or prevalence to be proven before a probe designed to discover it.
6. **Close and hand off.** Use `selected` for one or two justified next investigations or `blocked` for no investment; preserve a disposition for every portfolio candidate. Add one `Investigation Brief: C#` per selection, matching the comparison, evidence, scale, and allowance to the claim. Use `research-rapid-test` for an early empirical observation, `research-experiment` for formal validation, or `research-theory` when a derivation/proof is the next work. Blocked closure uses `none`. Validate with `decision <idea-root>` before handoff; this checks structure and lineage, not scientific merit or execution authorization.

Complete when the recommendation says why the next expenditure is worthwhile,
which uncertainty it resolves, and what different outcomes imply. A selected
candidate needs an independent review and positive investment case. A well-founded
no-investment decision is a complete evaluation; preserve its specific missing
evidence rather than inventing a winner.

## Match evidence to the claim

| Claim | Central evidence and rival |
| --- | --- |
| Method performance | Complete method against the strongest relevant alternative under declared resources; the claimed outcome may be quality, cost, reliability, or useful delivery. |
| Measurement/evaluation | Independent judgments of relevant sensitivity and invariance, comparison to existing measures/simple audits, and a consequential use. |
| Empirical/explanatory | A defined domain or population, competing predictions, and discriminating contrasts; causal claims need identification. |

These are examples, not a closed taxonomy. Synthetic contrasts can test a
property or refute a universal claim; natural prevalence needs a sampling frame.
Oracle-assisted headroom is conditional. Share raw inputs for complete-method
comparisons and keep generated diagnoses private; shared information tests its
use. Retain primary claims prospectively. A downstream gain is required when it
is the claim, not for every measurement or explanatory contribution.

## Screening-only requests and historical records

For a requested screening-only pass, or a human-reserved choice, use
[screening-template.md](screening-template.md) and `screening <idea-root>`, then
present the recommendation and unresolved choice. Resuming an already authorized
evaluation does not require another invocation or verbatim-ID ceremony.

Existing `screening.md`, `shortlist.md`, `attacks/`, and legacy `decision.md`
remain valid. [shortlist-template.md](shortlist-template.md) is for that historical
human-confirmed format, not a prerequisite for compact decisions. The validator
retains its old stages; do not migrate frozen records to adopt the new workflow.
