---
status: accepted
date: 2026-09-05
---

# Start with file-based task boundaries

For the v0.1 development baseline, keep the human agreement and outcome in task-local Markdown and the CLI's acceptance record in one task-local JSON file. The pilot demonstrated that this arrangement can support fresh-session recovery and negative closeout; the immediate need is a repeatable contract/verification boundary rather than the original proposal's database-centered control system.

The trade-off is deliberately limited coordination and evidence freshness assurance in exchange for readable, portable records and a small implementation surface. A shared database becomes a candidate when real same-task concurrent writes or query volume demand it; general immutable artifact storage becomes a candidate when declared local observations are insufficient. Until then, rctl must name the actual materials and checks and keep its claims within [the documented limits](../READINESS.md#limitations).

This decision also fixes ownership: scientific interpretation lives in `result.md`; machine acceptance lives in the rctl record; reminder receipts are diagnostics. Trellis and rctl will not simultaneously own the lifecycle of a migrated task. Migration itself is outside this development baseline.
