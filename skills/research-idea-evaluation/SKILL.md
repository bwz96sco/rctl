---
name: research-idea-evaluation
description: Assess whether research questions merit development or proposed investigations merit investment, using prior work, reader value and independent criticism. Invoke explicitly for question assessment, candidate comparison or a next-investment decision.
disable-model-invocation: true
---

# Research Idea Evaluation

Own value and investment judgment. Distinguish whether a question is worth answering
from whether a proposed approach is a good way to answer it. Developing or reframing
questions belongs to `$research-question`; replacement approaches belong to
`$research-ideation`. Surviving an attack is evidence about objections, not an
affirmative reason to invest.

## Choose the assessment subject

Read the active request before requiring artifacts. A question may arrive as a
statement, `questions.md` or another existing record. An investigation portfolio
arrives as `ideas.md`. If both are requested, assess the question and then the
approaches without adding a second approval ceremony. Preserve any user-reserved
choice and the existing authority to continue an expressly delegated workflow.

### Question assessment

Consider importance to the intended reader, the motivating evidence or need,
what remains unanswered relative to known work, and plausible ways evidence could
bear on the question. Check decisive premises proportionately. A question need not
already have a new algorithm, an observed baseline failure or a complete experimental
design. Unknown novelty remains unknown; an exact combination not found or a cheap
available test is insufficient to establish value.

Judge the prospective knowledge and reader consequence before choosing an order
of operations. Keep a scientific question separate from a prerequisite needed to
study it: an inexpensive annotation or feasibility check can come first without
becoming the preferred research contribution. Give an execution recommendation
only when requested. Distinguish an application's prerequisites from a question's
answerability; failure of a quality threshold may itself inform an explanatory
question rather than rule it out.

State which questions merit development, need reframing or lack a current value
case, and explain why. Distinguish insufficient evidence about a question from
evidence that its answer is already known or inconsequential. A promising question
can lack a good approach; a weak current approach does not settle the question's
value. Scale independent criticism to the proposed expenditure, rather than
requiring a separate reviewer for every exploratory question.

Keep the assessment in the existing question record or conversation. Use its
actual references or `Q#` labels; no `ideas.md`, `C#`, investigation brief or
solution-handoff validator is required. Complete when the value judgment and its
reason are clear, with the next intellectual step if one is justified. Further
question development goes to `$research-question`, approach development to
`$research-ideation`; a clear empirical inquiry can enter the study workflow with
an actual brief and allowance. A favorable assessment grants no execution budget.

## Investigation workspace

Continue beside `ideas.md`. For a new evaluation, use one `decision.md` with
[decision-template.md](decision-template.md): portfolio triage, selection basis,
investment cases, independent reviews, and next-investigation briefs. Link long
existing reviews rather than duplicate them. Its `decision_format: compact`
distinguishes this record from historical staged evaluations.

## Investigation assessment

1. **Read the request and evidence.** Validate `ideas.md` with `uv run --no-project python "<evaluation-skill>/scripts/validate-handoff.py" portfolio <idea-root>`, using this skill's actual installed directory. Compare the approaches with the parent question and active user request. If the question was silently replaced, return to `$research-question`; if the approaches fail to address it, return to `$research-ideation` before ranking. Picking the best supplied candidate cannot establish adequate scope. Identify any user-selected candidates or reserved human choice. Existing authority, not a new invocation ceremony, determines whether work can continue.
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
