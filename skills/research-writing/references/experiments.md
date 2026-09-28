# Experiments

Explain how the experiments answer the paper's central questions, under what conditions, and with what limits. Connect the setup, comparisons, observations, and interpretation so readers can assess the contribution. Reuse the retained experiment evidence; an unfinished experiment remains a visible gap in the draft.

## Choose sections that serve the contribution

A common structure is below. Combine, reorder, or omit parts according to the paper's claims and available evidence; the number of experiment sections is not a measure of support.

| Part | Reader's question |
|---|---|
| Experimental Setup | Which data, methods, metrics, and conditions define the comparison? |
| Main Results | What answers the central empirical question, and how does the proposed work compare with relevant baselines? |
| Ablation Study | What does each key component or design choice contribute under the tested conditions? |
| Analysis / Further Study | Where does the method work better or worse, and what helps explain its behavior? |
| Case Study / Visualization | What concrete outputs, behaviors, successes, or failures make the quantitative findings understandable? |
| Robustness / Generalization | Do the findings hold under the relevant perturbations or changes of setting? |
| Efficiency / Cost Analysis | What resources does the method require, and what trade-off accompanies its performance? |

Keep the experiments needed to assess the central contribution in the main paper. Put supporting detail in the appendix with clear pointers, within venue constraints.

## Establish the experimental conditions

Write the setup clearly enough that readers know what was compared and can interpret the results. Cover the applicable details:

- **Datasets and benchmarks:** identify the tasks, data versions, splits, selection, and preprocessing relevant to the evaluation.
- **Baselines:** identify the compared methods and versions, why they are relevant, and whether their results were reproduced or taken from a source.
- **Metrics:** define what is measured, how scores are aggregated, and which direction indicates improvement.
- **Implementation:** state the model and consequential implementation choices, with extended details in the appendix when needed.
- **Training and inference:** report the settings and parameters that affect the comparison, including resource budgets where relevant.
- **Repetition and statistics:** state the actual number of runs, seeds or sampling procedure, summary statistics, and uncertainty when available. Define error bars and statistical tests used in the displays.
- **Comparability:** explain the data, information, assistance, tuning, and budget available to each method. Disclose consequential differences and limit the interpretation accordingly.

Retain the details needed to judge fairness in the main text. Missing repetitions or uncertainty estimates remain an evidence limitation; prose cannot supply them. Writing the section does not itself authorize additional experiments.

## Make the main results answer the question

Identify the main table or figure and tell readers what to look for. A useful paragraph introduces the comparison, describes the consequential observation, and explains what it supports under the stated conditions.

For a claimed improvement, explain which methods are compared, where the gain appears, its magnitude and uncertainty when available, and which contribution it supports. Include settings with small gains, no gain, or worse performance when they affect the conclusion. For other contribution types, organize the results around the empirical question they answer.

Select important, representative, or informative observations for detailed discussion. Give the reader an interpretation beyond a table pointer or a list of scores, while keeping that emphasis faithful to the complete result. Use evaluative language that the evidence warrants: practical benefit, consistency, sensitivity, or a trade-off each needs a concrete basis. Reserve statistical significance for an appropriate reported analysis.

## Explain design choices and behavior

Connect each ablation to a design motivation from Method. State what is removed, replaced, or varied, what comparison isolates its contribution, and what the result establishes. Examples include a component, training objective, prompt, retrieval, memory, ranking strategy, data amount, model size, or training configuration. Choose variations for the question they test.

Distinguish a component's measured contribution from a complete explanation of why the method works. If a variant also changes resources or other consequential conditions, explain the resulting limit on attribution.

Use analysis to investigate behavior beyond the main score: sample categories, task difficulty, data or model scale, error types, sensitivity to hyperparameters, prompts, retrieval count or context length, and agreement with human or expert judgments. Explain when the method helps, why the observations might arise, and where it remains inadequate. Separate observed patterns from explanations still requiring evidence.

## Use cases and displays to clarify the findings

Use case studies when numbers alone cannot explain output quality, differences between methods, task difficulty, or failure behavior. Explain what each case illustrates and how it was selected. A compelling example illustrates a pattern; it does not establish its prevalence.

Read [figure-planning.md](figure-planning.md) for display selection, placement, captions, and drafting with placeholders. Explicitly refer readers to each relevant figure or table, then interpret the important observation in the surrounding text. Keep captions and prose complementary. Available evidence can support prose before the display is rendered; pending results remain marked as pending.

## Draft and check

Report unexpected results, anomalies, and failures with their conditions and consequences for the claim. Calibrated wording should express the actual uncertainty, rather than make an unfavorable result seem smaller. Distinguish an observed problem from an untested explanation.

- **Support:** the central empirical claims have relevant comparisons and traceable results.
- **Conditions:** readers can identify the setup, comparison differences, repetitions, and uncertainty that matter.
- **Interpretation:** the text explains consequential findings, including exceptions, without repeating every value or claiming more than the study establishes.
- **Coherence:** ablations address design motivations, further analysis adds understanding, and displays agree with the prose and the paper's contribution.
