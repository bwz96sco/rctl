"""Local storage and application services for the M1 lifecycle."""

import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .documents import (
    RctlError,
    invalid,
    local_path,
    parse_contract,
    read_text,
    require_completed,
    resource_text,
)


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
        except (RctlError, ValueError, TypeError, KeyError):
            raise RctlError(
                "RECORD_UNAVAILABLE",
                f"Malformed or unsupported record: {path}",
                "Restore a valid record; do not reset task history.",
                3,
            ) from None
        return record

    def validate_record(self, record):
        required = {
            "schema_version",
            "task_id",
            "phase",
            "cycle",
            "contracts",
            "verifications",
            "closures",
            "lifecycle",
        }
        if not isinstance(record, dict) or set(record) != required:
            raise ValueError
        if type(record["schema_version"]) is not int or record["schema_version"] != 1:
            raise ValueError
        if record["task_id"] != self.task_id:
            raise ValueError
        # This increment only writes M1 records. M2 adds verification and closure.
        if (
            record["phase"] != "active"
            or type(record["cycle"]) is not int
            or record["cycle"] != 1
        ):
            raise ValueError
        if record["verifications"] != [] or record["closures"] != []:
            raise ValueError
        contracts = record["contracts"]
        if not isinstance(contracts, list) or not contracts:
            raise ValueError
        for revision, entry in enumerate(contracts, 1):
            if not isinstance(entry, dict) or set(entry) != {
                "revision",
                "text",
                "reason",
                "recorded_at",
            }:
                raise ValueError
            if type(entry["revision"]) is not int or entry["revision"] != revision:
                raise ValueError
            if not all(
                isinstance(entry[key], str) and entry[key].strip()
                for key in ("text", "reason", "recorded_at")
            ):
                raise ValueError
            datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
            parse_contract(entry["text"], self.file(".rctl/record.json"), self.task_id)
        lifecycle = record["lifecycle"]
        if not isinstance(lifecycle, list) or len(lifecycle) != len(contracts):
            raise ValueError
        for index, entry in enumerate(lifecycle):
            if not isinstance(entry, dict) or set(entry) != {
                "action",
                "reason",
                "recorded_at",
            }:
                raise ValueError
            if entry["action"] != ("begin" if index == 0 else "amendment"):
                raise ValueError
            if (
                entry["reason"] != contracts[index]["reason"]
                or entry["recorded_at"] != contracts[index]["recorded_at"]
            ):
                raise ValueError

    def managed(self):
        record = self.read_record()
        if record is None:
            raise state_error("Task is an unmanaged draft; begin it first.")
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

    def status(self):
        record = self.read_record()
        warnings = []
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
        warnings.append(
            "No verification has been recorded; structural checks and handoffs do not establish closure."
        )
        return {
            "task_id": self.task_id,
            "phase": phase,
            "contract_revision": revision,
            "contract_drift": drift,
            "verification": None,
            "currentness": "not_checked",
            "historical_closure": None,
            "next_action": "Complete the draft and begin."
            if record is None
            else (
                "Amend the contract with a reason before dependent work."
                if drift
                else "Continue within the contract; checkpoint to save a handoff. Verification and closure require M2."
            ),
        }, warnings
