# Method

Explain how the method works and why its main design choices address the stated problem. Give readers an overall account before the definitions, components, and procedures needed to understand it.

## Organize from overview to detail

Use this order as a starting point, adapting headings and including only stages that apply to the method:

| Part | Job |
|---|---|
| Overview | Connect the problem, core idea, component roles, and input-to-output flow. |
| Problem Formulation | Define inputs, outputs, data representation, model or function, objective, and key notation. |
| Method Details | Explain the components and how they fit together. |
| Training / Optimization | Describe the objective and how the method is trained or optimized. |
| Inference / Deployment | Explain how the method runs at test time or in use. |

Coordinate the overview with the main method figure using consistent names and connections. Read [figure-planning.md](figure-planning.md) when planning its placement, caption, or placeholder. The overview should remain understandable while the figure is being prepared.

## Explain the components and their rationale

A dedicated formulation subsection gives readers one place to find definitions before the technical details. Define symbols at first use, keep their meanings consistent, and use subscripts only for meaningful distinctions.

For each component, explain the problem it addresses, its input, the operation, its output, and the reason for that design. Make clear how its output feeds the next stage or contributes to the overall result. These points should form a connected explanation of the component's role.

## Connect equations and pseudocode to the prose

Introduce an equation by explaining why it is needed. Explain its key symbols nearby, then state what the equation does in the method. This purpose–definition–role sequence keeps the mathematics connected to the argument.

Use pseudocode when a complex procedure benefits from a compact view of the complete flow. Explain its purpose before the block and discuss consequential steps and design reasons in the surrounding text. Keep variables and operations consistent with the prose and equations.

## Make the contribution visible

Identify the concrete difference from prior methods and explain why the design is needed for the stated problem. Where useful, explain what would change without a key component. Distinguish the expected consequence from an observed effect; a design rationale alone does not establish effectiveness.

Keep this positioning concise in Method. Detailed comparisons and empirical support belong in Experiments, with claims consistent across the introduction, related work, and results.

## Draft and check

Reuse the current manuscript and established method details. Keep unresolved definitions or procedures visible in a working draft, and resolve them before treating the description as complete.

- **Flow:** the reader can follow inputs through the components to the outputs.
- **Explanation:** each key component and equation has a clear purpose and role.
- **Consistency:** notation, prose, pseudocode, and figures describe the same method; contribution claims agree with the supporting evidence.
