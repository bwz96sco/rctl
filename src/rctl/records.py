"""Local storage and application services for the M1 lifecycle."""

import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import ValidationError

from .documents import (
    RctlError,
    invalid,
    local_path,
    parse_contract,
    read_text,
    require_completed,
    resource_text,
)
from .policy import validate_record


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def project_root(value=None):
    selected = value if value is not None else os.environ.get("RCTL_PROJECT_ROOT")
    if selected is not None and not str(selected).strip():
        raise invalid("Project root must not be empty; select an existing directory.")
    root = Path(selected if selected is not None else Path.cwd()).resolve()
    if not root.is_dir():
        raise RctlError(
            "NOT_FOUND",
            f"Project root does not exist: {root}",
            "Select an existing project root.",
            3,
        )
    return root


def select_task(root, value=None):
    value = value if value is not None else os.environ.get("RCTL_TASK_PATH")
    if not value or not value.strip():
        raise RctlError(
            "NOT_FOUND",
            "No task selected.",
            "Supply TASK or set RCTL_TASK_PATH for this session.",
            3,
        )
    return local_path(root, value)


def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=path.parent, delete=False
        ) as stream:
            temporary = Path(stream.name)
            stream.write(text)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def state_error(message):
    return RctlError(
        "STATE_REJECTED", message, "Inspect task status before the next mutation.", 4
    )


class Task:
    def __init__(self, root, path):
        self.root = root
        self.path = local_path(root, path)
        self.task_id = self.path.name

    def file(self, name):
        return local_path(self.root, name, self.path)

    def contract(self):
        path = self.file("contract.md")
        text = read_text(path)
        return text, parse_contract(text, path, self.task_id, self.root, self.path)

    def read_record(self):
        path = self.file(".rctl/record.json")
        if not path.exists() and not path.is_symlink():
            return None
        try:
            record = json.loads(read_text(path))
            self.validate_record(record)
        except (
            RctlError,
            ValidationError,
            ValueError,
            TypeError,
            KeyError,
            IndexError,
        ):
            raise RctlError(
                "RECORD_UNAVAILABLE",
                f"Malformed or unsupported record: {path}",
                "Restore a valid record; do not reset task history.",
                3,
            ) from None
        return record

    def validate_record(self, record):
        validate_record(record, self.task_id, self.file(".rctl/record.json"))

    def managed(self, phases=("active",)):
        record = self.read_record()
        if record is None:
            raise state_error("Task is an unmanaged draft; begin it first.")
        if record["phase"] not in phases:
            raise state_error(
                f"Task phase {record['phase']} does not permit this operation."
            )
        return record

    def save(self, record):
        atomic_write(
            self.file(".rctl/record.json"),
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
        )

    def new(self, kind, title):
        if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", self.task_id):
            raise invalid("Task directory basename must match [a-z0-9][a-z0-9_-]*.")
        if not title.strip():
            raise invalid("Title must contain non-whitespace text.")
        if self.path.exists():
            raise state_error("Task destination already exists.")
        text = resource_text("templates", "contract.md")
        text = text.replace("task_id: replace-task-id", f"task_id: {self.task_id}")
        text = text.replace(
            'title: "<Bounded question or deliverable>"',
            f"title: {json.dumps(title, ensure_ascii=False)}",
        )
        text = text.replace("kind: exploration", f"kind: {kind}")
        self.path.mkdir(parents=True, exist_ok=False)
        self.file("contract.md").write_text(text, encoding="utf-8")
        return {
            "task_id": self.task_id,
            "phase": "draft",
            "contract_path": str(self.file("contract.md")),
        }

    def begin(self):
        if self.read_record() is not None:
            raise state_error("Task is already managed.")
        text, _ = self.contract()
        require_completed(text, self.file("contract.md"))
        timestamp = now()
        reason = "Initial contract"
        record = {
            "schema_version": 1,
            "task_id": self.task_id,
            "phase": "active",
            "cycle": 1,
            "contracts": [
                {
                    "revision": 1,
                    "text": text,
                    "reason": reason,
                    "recorded_at": timestamp,
                }
            ],
            "verifications": [],
            "closures": [],
            "lifecycle": [
                {"action": "begin", "reason": reason, "recorded_at": timestamp}
            ],
        }
        self.save(record)
        return {"task_id": self.task_id, "phase": "active", "contract_revision": 1}

    def amend(self, reason):
        if not reason.strip():
            raise invalid("Amendment reason must contain non-whitespace text.")
        record = self.managed()
        text, _ = self.contract()
        require_completed(text, self.file("contract.md"))
        if text == record["contracts"][-1]["text"]:
            raise state_error("Contract is unchanged; no amendment to record.")
        revision = len(record["contracts"]) + 1
        timestamp = now()
        record["contracts"].append(
            {
                "revision": revision,
                "text": text,
                "reason": reason,
                "recorded_at": timestamp,
            }
        )
        record["lifecycle"].append(
            {"action": "amendment", "reason": reason, "recorded_at": timestamp}
        )
        self.save(record)
        return {
            "task_id": self.task_id,
            "phase": "active",
            "contract_revision": revision,
        }

    def checkpoint(self, source):
        record = self.managed()
        text = read_text(local_path(self.root, source))
        atomic_write(self.file("state.md"), text)
        return {
            "task_id": self.task_id,
            "phase": record["phase"],
            "state_path": str(self.file("state.md")),
        }

    def governing(self, record):
        text = read_text(self.file("contract.md"))
        if text != record["contracts"][-1]["text"]:
            raise RctlError(
                "AMENDMENT_REQUIRED",
                "Current contract differs from the governing revision.",
                "Amend the contract with a reason before dependent work.",
                4,
            )
        return text, parse_contract(
            text, self.file("contract.md"), self.task_id, self.root, self.path
        )

    def verify(self, reviews=None):
        from .verification import verify

        return verify(self, reviews)

    def close(self):
        from .documents import parse_result
        from .verification import currentness, verdict_error

        record = self.managed()
        self.governing(record)
        if not record["verifications"]:
            raise state_error(
                "No verification report; write a result and verify before close."
            )
        report = record["verifications"][-1]
        applicability, issues = currentness(self, record, readable=True)
        if applicability != "current":
            raise RctlError(
                "VERIFICATION_UNKNOWN"
                if applicability == "unknown"
                else "VERIFICATION_STALE",
                "; ".join(issues),
                "Restore/update the task materials and verify again.",
                5 if applicability == "unknown" else 4,
            )
        verdict_error(self, record, report)
        result = parse_result(
            read_text(self.file("result.md")),
            self.file("result.md"),
            self.task_id,
            report["contract_revision"],
        )
        timestamp = now()
        closure = {
            "verification_id": report["id"],
            "contract_revision": report["contract_revision"],
            "cycle": record["cycle"],
            "assessment": result["assessment"],
            "closed_at": timestamp,
        }
        record["closures"].append(closure)
        record["phase"] = "closed"
        record["lifecycle"].append(
            {
                "action": "close",
                "reason": "Current verification passed",
                "recorded_at": timestamp,
            }
        )
        self.save(record)
        return {
            "task_id": self.task_id,
            "phase": "closed",
            "closure": closure,
            "verification_id": report["id"],
        }

    def reopen(self, reason):
        return self.transition("reopen", reason)

    def cancel(self, reason):
        return self.transition("cancel", reason)

    def transition(self, action, reason):
        if not reason.strip():
            raise invalid("Lifecycle reason must contain non-whitespace text.")
        record = self.managed(
            ("closed", "cancelled") if action == "reopen" else ("active",)
        )
        if action == "reopen":
            record["cycle"] += 1
        record["phase"] = "active" if action == "reopen" else "cancelled"
        record["lifecycle"].append(
            {"action": action, "reason": reason, "recorded_at": now()}
        )
        self.save(record)
        return {
            "task_id": self.task_id,
            "phase": record["phase"],
            "cycle": record["cycle"],
        }

    def status(self):
        from .verification import currentness

        record = self.read_record()
        warnings = []
        report, closure, applicability = None, None, "not_checked"
        if record is None:
            self.contract()
            phase, revision, drift = "draft", None, False
        else:
            phase = record["phase"]
            revision = record["contracts"][-1]["revision"]
            try:
                drift = (
                    read_text(self.file("contract.md"))
                    != record["contracts"][-1]["text"]
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
            applicability, issues = currentness(self, record)
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
        return {
            "task_id": self.task_id,
            "phase": phase,
            "contract_revision": revision,
            "contract_drift": drift,
            "verification": report,
            "currentness": applicability,
            "historical_closure": closure,
            "next_action": action,
        }, warnings
