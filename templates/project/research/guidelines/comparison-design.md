# Comparison Design

Use this guidance when proposing a method comparison, changing its control,
sharing intermediate evidence, or interpreting a tie. Adapt scientific details
to the project; reuse the existing task/rapid note rather than add another gate.

## Question and comparison roles

State the primary outcome and what the experiment does not decide. Distinguish:

- A complete method starting from the declared raw inputs.
- A fixed main control and separately identified published-method baselines.
- An enhanced control receiving development lessons or case-specific assistance.
- An ablation receiving the method's generated intermediate information.
- A diagnosis or single-control screen, which does not compare a new method.

Keep method-generated records private in a complete-method comparison. Sharing
them with a control tests downstream use conditional on those records. A tie
under supplied diagnosis does not test automatic production of that diagnosis.
Controls may independently discover the same strategy using the common tools.

## Baseline identity and resources

Record an ID/version and link the source, prompt/policy, inputs, tools, model or
initialization, feedback, budget, output selection and evaluator settings. Keep
the main control fixed across the intended comparison. Add enhanced controls as
separate versions while retaining the original comparison. A necessary bug fix
marks affected evidence and reruns the relevant comparison, not the entire history.

Match raw starting resources and comparable total effort. Count work used to
generate records/candidates, or explicitly scope the question to a common retained
pool. Let controls use the corresponding allowance for their own improvement.
Record material resource differences without turning a rapid test into exact
token accounting or a full reproduction campaign.

## Development and evaluation

Known failures may support favorable rapid development. Label their selection,
manual help and training/development feedback. Fix methods and controls before
claiming transfer to held-out cases; repeated runs are not independent original
cases. Keep final evaluation feedback outside test-time improvement unless such
access is explicitly the studied setting. Evaluator access is an information
condition, not something inferred from the absence of a reference in a prompt.

Report the primary outcome, paired gains/regressions and resource costs. Keep
secondary and diagnostic metrics separate; an intermediate-quality gain cannot
silently replace a final-performance question. Separate infrastructure failures,
missing outputs, scientific failures and ambiguous reference judgments.

## Interpretation and task ownership

Compare complete methods first when pipeline benefit is the question; use
ablations to explain a signal. If shared analysis lets free processing match,
the analysis may be the useful product. A small null or conditional tie supports
a bounded investment decision, not rejection of every mechanism for a problem.

Task contracts retain the declared scope and acceptance criteria. Material
changes use an explicit amendment; a different question uses a linked task.
`rctl contract check` validates structure. Scientific adequacy requires evidence
review; an accepted record or populated template cannot establish it.
