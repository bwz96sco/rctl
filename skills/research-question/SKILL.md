---
name: research-question
description: Develop and refine research questions from observations, goals, papers, conflicting findings, or new technical capabilities. Use when deciding what is worth studying or reframing a problem. Reading belongs to research-literature; designing approaches to a clear question belongs to research-ideation.
---

# Research Question

Own question formation. Turn a motivating observation or need into a question
whose answer could change understanding or practice. Preserve the user's requested
perspective while exploring different framings. Methods can inspire questions;
an available implementation or an unexplained case alone does not establish value.

## Workspace and entry

Use the supplied material directly: reading notes, experimental observations,
practical needs, human suggestions or a method's demonstrated capability. Literature
and synthesis can help, but neither is a prerequisite. A user-supplied clear question
can go directly to `$research-ideation` for ways to answer it.

For a short discussion, answer in chat. For durable question development, continue
the existing topic record or use `questions.md` in that topic. For a new topic,
follow the project-relative vault binding in `.rctl/project.json` or the existing
note convention; otherwise use `artifacts/research-question/<topic>/`. Use `Q1`,
`Q2`, etc. only when multiple questions need references. Reading reflections stay
in their paper notes unless further development is requested.

## Develop the question

1. **Establish the inquiry.** Preserve the active user goal, intended reader and
   requested perspective. Separate real constraints from inherited assumptions,
   including whether the task, research object and evaluation may change.
2. **Choose a useful entry.** Consult the relevant sections of
   [question routes](references/question-routes.md): failure/bottleneck, successful
   effect, conflicting findings, goal/assumption change, measurement ambiguity, or
   new technical capability. Combine routes when useful; they are alternatives,
   not a coverage requirement.
3. **Develop alternative framings.** Ask what is important to understand or achieve,
   not just what operation could be added. Vary a consequential assumption, unit,
   time scale or explanation when it opens a different question. Explore the
   requested breadth before comparing candidates. Keep observations, interpretations
   and proposals distinguishable; speculative ideas can be useful when labelled.
   Carry these distinctions into the question's motivation and value argument,
   rather than qualifying an assumption once and later treating it as established.
4. **Check decisive premises and refine.** Reuse relevant source evidence. Check a
   claim or closest-prior passage when it could change the question; route a missing
   paper to `$paper-discovery`, reading to `$research-literature`, and cross-paper
   comparison to `$research-synthesis`. Reopen a framing when evidence changes it.
   A bounded search does not establish novelty, and a missing benchmark failure
   does not by itself rule out a measurement or explanatory question.
5. **State the developed questions.** In concise prose, communicate the research
   object and scope, motivation, precise unknown, possible reader consequence,
   relation to known work, and preliminary answerability. Competing answers are
   helpful for explanatory questions; capability and measurement questions need
   a meaningful success distinction. Name the key uncertainty without demanding
   its resolution in advance. Explain any narrowing from the active request.
   Distinguish premises needed for a proposed application from those needed to
   study a phenomenon: poor reliability can undermine deployment while making
   a question about the structure of errors more consequential.
6. **Stop or continue within scope.** Question-only work ends with the statements
   and their unresolved premises, or an explanation of what still needs framing.
   When the user also requested assessment, continue to explicit
   `$research-idea-evaluation` for question-value assessment. When approach
   development is requested, use `$research-ideation`; an obvious observational
   approach can instead go directly to the appropriate study workflow once its
   scope and resources are established. No extra approval ceremony is implied.

## Useful completion

The reader should understand what answering the question could teach, why it
matters and how evidence might bear on it. A problem statement need not contain
a new algorithm, final metric, experiment count or complete budget. A failure
collection, list of literature gaps or fashionable combination is only material
until its connection to a worthwhile question is explained.

Do not force a winner or a contribution-type quota. Preserve unresolved alternatives
when judgment is premature. New tasks and metrics require a reason the distinction
matters; explaining an established success can be worthwhile without either.
Question development supports a value argument; comparative investment judgment
belongs to evaluation. An important question and a promising proposed solution
are separate judgments.
