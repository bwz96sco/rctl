# Profiling

## profiling_triggers

## target_types

script:

process:

gpu: SM utilization, kernel launch overhead, memory bandwidth utilization

memory: allocated vs reserved vs peak, CPU-GPU redundancy, per-device balance

interconnect: CPU-GPU and GPU-GPU transfer frequency/size/bandwidth, collective communication ops, comm-to-compute ratio

framework:

cpu: context switching, utilization ratio, per-function hotspots

## tools

## instrumentation_policy

Prefer wrappers over inline edits. If inline edits are necessary, mark them with a consistent tag and track in the changelog. Minimize observer effect: sample rather than instrument tight inner loops. Collect into a structured log, not scattered prints.

## profile_output_root

## report_structure

Answer the bottleneck question with observed measurements and source locations.
Include tables or recommendations when useful; record consequential instrumentation
and cleanup state in existing evidence.

## instrumentation_changelog_required

## cleanup_policy

## unknowns
