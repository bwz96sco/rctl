"""Required goal judgments for new work, without a scientific verdict engine."""

from urllib.parse import urlsplit

from .documents import RctlError, invalid, local_path, read_text, sections

GOAL_SOURCE = "research/PROGRAM.md"


def project_goal(root):
    path = local_path(root, GOAL_SOURCE)
    if not path.exists():
        return None
    # Reuse the reminder reader's treatment of unfinished goals.
    from .project_context import read_project

    sections(read_text(path))
    project, _ = read_project(root)
    return project["goal"]


def validate_goal_contribution(contract, root=None, task=None, *, required=False):
    contribution = contract.get("goal_contribution")
    goal = project_goal(root) if root is not None and required else None
    if required and goal and contribution is None:
        raise invalid(
            "This project has a research goal. Declare goal_contribution and its "
            "required review criterion before begin/amend."
        )
    if contribution is None:
        return
    criteria = {criterion["id"]: criterion for criterion in contract["criteria"]}
    key = contribution["review_criterion"]
    criterion = criteria.get(key)
    if criterion is None or criterion["method"]["type"] != "review":
        raise invalid(f"goal_contribution.review_criterion must name a review: {key}.")
    if root is not None:
        if required and not goal:
            raise invalid("Complete research/PROGRAM.md / Goal before declaring goal_contribution.")
        # verify records the Goal section itself; citing PROGRAM.md is optional.
        refs = {
            local_path(root, ref, task)
            for ref in criterion["evidence_refs"]
            if not urlsplit(ref).scheme
        }
        result = local_path(root, "result.md", task)
        if result not in refs:
            raise invalid(
                f"{key}: goal review must cite result.md using a task-relative evidence path."
            )
        if not refs - {result, local_path(root, GOAL_SOURCE)} and not any(
            urlsplit(ref).scheme for ref in criterion["evidence_refs"]
        ):
            raise invalid(f"{key}: goal review must also cite primary task evidence.")


def validate_goal_review(check, contract, source):
    contribution = contract.get("goal_contribution")
    is_goal_review = contribution and check["criterion_id"] == contribution["review_criterion"]
    if is_goal_review and "goal_impact" not in check:
        raise invalid(
            f"{source}: {check['criterion_id']} requires goal_impact with claim "
            "consequence, remaining gap and a justified next investment decision."
        )
    if not is_goal_review and "goal_impact" in check:
        raise invalid(f"{source}: goal_impact must belong to the declared goal review.")


def record_reviewed_goal(root, check):
    """Retain the Goal a supplied goal review was judged against."""
    try:
        goal = project_goal(root)
    except RctlError as error:
        goal, reason = None, error.message
    else:
        reason = f"{GOAL_SOURCE} / Goal is missing or unfinished."
    if goal is None:
        check["verdict"] = "unknown"
        check["rationale"] += f" Project Goal unavailable: {reason}"
    else:
        check["reviewed_goal"] = goal


def goal_currentness(root, report):
    """Return (stale, unknown) issues when the reviewed Goal no longer applies."""
    reviewed = [c["reviewed_goal"] for c in report["checks"] if "reviewed_goal" in c]
    if not reviewed:
        return [], []
    try:
        goal = project_goal(root)
    except RctlError:
        return [], [f"Cannot read the project Goal: {GOAL_SOURCE}."]
    if goal != reviewed[0]:
        return ["Project Goal changed since the goal review; review it again."], []
    return [], []


def scaffold_goal_contribution(text, root):
    guide_start = text.index("# task new enables the following block")
    start = text.index("# goal_contribution:")
    end = text.index("\ncriteria:", start)
    if not project_goal(root):
        return text[:guide_start] + text[end:]
    declaration = "\n".join(line.removeprefix("# ") for line in text[start:end].splitlines())
    text = text[:guide_start] + declaration + text[end:]
    criterion = (
        "  - id: AC-02\n"
        "    requirement: Assess the goal obligation against actual evidence and justify the next investment.\n"
        '    evidence_refs: [result.md, "<Primary task evidence file>"]\n'
        "    failure_action: Supply the missing goal judgment or correct unsupported continuation.\n"
        "    method: {type: review, reviewer: either}\n"
    )
    return text.replace("\n---\n", "\n" + criterion + "---\n", 1)
