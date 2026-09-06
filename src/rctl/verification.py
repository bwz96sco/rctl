"""Bounded local checks, attributed reviews, and material applicability."""

import os
import signal
import stat
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

from . import __version__
from .documents import RctlError, local_path, parse_result, parse_reviews, read_text
from .policy import aggregate
from .records import now, state_error


def project_ref(task, ref):
    # Parsing already checks containment; observe() checks the current target again.
    # Keep the selected spelling so re-pointing an input symlink is reobserved.
    return Path(os.path.abspath(task.path / ref)).relative_to(task.root).as_posix()


def observe(root, ref, readable=False):
    observation = {
        "path": ref,
        "observation": "present",
        "size_bytes": None,
        "mtime_ns": None,
    }
    try:
        path = local_path(root, ref)
        metadata = path.stat()
        if not stat.S_ISREG(metadata.st_mode):
            raise OSError("Expected a regular file")
        if readable:
            with path.open("rb"):
                pass
        observation.update(size_bytes=metadata.st_size, mtime_ns=metadata.st_mtime_ns)
    except FileNotFoundError:
        observation["observation"] = "missing"
    except (OSError, RctlError):
        observation["observation"] = "unreadable"
    return observation


def references(task, criteria, reviews):
    local, external = [], []
    for criterion in criteria:
        refs = criterion["evidence_refs"] + criterion["method"].get("inputs", [])
        refs += reviews.get(criterion["id"], {}).get("evidence_refs", [])
        for ref in refs:
            target = external if urlsplit(ref).scheme else local
            value = ref if target is external else project_ref(task, ref)
            if value not in target:
                target.append(value)
    return local, external


def stop_group(process):
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()


def command_check(task, criterion, log_dir):
    method = criterion["method"]
    check = {
        "criterion_id": criterion["id"],
        "method": "command",
        "verdict": "unknown",
        "rationale": "Execution unavailable.",
        "evidence_refs": criterion["evidence_refs"],
        "execution": None,
    }
    unavailable = [
        ref
        for ref in method["inputs"]
        if observe(task.root, project_ref(task, ref), readable=True)["observation"]
        != "present"
    ]
    if unavailable:
        check["rationale"] = "Required input missing or unreadable: " + ", ".join(
            unavailable
        )
        return check, []
    stdout = log_dir / f"{criterion['id']}.stdout"
    stderr = log_dir / f"{criterion['id']}.stderr"
    execution = {
        "argv": method["argv"],
        "cwd": task.path.relative_to(task.root).as_posix(),
        "started_at": now(),
        "finished_at": None,
        "exit_code": None,
        "timed_out": False,
        "error": None,
        "stdout_ref": stdout.relative_to(task.root).as_posix(),
        "stderr_ref": stderr.relative_to(task.root).as_posix(),
    }
    process = None
    try:
        with stdout.open("wb") as out, stderr.open("wb") as err:
            process = subprocess.Popen(
                method["argv"],
                cwd=task.path,
                shell=False,
                stdout=out,
                stderr=err,
                start_new_session=True,
            )
            try:
                execution["exit_code"] = process.wait(timeout=method["timeout_seconds"])
            except subprocess.TimeoutExpired:
                stop_group(process)
                execution.update(
                    timed_out=True,
                    exit_code=process.returncode,
                    error=f"Timed out after {method['timeout_seconds']} seconds.",
                )
            except BaseException:
                stop_group(process)
                raise
    except OSError as exc:
        execution["error"] = (
            f"Cannot execute declared check: {exc.strerror or type(exc).__name__}."
        )
    execution["finished_at"] = now()
    if process is None:
        check["rationale"] = execution["error"]
        return check, []
    check["execution"] = execution
    check["verdict"] = (
        "unknown"
        if execution["error"]
        else "pass"
        if execution["exit_code"] == 0
        else "fail"
    )
    check["rationale"] = (
        execution["error"] or f"Declared command exited {execution['exit_code']}."
    )
    return check, [execution["stdout_ref"], execution["stderr_ref"]]


def review_check(task, criterion, entry):
    check = {
        "criterion_id": criterion["id"],
        "method": "review",
        "verdict": "unknown",
        "rationale": "Required review is missing.",
        "evidence_refs": criterion["evidence_refs"],
        "reviewer": None,
    }
    if entry is None:
        return check
    check.update(
        {
            key: entry[key]
            for key in ("verdict", "rationale", "evidence_refs", "reviewer")
        }
    )
    issues = []
    if (
        criterion["method"]["reviewer"] == "operator"
        and entry["reviewer"] != "operator"
    ):
        issues.append("An operator review is required.")
    for ref in entry["evidence_refs"]:
        if (
            not urlsplit(ref).scheme
            and observe(task.root, project_ref(task, ref), readable=True)["observation"]
            != "present"
        ):
            issues.append(f"Review evidence missing or unreadable: {ref}.")
    if issues:
        check["verdict"] = "unknown"
        check["rationale"] += " " + " ".join(issues)
    return check


def currentness(task, record, readable=False):
    if not record["verifications"]:
        return "not_checked", []
    report = record["verifications"][-1]
    stale, unknown = [], []
    if report["cycle"] != record["cycle"]:
        stale.append("Verification predates the current cycle; verify again.")
    if report["contract_revision"] != record["contracts"][-1]["revision"]:
        stale.append("Verification names an earlier contract revision.")
    if report["rctl_version"] != __version__:
        stale.append("Verification was produced by another rctl version.")
    for name, expected in (
        ("contract.md", record["contracts"][-1]["text"]),
        ("result.md", report["result_text"]),
    ):
        try:
            if read_text(task.file(name)) != expected:
                stale.append(f"Current {name} differs from verified materials.")
        except RctlError:
            if not task.file(name).exists():
                stale.append(f"Missing verified material: {name}.")
            else:
                unknown.append(f"Cannot read verified material: {name}.")
    for previous in report["observed_files"]:
        current = observe(task.root, previous["path"], readable)
        if current["observation"] == "unreadable":
            unknown.append(f"Cannot observe evidence: {previous['path']}.")
        elif current["observation"] == "missing" or current != previous:
            stale.append(f"Evidence missing or changed: {previous['path']}.")
    if stale:
        return "stale", stale + unknown
    if unknown:
        return "unknown", unknown
    return "current", []


def verdict_error(task, record, report):
    if report["verdict"] == "pass":
        return
    verdict = report["verdict"]
    contract = record["contracts"][report["contract_revision"] - 1]
    from .documents import parse_contract

    criteria = {
        c["id"]: c
        for c in parse_contract(contract["text"], "governing contract", task.task_id)[
            "criteria"
        ]
    }
    failed = [check for check in report["checks"] if check["verdict"] != "pass"]
    message = "; ".join(
        [f"{c['criterion_id']}: {c['rationale']}" for c in failed]
        + report["subject_issues"]
    )
    action = (
        " ".join(criteria[c["criterion_id"]]["failure_action"] for c in failed)
        or (
            "Prepare stable, available evidence before verify; check commands must "
            "only validate it. Amend the contract with a reason if the command "
            "must change, then verify again."
        )
    )
    raise RctlError(
        "VERIFICATION_FAILED" if verdict == "fail" else "VERIFICATION_UNKNOWN",
        message,
        action,
        4 if verdict == "fail" else 5,
        {
            "task_id": task.task_id,
            "phase": record["phase"],
            "verification_id": report["id"],
            "verdict": verdict,
            "checks": report["checks"],
        },
    )


def verify(task, reviews_file=None):
    record_path = task.file(".rctl/record.json")
    try:
        record_source = read_text(record_path)
    except RctlError as error:
        if (
            error.code == "NOT_FOUND"
            and task.path.is_dir()
            and not record_path.exists()
        ):
            raise state_error(
                "Task is an unmanaged draft; begin it before verification."
            ) from None
        raise
    record = task.managed()
    contract_text, contract = task.governing(record)
    revision = record["contracts"][-1]["revision"]
    result_text = read_text(task.file("result.md"))
    parse_result(result_text, task.file("result.md"), task.task_id, revision)
    reviews, reviews_text = {}, None
    if reviews_file is not None:
        source = local_path(task.root, reviews_file)
        reviews_text = read_text(source)
        reviews = parse_reviews(
            reviews_text, source, task.task_id, revision, contract, task.root, task.path
        )
    refs, external = references(task, contract["criteria"], reviews)
    starting = {ref: observe(task.root, ref, readable=True) for ref in refs}
    report_id = f"V{len(record['verifications']) + 1:04d}"
    checks_dir = task.file(".rctl/checks")
    checks_dir.mkdir(parents=True, exist_ok=True)
    log_dir = Path(tempfile.mkdtemp(prefix=f"{report_id}-", dir=checks_dir))
    checks, logs = [], []
    for criterion in contract["criteria"]:
        if criterion["method"]["type"] == "command":
            check, new_logs = command_check(task, criterion, log_dir)
            logs.extend(new_logs)
        else:
            check = review_check(task, criterion, reviews.get(criterion["id"]))
        checks.append(check)
    final = {
        ref: observe(task.root, ref, readable=True)
        for ref in dict.fromkeys(refs + logs)
    }
    issues = []
    for ref, observation in final.items():
        if observation["observation"] != "present":
            issues.append(f"Evidence {observation['observation']}: {ref}.")
        if ref in starting and observation != starting[ref]:
            issue = f"Evidence changed during verification: {ref}."
            declared_by = [
                check["criterion_id"]
                for check in checks
                if check["method"] == "command"
                and check["execution"] is not None
                and any(
                    not urlsplit(evidence).scheme
                    and project_ref(task, evidence) == ref
                    for evidence in check["evidence_refs"]
                )
            ]
            if declared_by:
                issue += (
                    f" Declared evidence for executed command criteria: {', '.join(declared_by)}."
                    " If a check regenerates this file, run that generation before verify"
                    " and use a check that only reads the prepared evidence."
                )
            issues.append(issue)
    for name, original in (("contract.md", contract_text), ("result.md", result_text)):
        try:
            if read_text(task.file(name)) != original:
                issues.append(f"{name} changed during verification.")
        except RctlError:
            issues.append(f"{name} became unavailable during verification.")
    report = {
        "id": report_id,
        "contract_revision": revision,
        "cycle": record["cycle"],
        "created_at": now(),
        "rctl_version": __version__,
        "result_text": result_text,
        "observed_files": list(final.values()),
        "external_refs": external,
        "subject_issues": issues,
        "checks": checks,
        "verdict": aggregate(checks, issues),
    }
    if reviews_text is not None:
        report["review_input_text"] = reviews_text
    try:
        unchanged = read_text(task.file(".rctl/record.json")) == record_source
    except RctlError:
        unchanged = False
    if not unchanged:
        raise RctlError(
            "RECORD_CHANGED",
            "Record changed during verification; report was not published.",
            "Inspect status before a new verification; existing check logs are retained.",
            6,
        )
    record["verifications"].append(report)
    task.save(record)
    verdict_error(task, record, report)
    return {
        "task_id": task.task_id,
        "phase": "active",
        "verification_id": report_id,
        "checks": checks,
        "verdict": report["verdict"],
    }
