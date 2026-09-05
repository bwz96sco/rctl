"""The M1 command surface and a single JSON response envelope."""

import argparse
import json
import sys

from . import __version__
from .context import context
from .documents import RctlError, invalid
from .records import Task, project_root, select_task


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise invalid(message)


def parser():
    result = Parser(
        prog="rctl",
        description="Research contracts and readable state (M1; structure only).",
    )
    result.add_argument("--root")
    result.add_argument("--format", choices=("text", "json"), default="text")
    result.add_argument("--version", action="version", version=f"rctl {__version__}")
    commands = result.add_subparsers(dest="command", required=True)
    task = commands.add_parser("task").add_subparsers(
        dest="task_command", required=True
    )
    new = task.add_parser("new", help="Create a draft; fill placeholders before begin.")
    new.add_argument("task")
    new.add_argument("--kind", choices=("exploration", "analysis"), required=True)
    new.add_argument("--title", required=True)
    contract = commands.add_parser("contract").add_subparsers(
        dest="contract_command", required=True
    )
    contract.add_parser(
        "check", help="Validate structure, without executing criteria."
    ).add_argument("task")
    for name in ("begin", "amend", "checkpoint", "status", "context"):
        command = commands.add_parser(name)
        command.add_argument("task", **({"nargs": "?"} if name == "context" else {}))
        if name == "amend":
            command.add_argument("--reason", required=True)
        if name == "checkpoint":
            command.add_argument("--file", required=True)
    return result


def dispatch(args):
    root = project_root(args.root)
    task = Task(root, select_task(root, args.task))
    if args.command == "task":
        return task.new(args.kind, args.title), []
    if args.command == "contract":
        _, data = task.contract()
        return {
            "task_id": task.task_id,
            "check": "structure",
            "valid": True,
            "criterion_ids": [item["id"] for item in data["criteria"]],
        }, [
            "Structural validity does not establish scientific adequacy or verification."
        ]
    if args.command == "begin":
        return task.begin(), []
    if args.command == "amend":
        return task.amend(args.reason), []
    if args.command == "checkpoint":
        return task.checkpoint(args.file), []
    if args.command == "status":
        return task.status()
    return context(task)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    json_mode = any(
        value == "--format=json"
        or (value == "--format" and argv[i + 1 : i + 2] == ["json"])
        for i, value in enumerate(argv)
    )
    response = {
        "schema_version": 1,
        "ok": True,
        "data": {},
        "error": None,
        "warnings": [],
    }
    exit_code = 0
    args = None
    try:
        args = parser().parse_args(argv)
        response["data"], response["warnings"] = dispatch(args)
    except RctlError as error:
        response["ok"] = False
        response["error"] = {
            "code": error.code,
            "message": error.message,
            "next_action": error.next_action,
        }
        exit_code = error.exit_code
        if args and args.command == "context":
            response["data"] = {
                "available": False,
                "context": f"rctl context unavailable: {error.message}\n{error.next_action}",
            }
    except OSError as error:
        response["ok"] = False
        response["error"] = {
            "code": "NOT_FOUND",
            "message": f"File operation failed: {error.strerror}.",
            "next_action": "Inspect task status, paths, and permissions before retrying.",
        }
        exit_code = 3
    except Exception:
        response["ok"] = False
        response["error"] = {
            "code": "INTERNAL_ERROR",
            "message": "Unexpected internal failure.",
            "next_action": "Inspect task status and report the failing command.",
        }
        exit_code = 70
    if json_mode:
        print(json.dumps(response, ensure_ascii=False))
    elif "context" in response["data"]:
        print(response["data"]["context"])
    else:
        for key, value in response["data"].items():
            print(f"{key}: {value}")
        for warning in response["warnings"]:
            print(f"Warning: {warning}")
    if response["error"]:
        error = response["error"]
        print(
            f"{error['code']}: {error['message']} {error['next_action']}",
            file=sys.stderr,
        )
    return exit_code
