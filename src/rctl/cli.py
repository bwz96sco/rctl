"""Local task commands and a single JSON response envelope."""

import argparse
import io
import json
import os
import sys
import traceback
from contextlib import redirect_stdout

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
        description="Research contracts, evidence verification, and task closure.",
    )
    result.add_argument("--root")
    result.add_argument("--format", choices=("text", "json"), default="text")
    result.add_argument("--version", action="version", version=f"rctl {__version__}")
    commands = result.add_subparsers(dest="command", required=True)
    initialize = commands.add_parser("init", help="Create missing project scaffolding.")
    initialize.add_argument("--vault")
    initialize.add_argument("--codex", action="store_true")
    commands.add_parser(
        "doctor", help="Inspect project assets without changing them."
    ).add_argument("--codex", action="store_true")
    update = commands.add_parser("update").add_subparsers(
        dest="update_command", required=True
    )
    candidates = update.add_parser(
        "export", help="Write update candidates, never apply them."
    )
    candidates.add_argument("directory")
    candidates.add_argument("--codex", action="store_true")
    integration = commands.add_parser("integration").add_subparsers(
        dest="host", required=True
    )
    export = integration.add_parser("codex").add_subparsers(
        dest="integration_command", required=True
    )
    export.add_parser("export").add_argument("directory")
    commands.add_parser("hook", help="Internal host reminder adapter.").add_subparsers(
        dest="host", required=True
    ).add_parser("codex")
    task = commands.add_parser("task").add_subparsers(
        dest="task_command", required=True
    )
    new = task.add_parser("new", help="Create a draft; fill placeholders before begin.")
    new.add_argument("task")
    new.add_argument("--kind", choices=("exploration", "analysis"), required=True)
    new.add_argument("--title", required=True)
    listing = task.add_parser(
        "list", help="List immediate tasks/ children without selection."
    )
    listing.add_argument("--phase", choices=("draft", "active", "closed", "cancelled"))
    contract = commands.add_parser("contract").add_subparsers(
        dest="contract_command", required=True
    )
    contract.add_parser(
        "check", help="Validate structure, without executing criteria."
    ).add_argument("task")
    for name in (
        "begin",
        "amend",
        "checkpoint",
        "status",
        "context",
        "verify",
        "close",
        "reopen",
        "cancel",
    ):
        command = commands.add_parser(name)
        command.add_argument("task", **({"nargs": "?"} if name == "context" else {}))
        if name in {"amend", "reopen", "cancel"}:
            command.add_argument("--reason", required=True)
        if name == "checkpoint":
            command.add_argument("--file", required=True)
        if name == "verify":
            command.add_argument("--reviews")
    return result


def dispatch(args):
    if sys.platform not in {"darwin", "linux"}:
        raise RctlError(
            "UNSUPPORTED_PLATFORM",
            f"rctl requires macOS or Linux (POSIX); current platform: {sys.platform}.",
            "Run rctl on macOS or Linux; Windows users can use WSL.",
        )
    root = project_root(args.root)
    if args.command == "init":
        from .initialize import initialize

        return initialize(root, args.vault, args.codex)
    if args.command == "integration":
        from .integration import export_codex

        return export_codex(root, args.directory), []
    if args.command == "doctor":
        from .maintenance import doctor

        return doctor(root, args.codex)
    if args.command == "update":
        from .maintenance import export_update

        return export_update(root, args.directory, args.codex)
    if args.command == "task" and args.task_command == "list":
        from .discovery import list_tasks

        return list_tasks(root, args.phase)
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
    if args.command == "verify":
        return task.verify(args.reviews), []
    if args.command == "close":
        return task.close(), []
    if args.command in {"reopen", "cancel"}:
        return getattr(task, args.command)(args.reason), []
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
    information = io.StringIO()
    try:
        with redirect_stdout(information):
            args = parser().parse_args(argv)
        json_mode = args.format == "json"
        if args.command == "hook":
            from .hooks.codex import main as hook_main

            return hook_main(args.root)
        response["data"], response["warnings"] = dispatch(args)
    except SystemExit as result:
        if result.code:
            raise
        response["data"] = {"message": information.getvalue().rstrip()}
    except RctlError as error:
        response["ok"] = False
        response["data"] = error.data
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
        if os.environ.get("RCTL_DEBUG") == "1":
            traceback.print_exc(file=sys.stderr)
        response["ok"] = False
        response["error"] = {
            "code": "INTERNAL_ERROR",
            "message": "Unexpected internal failure.",
            "next_action": (
                "Inspect task status before retrying; set RCTL_DEBUG=1 to include "
                "a traceback on stderr when reproducing the failure."
            ),
        }
        exit_code = 70
    if json_mode:
        print(json.dumps(response, ensure_ascii=False))
    elif "context" in response["data"]:
        print(response["data"]["context"])
    elif "message" in response["data"]:
        print(response["data"]["message"])
    elif "tasks" in response["data"]:
        rows = response["data"]["tasks"]
        if not rows:
            print("No tasks found under tasks/.")
        for row in rows:
            report = row["verification"]
            verdict = f"{report['id']} {report['verdict']}" if report else "none"
            print(
                f"{row['path']} | {row['title'] or '(unavailable)'} | {row['phase'] or 'unavailable'} | verification: {verdict} | {row['currentness']}"
            )
            for warning in row["warnings"]:
                print(f"  Warning: {warning}")
            if row["error"]:
                error = row["error"]
                print(f"  {error['code']}: {error['message']} {error['next_action']}")
    elif "findings" in response["data"]:
        data = response["data"]
        print(f"Project: {data['root']}; rctl {data['rctl_version']}")
        print(
            f"Codex: {'project configuration inspected; trust/delivery not inspected' if data['codex_inspected'] else 'not inspected (use --codex)'}"
        )
        print(f"Review needed: {data['review_needed']}")
        for item in data["findings"]:
            print(
                f"{item['status']}: {item['path']} — {item['message']} Next: {item['next_action']}"
            )
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
