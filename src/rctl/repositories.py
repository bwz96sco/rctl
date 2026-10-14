"""Project Git roots and independent repositories inside code/paper containers."""

import shutil
import subprocess
from pathlib import Path

from .documents import RctlError, invalid, local_path


def git(path, *arguments):
    result = subprocess.run(
        ["git", "-C", str(path), *arguments], capture_output=True, text=True
    )
    if result.returncode:
        raise RctlError(
            "GIT_ERROR",
            f"Git failed in {path}: {result.stderr.strip() or result.stdout.strip()}",
            "Inspect the repository and permissions, then rerun rctl init.",
            3,
        )
    return result.stdout.strip()


def plan_repositories(root, code_repos, paper_repos):
    """Check repository destinations and Git availability before scaffold writes."""
    if shutil.which("git") is None:
        raise RctlError(
            "NOT_FOUND", "rctl init requires Git on PATH.", "Install Git and retry.", 3
        )
    paths = [root]
    for container, names in (("code", code_repos), ("paper", paper_repos)):
        directory = local_path(root, container)
        if directory != root / container:
            raise invalid(f"{container}/ must be a directory at the project root.")
        if (directory / ".git").exists():
            raise invalid(
                f"{container}/ is already a repository; review its layout before "
                f"using it as a container for {container}/<name>/ repositories."
            )
        for name in names:
            if (
                not name.strip()
                or name in {".", "..", ".git"}
                or "/" in name
                or "\\" in name
            ):
                raise invalid("Repository name must be one directory name.")
            path = local_path(root, f"{container}/{name}")
            if path != directory / name:
                raise invalid("Repository destination must not be a directory alias.")
            if path not in paths:
                paths.append(path)
    for path in paths:
        marker = path / ".git"
        if marker.exists():
            # A .git file is valid for a worktree or an established submodule.
            if Path(git(path, "rev-parse", "--show-toplevel")).resolve() != path:
                raise invalid(f"Expected a Git working tree rooted at {path}.")
    return paths


def initialize_repositories(root, paths, created, preserved):
    repositories = []
    for path in paths:
        name = path.relative_to(root).as_posix()
        marker = f"{name}/.git" if name != "." else ".git"
        if (path / ".git").exists():
            status = "preserved"
            preserved.append(marker)
        else:
            git(path, "init", "--quiet", "--initial-branch=main")
            status = "initialized"
            created.append(marker + "/")
        repositories.append({"path": name, "status": status})
    return repositories
