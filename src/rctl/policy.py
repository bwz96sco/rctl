"""Structural and lifecycle validation for machine-owned records (SPEC §4–7)."""

from datetime import datetime

from jsonschema import Draft202012Validator

from .documents import parse_contract, parse_result, parse_reviews


def obj(**fields):
    return {
        "type": "object",
        "properties": fields,
        "required": list(fields),
        "additionalProperties": False,
    }


def array(item):
    return {"type": "array", "items": item}


TEXT = {"type": "string", "minLength": 1, "pattern": r"\S"}
INT = {"type": "integer", "minimum": 1}
VERDICT = {"enum": ["pass", "fail", "unknown"]}
STRINGS = array(TEXT)
NULL_TEXT = {"type": ["string", "null"]}
NULL_INT = {"type": ["integer", "null"]}
EXECUTION = obj(
    argv={**array(TEXT), "minItems": 1},
    cwd=TEXT,
    started_at=TEXT,
    finished_at=TEXT,
    exit_code=NULL_INT,
    timed_out={"type": "boolean"},
    error=NULL_TEXT,
    stdout_ref=TEXT,
    stderr_ref=TEXT,
)
CHECK_BASE = dict(
    criterion_id=TEXT,
    method=TEXT,
    verdict=VERDICT,
    rationale=TEXT,
    evidence_refs={**STRINGS, "minItems": 1},
)
COMMAND_CHECK = obj(
    **{**CHECK_BASE, "method": {"const": "command"}},
    execution={"anyOf": [EXECUTION, {"type": "null"}]},
)
REVIEW_CHECK = obj(
    **{**CHECK_BASE, "method": {"const": "review"}},
    reviewer={"enum": ["agent", "operator", None]},
)
OBSERVATION = obj(
    path=TEXT,
    observation={"enum": ["present", "missing", "unreadable"]},
    size_bytes=NULL_INT,
    mtime_ns=NULL_INT,
)
REPORT = obj(
    id=TEXT,
    contract_revision=INT,
    cycle=INT,
    created_at=TEXT,
    rctl_version=TEXT,
    result_text=TEXT,
    observed_files=array(OBSERVATION),
    external_refs=STRINGS,
    subject_issues=STRINGS,
    checks=array({"oneOf": [COMMAND_CHECK, REVIEW_CHECK]}),
    verdict=VERDICT,
)
REPORT["properties"]["review_input_text"] = TEXT
CLOSURE = obj(
    verification_id=TEXT,
    contract_revision=INT,
    cycle=INT,
    assessment={
        "enum": ["supported", "not_supported", "inconclusive", "not_applicable"]
    },
    closed_at=TEXT,
)
RECORD = obj(
    schema_version={"type": "integer", "const": 1},
    task_id=TEXT,
    phase={"enum": ["active", "closed", "cancelled"]},
    cycle=INT,
    contracts={
        **array(obj(revision=INT, text=TEXT, reason=TEXT, recorded_at=TEXT)),
        "minItems": 1,
    },
    verifications=array(REPORT),
    closures=array(CLOSURE),
    lifecycle={
        **array(
            obj(
                action={"enum": ["begin", "amendment", "close", "reopen", "cancel"]},
                reason=TEXT,
                recorded_at=TEXT,
            )
        ),
        "minItems": 1,
    },
)


def aggregate(checks, issues):
    verdicts = {check["verdict"] for check in checks}
    return (
        "fail"
        if "fail" in verdicts
        else "unknown"
        if "unknown" in verdicts or issues
        else "pass"
    )


def timestamp(text):
    value = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if value.utcoffset() is None or value.utcoffset().total_seconds() != 0:
        raise ValueError("Expected a UTC timestamp")


def validate_record(record, task_id, source):
    Draft202012Validator(RECORD).validate(record)
    if record["task_id"] != task_id:
        raise ValueError("Task identity changed")
    contracts = []
    for revision, entry in enumerate(record["contracts"], 1):
        if entry["revision"] != revision:
            raise ValueError("Contract revisions must be consecutive")
        timestamp(entry["recorded_at"])
        contracts.append(parse_contract(entry["text"], source, task_id))
    reports = {}
    for index, report in enumerate(record["verifications"], 1):
        if (
            report["id"] != f"V{index:04d}"
            or report["contract_revision"] > len(contracts)
            or report["cycle"] > record["cycle"]
        ):
            raise ValueError("Invalid report identity/revision/cycle")
        timestamp(report["created_at"])
        revision = report["contract_revision"]
        contract = contracts[revision - 1]
        parse_result(report["result_text"], source, task_id, revision)
        reviews = {}
        if "review_input_text" in report:
            reviews = parse_reviews(
                report["review_input_text"], source, task_id, revision, contract
            )
        observed_paths = [entry["path"] for entry in report["observed_files"]]
        if len(observed_paths) != len(set(observed_paths)):
            raise ValueError("Duplicate file observations")
        if [c["criterion_id"] for c in report["checks"]] != [
            c["id"] for c in contract["criteria"]
        ]:
            raise ValueError("Report must enumerate each criterion in order")
        for check, criterion in zip(report["checks"], contract["criteria"]):
            if check["method"] != criterion["method"]["type"]:
                raise ValueError("Check method differs from contract")
            if not set(criterion["evidence_refs"]) <= set(check["evidence_refs"]):
                raise ValueError("Missing criterion evidence references")
            if check["method"] == "command":
                execution = check["execution"]
                if execution is None:
                    if check["verdict"] != "unknown":
                        raise ValueError("Unexecuted check cannot pass or fail")
                else:
                    if not {execution["stdout_ref"], execution["stderr_ref"]} <= set(
                        observed_paths
                    ):
                        raise ValueError("Execution logs must be observed")
                    timestamp(execution["started_at"])
                    timestamp(execution["finished_at"])
                    expected = (
                        "unknown"
                        if execution["timed_out"]
                        or execution["error"]
                        or execution["exit_code"] is None
                        else "pass"
                        if execution["exit_code"] == 0
                        else "fail"
                    )
                    if (
                        execution["argv"] != criterion["method"]["argv"]
                        or check["verdict"] != expected
                    ):
                        raise ValueError(
                            "Command verdict/argv inconsistent with execution"
                        )
            elif check["verdict"] != "unknown" and (
                check["reviewer"] is None
                or (
                    criterion["method"]["reviewer"] == "operator"
                    and check["reviewer"] != "operator"
                )
            ):
                raise ValueError("Review source cannot satisfy criterion")
            if check["method"] == "review" and check["reviewer"] is not None:
                entry = reviews[check["criterion_id"]]
                if (
                    check["reviewer"] != entry["reviewer"]
                    or check["evidence_refs"] != entry["evidence_refs"]
                    or (
                        check["verdict"] != "unknown"
                        and check["verdict"] != entry["verdict"]
                    )
                ):
                    raise ValueError("Review differs from retained judgment")
        if report["verdict"] != aggregate(report["checks"], report["subject_issues"]):
            raise ValueError("Inconsistent report verdict")
        for observation in report["observed_files"]:
            if observation["observation"] == "present":
                if (
                    observation["size_bytes"] is None
                    or observation["size_bytes"] < 0
                    or observation["mtime_ns"] is None
                ):
                    raise ValueError("Incomplete present observation")
            elif (
                observation["size_bytes"] is not None
                or observation["mtime_ns"] is not None
            ):
                raise ValueError("Invalid absent observation")
            elif not report["subject_issues"]:
                raise ValueError("Unavailable evidence must have a subject issue")
        reports[report["id"]] = report
    for closure in record["closures"]:
        report = reports[closure["verification_id"]]
        result = parse_result(
            report["result_text"], source, task_id, report["contract_revision"]
        )
        if (
            report["verdict"] != "pass"
            or any(
                closure[key] != report[key] for key in ("cycle", "contract_revision")
            )
            or closure["assessment"] != result["assessment"]
        ):
            raise ValueError("Closure does not match a passing report")
        timestamp(closure["closed_at"])
    phase, cycle, revisions, closures = None, 1, 0, 0
    for event in record["lifecycle"]:
        timestamp(event["recorded_at"])
        action = event["action"]
        if action in {"begin", "amendment"}:
            if (action == "begin" and phase is not None) or (
                action == "amendment" and phase != "active"
            ):
                raise ValueError("Invalid contract transition")
            entry = record["contracts"][revisions]
            if any(event[key] != entry[key] for key in ("reason", "recorded_at")):
                raise ValueError("Contract history does not match lifecycle")
            revisions += 1
            phase = "active"
        elif action == "reopen" and phase in {"closed", "cancelled"}:
            phase, cycle = "active", cycle + 1
        elif action == "cancel" and phase == "active":
            phase = "cancelled"
        elif action == "close" and phase == "active":
            closure = record["closures"][closures]
            if (
                closure["cycle"] != cycle
                or closure["contract_revision"] != revisions
                or closure["closed_at"] != event["recorded_at"]
            ):
                raise ValueError("Closure history does not match lifecycle")
            closures += 1
            phase = "closed"
        else:
            raise ValueError("Invalid lifecycle transition")
    if (phase, cycle, revisions, closures) != (
        record["phase"],
        record["cycle"],
        len(contracts),
        len(record["closures"]),
    ):
        raise ValueError("Lifecycle does not match record")
