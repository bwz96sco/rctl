"""Immutable derived task state and its public read projections."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .documents import (
    RctlError,
    compatibility_alignment_warning,
    parse_contract,
    parse_result,
    question_source_path,
    read_text,
)


def _freeze(value):
    from types import MappingProxyType

    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(map(_freeze, value))
    return value


def _plain(value):
    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return list(map(_plain, value))
    return value


@dataclass(frozen=True)
class TaskSnapshot:
    task_id: str
    path: str
    title: str
    question: str
    question_alignment: Mapping[str, str] | None
    assessment: Mapping[str, str | int] | None
    phase: str
    contract_revision: int | None
    contract_drift: bool
    verification: Mapping[str, Any] | None
    currentness: str
    historical_closure: Mapping[str, Any] | None
    next_action: str
    handoff: Mapping[str, str | None]
    warnings: tuple[str, ...]

    @property
    def contract_source(self) -> str:
        if self.contract_revision is None:
            return "T/contract.md (draft)"
        return "T/.rctl/record.json contracts[-1].text (accepted)"

    def _state_data(self):
        return {
            "task_id": self.task_id,
            "phase": self.phase,
            "contract_revision": self.contract_revision,
            "contract_drift": self.contract_drift,
            "assessment": _plain(self.assessment),
            "currentness": self.currentness,
            "historical_closure": _plain(self.historical_closure),
            "next_action": self.next_action,
        }

    def verification_summary(self):
        return (
            {
                key: self.verification[key]
                for key in ("id", "verdict", "contract_revision", "cycle")
            }
            if self.verification
            else None
        )

    def status(self):
        return {
            **self._state_data(),
            "title": self.title,
            "question": self.question,
            "question_alignment": _plain(self.question_alignment),
            "verification": _plain(self.verification),
            "handoff": _plain(self.handoff),
        }

    def discovery(self):
        report = self.verification_summary()
        return {
            "title": self.title,
            "phase": self.phase,
            "currentness": self.currentness,
            "verification": {key: report[key] for key in ("id", "verdict")}
            if report
            else None,
            "warnings": list(self.warnings),
        }

    def context_data(self, values, title):
        return {
            **self._state_data(),
            "title": title,
            "question": values.get("question") or None,
            "question_alignment": {
                key: values.get(f"alignment_{key}") or None
                for key in self.question_alignment
            }
            if self.question_alignment is not None
            else None,
            "verification": self.verification_summary(),
            "handoff": {
                key: (values.get(key) or None) if value else None
                for key, value in self.handoff.items()
            },
        }

    def identity(self):
        report = self.verification
        verification = f"{report['id']}: {report['verdict']}" if report else "none"
        closure = self.historical_closure
        historical = (
            f"{closure['verification_id']} (cycle {closure['cycle']}, {closure['assessment']})"
            if closure
            else "none"
        )
        return (
            f"Task: {self.task_id}\n"
            f"Phase: {self.phase}; governing revision: {self.contract_revision or 'none'}\n"
            f"Verification: {verification}; applicability: {self.currentness}; "
            f"historical closure: {historical}\n"
        )

    def task_fields(self):
        fields = [
            ("question", "Governing task question", self.question, "C / Question")
        ]
        if self.question_alignment is not None:
            fields.extend(
                (
                    f"alignment_{key}",
                    label,
                    self.question_alignment[key],
                    "C / Question alignment",
                )
                for key, label in (
                    ("source", "Governing question source (declared)"),
                    ("mechanism", "Governing mechanism (declared)"),
                    ("tests", "This task tests (declared)"),
                    ("does_not_decide", "This task does not decide (declared)"),
                )
            )
        if self.assessment is not None:
            assessment = self.assessment
            fields.append(
                (
                    "assessment",
                    "Task assessment",
                    f"{assessment['value']} (verification {assessment['verification_id']}; "
                    f"revision {assessment['contract_revision']}; {assessment['currentness']})",
                    "latest verification result",
                )
            )
        return fields

    def handoff_fields(self):
        label = (
            "Historical handoff"
            if self.phase in {"closed", "cancelled"}
            else "Reported handoff"
        )
        return [
            (
                key,
                f"{label} — {title}",
                self.handoff[key] or "Not recorded; read T/state.md.",
                "T/state.md",
            )
            for key, title in (("blockers", "Blockers"), ("next_action", "Next action"))
        ] + [("lifecycle", "Lifecycle action", self.next_action, "status TASK")]


def read_snapshot(task):
    from .handoff import read_handoff
    from .verification import currentness

    record = task.read_record()
    warnings = []
    report, closure, applicability = None, None, "not_checked"
    if record is None:
        _, contract = task.contract()
        phase, revision, drift = "draft", None, False
    else:
        contract = parse_contract(
            record["contracts"][-1]["text"],
            "governing contract",
            task.task_id,
            compatible_alignment=True,
            alignment_warnings=warnings,
        )
        phase = record["phase"]
        revision = record["contracts"][-1]["revision"]
        try:
            drift = (
                read_text(task.file("contract.md")) != record["contracts"][-1]["text"]
            )
        except RctlError:
            drift = True
            warnings.append(
                "Current contract is unavailable; restore it before dependent work."
            )
        if drift:
            warnings.append(
                "AMENDMENT_REQUIRED: current contract differs from the governing revision."
            )
        report = record["verifications"][-1] if record["verifications"] else None
        closure = record["closures"][-1] if record["closures"] else None
        applicability, issues = currentness(task, record)
        warnings.extend(issues)
    if report is None:
        warnings.append(
            "No verification has been recorded; structural checks and handoffs do not establish closure."
        )
    elif report["verdict"] != "pass":
        warnings.append(f"Latest verification {report['id']}: {report['verdict']}.")
    if record is None:
        action = "Complete the draft and begin."
    elif phase in {"closed", "cancelled"}:
        action = "Reopen with a reason before revising accepted work."
    elif drift:
        action = "Amend the contract with a reason before dependent work."
    elif report and report["verdict"] == "pass" and applicability == "current":
        action = "Close using the current passing verification."
    else:
        action = "Prepare the result and required evidence/reviews, then verify; checkpoint to pause."
    handoff, handoff_warnings = read_handoff(task)
    warnings.extend(handoff_warnings)
    alignment = contract["question_alignment"]
    if record is not None and alignment is not None:
        try:
            alignment_source = question_source_path(task.root, alignment["source"])
        except RctlError as error:
            warnings.append(compatibility_alignment_warning(error))
            alignment = None
        else:
            try:
                read_text(alignment_source)
            except RctlError as error:
                warnings.append(
                    "Question alignment source unavailable: "
                    f"{alignment['source']}. {error.message}"
                )
    assessment = None
    if report is not None:
        value = parse_result(
            report["result_text"],
            "latest verification result",
            task.task_id,
            report["contract_revision"],
        )["assessment"]
        assessment = {
            "value": value,
            "verification_id": report["id"],
            "contract_revision": report["contract_revision"],
            "currentness": applicability,
        }
    return TaskSnapshot(
        task_id=task.task_id,
        path=task.path.relative_to(task.root).as_posix(),
        title=contract["title"],
        question=contract["question"],
        question_alignment=_freeze(alignment),
        assessment=_freeze(assessment),
        phase=phase,
        contract_revision=revision,
        contract_drift=drift,
        verification=_freeze(report),
        currentness=applicability,
        historical_closure=_freeze(closure),
        next_action=action,
        handoff=_freeze(handoff),
        warnings=tuple(warnings),
    )
