# Development Readiness

Updated: 2026-09-06. Target: rctl v0.1.0 local release.

**M1–M4 complete.** All release cases have observed evidence in [RELEASE-VERIFICATION](RELEASE-VERIFICATION.md). The original preparation record below remains historical; it is distinct from implementation and real-host acceptance.

## Preparation completion criteria

| Item | Evidence | State |
|---|---|---|
| User priorities and corrected name are represented | README, PRD, and CONTEXT | Complete |
| Original proposal and pilot history are reconciled | SOURCES, ADR-0001, DEVELOPMENT change table | Complete |
| Every product requirement has acceptance coverage | R-01–R-12 mapped in ACCEPTANCE | Complete |
| Record, criterion, review, and result semantics are concrete | SPEC, CLI, and schemas | Complete |
| Templates and an executable synthetic example exist | templates/ and examples/retained-comparison/ | Complete |
| Local document links, schemas, examples, and mappings are checked | Preparation validation below | Passed |
| Implementation can begin without another product decision | M1 has bounded deliverable and named exit cases | Complete |

## Preparation validation

The documentation checker is `scripts/check_docs.py`. It detects broken local references, invalid schemas/example payloads, missing criterion evidence, unmapped product requirements, and inconsistent example identity/revision. Failures require repairing the docs or fixture before handoff. It is not the rctl implementation or its acceptance suite.

The synthetic arithmetic checker detects a mismatch between its declared metric direction, calculated gain, threshold, and recorded promotion label. Its execution establishes only that the example is internally coherent.

Executed successfully on 2026-09-05 with uv 0.12.3:

```sh
# From the rctl project root:
uv run --offline scripts/check_docs.py
# From examples/retained-comparison:
uv run --offline --no-project python check_arithmetic.py
```

The documentation check passed: 86 local links, seven JSON files, three schemas and their example inputs, and all 12 product requirements mapped to 20 acceptance cases. The arithmetic check passed with `gain=-0.03; promote=False`. Dependencies for the documentation checker were available from the local uv cache; no network download was needed.

Manual consistency review checked phase versus assessment, amendment/reopen invalidation, structural validation versus substantive checks, record versus handoff authority, Codex target versus historical Claude scope, and preparation versus release claims. The record now carries an explicit cycle so reopen cannot reuse an earlier report; generated check logs are included in material observations so deleted execution evidence prevents closure. No unresolved design conflict was found in those reviewed paths.

## Completed development gates

- M1: contract and state; [verification](M1-VERIFICATION.md).
- M2: execution/review, currentness, and closure; [verification](M2-VERIFICATION.md).
- M3: packaged task skill, adapter/export, official protocol recheck, and actual delivery; [verification](M3-VERIFICATION.md).
- M4: new real analysis across two fresh sessions, full suite, installed-package walkthrough, and release matrix; [verification](RELEASE-VERIFICATION.md).

Shared-skill changes, live task migration, and remote publication were not part of this release.

## Limitations

1. The old pilot reanalyzed retained aggregates. It did not establish fresh training, raw-prediction/bootstrap reproduction, independent health/contact audits, superiority over Trellis/Comet, or quantified hook benefit.
2. The release host evidence covers invocation-local Codex CLI 0.153.4 configuration, SessionStart startup and UserPromptSubmit. The original isolated project-file probe delivered no reminder. A [follow-up](PROJECT-HOOKS-VERIFICATION.md) succeeded with normal config loading and invocation-only hook-trust bypass; adding `--ignore-user-config` eliminated delivery in a controlled pair. The internal reason remains undiagnosed. Official online retrieval succeeded during M3 after the historical preparation timeout. Real compact/native resume, subagent delivery, and ordinary persisted project installation are not established here.
3. v0.1 assumes one cooperating writer per task. Atomic replacement protects one record against partial publication; the recheck is not a transactional multi-writer lock, a cross-filesystem durability guarantee, or a defense against direct record edits.
4. Contract/result text comparison is exact. Other declared local files use size/mtime observations, which do not detect changes preserving both metadata values; undeclared dependencies and remote references are outside automatic freshness observation. A current report does not certify full reproducibility or immutable artifacts.
5. Command pass proves the declared check ran successfully. Review entries record attributed judgment without authenticating a person or proving arbitrary scientific prose. A checkpoint is also a report of progress, not newly verified evidence.
6. Local source citations depend on this workstation's paths. Self-contained source summaries and synthetic fixtures permit implementation elsewhere, but the original historical evidence must be obtained separately for independent pilot auditing.
7. v0.1.0 is tested on macOS arm64 with CPython 3.11.11 and 3.13.2. Linux and other runtimes remain untested targets. Local Git work was authorized during implementation; no remote repository or host/global configuration was created or changed.
8. Version 0.1.0 implements M1–M4 and accepts the existing schema-1 records. The real release task analyzes retained host observations; it does not establish training, remote execution, or quantified research-performance benefit. Placeholder rejection detects the bundled contract template markers; scientific adequacy requires evidence-based judgment. Timeout tests establish termination of the launched local process group; interrupted-verification tests exercise SIGINT. Detached jobs are outside the checker contract, and SIGKILL/power-loss recovery is not established by those interruption tests.
