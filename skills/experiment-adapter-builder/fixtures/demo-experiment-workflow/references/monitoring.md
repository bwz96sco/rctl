# Monitoring

## backend_status_checks

Check local process exit code and output file timestamps.

## logs

Primary log: `runs/demo-fixture/train.log`.

## metrics

Primary metric: `demo_accuracy`.

## tracker_sources

No external tracker in fixture.

## structured_outputs

`runs/demo-fixture/metrics.json`

## raw_numbers_summary

Report raw `demo_loss` and `demo_accuracy` before interpretation.

## status_values

running: process still active.

completed: metrics parsed.

failed: nonzero exit or missing metrics.

blocked: preflight failure.

inconclusive: logs exist but metrics cannot be parsed.

## cost_or_cleanup_risks

Low; local fixture only.

## unknowns

None for fixture.
