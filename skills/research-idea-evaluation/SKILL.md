---
name: research-idea-evaluation
description: Screen a full research-idea portfolio, obtain an informed human shortlist, then converge it through independent deep evaluation. Invoke explicitly after research-ideation; selects at most two routes or closes blocked.
disable-model-invocation: true
---

# Research Idea Evaluation

Own convergence. First screen every portfolio candidate with bounded evidence. After the human shortlists from that screening, deeply evaluate only their choices. Generating or replacing the portfolio belongs to `$research-ideation`.

## Workspace

Continue in the idea folder. Require `ideas.md`; write `screening.md` with `screening-template.md`. After human selection, write `shortlist.md` with `shortlist-template.md`, then `attacks/<candidate-id>.md` and `decision.md` with `decision-template.md`.

## Workflow

1. **Validate the portfolio.** Use this skill's actual installed directory as `<evaluation-skill>`, regardless of host or install scope. Run `uv run --no-project python "<evaluation-skill>/scripts/validate-handoff.py" portfolio <idea-root>`.
2. **Screen every candidate.** If `screening.md` is absent, inspect each card against the supplied evidence and write one bounded screening record per candidate. Record closest-prior status, surviving delta, asset feasibility, strongest concern, evidence, and one advisory signal: `advance`, `hold`, or `reject`. This is triage, not a full candidate-specific literature review or final verdict. Run the validator with `screening <idea-root>`, show the human the screening, ask them to invoke `$research-idea-evaluation` again with their candidate IDs and verbatim rationale, then stop. Suggest 3–5 IDs for a broad portfolio; accept any nonempty explicit selection, including one candidate.
3. **Resume from screening.** On the later explicit invocation, validate the existing `screening.md`. If the human has not supplied an explicit post-screening selection, repeat the request and stop. Otherwise write `shortlist.md` from their IDs and verbatim rationale; do not infer selection from “continue.” A human may override any screening signal. Run the validator with `shortlist <idea-root>` before deep work.
4. **Attack only shortlisted candidates.** Use one clean subagent per candidate. Give it only the candidate card, parent question, supplied closest-prior paths, and `attack-template.md`. Save one attack per shortlisted `C#`. The generator never grades its own work.
5. **Verify and compare.** For each shortlisted candidate, verify closest prior, surviving delta, strongest method flaw, resource and asset feasibility, research-story value, fair controls, and decisive falsification terms.
6. **Close.** Write a disposition for every shortlisted candidate. `decision_status` is `selected` with one or two survivors, or `blocked` with none. Never force a winner and never introduce a new candidate.
7. **Prepare the next test.** For every survivor, add an experiment brief containing baseline, dataset, metric, intervention, budget, and abandonment rule. Use `next_owner: research-rapid-test` for an early feasibility or promote-or-drop pilot; use `next_owner: research-experiment` for requested formal reproduction, controlled comparison, ablation, or publication validation. Honor the user's requested depth and name the chosen skill. Blocked closure uses `next_owner: none`. A handoff grants no additional execution budget.
8. **Validate closure.** Run the packaged validator with `decision <idea-root>`. Any failure blocks handoff.

The screening pass is complete when `screening.md` covers the portfolio exactly once and the workflow is waiting for informed human selection. Final convergence is complete when every shortlisted candidate has one attack and disposition, selected IDs are a subset of the shortlist, zero to two survive, and the decision handoff validates.

## Rules

- Unknown novelty is not novelty; weak prior search blocks a novelty claim.
- Screening signals guide attention; they never mechanically prevent a human override.
- Report `no material objection found` when an honest attack finds none.
- Lexical similarity, fixed scores, and portfolio order are not research evidence.
- Evaluation may return lessons to a later expansion round, but it does not silently regenerate candidates.
