# Research Inventory

This file records verified availability, not desired future state. Use `verified`, `unavailable`, or `audit_required`; cite concrete evidence for every `verified` entry.

## Datasets

| Resource ID | Location or owner | Availability | Verification evidence | Access or use constraints |
|---|---|---|---|---|
| `<dataset-id>` | `<path, system, or owner>` | `audit_required` | `<command, manifest, record, or pending audit>` | `<license, privacy, format, or none>` |

## Checkpoints and Models

| Resource ID | Location or owner | Availability | Verification evidence | Compatibility or provenance |
|---|---|---|---|---|
| `<checkpoint-id>` | `<path, system, or owner>` | `audit_required` | `<record or pending audit>` | `<training origin, code revision, or unknown>` |

## Code and Environments

| Resource ID | Repository or environment | Availability | Verification evidence | Constraints |
|---|---|---|---|---|
| `<code-or-env-id>` | `<Git root, revision, or environment>` | `audit_required` | `<inspection or pending audit>` | `<runtime, dependency, or access constraint>` |

## Infrastructure

| Resource ID | Location or owner | Availability | Verification evidence | Constraints |
|---|---|---|---|---|
| `<infrastructure-id>` | `<host, scheduler, service, or owner>` | `audit_required` | `<inspection or pending audit>` | `<quota, hardware, access, or schedule>` |

## Update Policy

Update entries when availability or verification evidence changes. Keep secrets, large artifacts, raw logs, and mutable run status out of this file.
