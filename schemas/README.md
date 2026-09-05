# Record input schemas

These Draft 2020-12 schemas define the parsed frontmatter of [contract.md](../templates/contract.md) and [result.md](../templates/result.md), plus review-input JSON. They are v0.1 input contracts, not schemas for a generic research workflow.

- [contract.schema.json](contract.schema.json): criterion structure and command/review methods.
- [result.schema.json](result.schema.json): result identity, governing revision, and scientific assessment.
- [reviews.schema.json](reviews.schema.json): attributed criterion judgments.

All three reject unknown object fields. Semantic checks additionally enforce unique criterion IDs, task identity, current contract revision, criterion coverage, allowed local paths, required headings, and governing-text equality as specified in [SPEC](../docs/SPEC.md). The machine-owned record's field contract is in SPEC §4; it is not accepted through a general import command.

Templates intentionally contain authoring placeholders and are not ready-to-begin tasks. The [example](../examples/retained-comparison/README.md) provides complete, synthetic valid inputs. A schema pass only means the input is structurally acceptable.
