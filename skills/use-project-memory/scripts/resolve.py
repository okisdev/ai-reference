#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
PROJECTS = HOME / ".claude" / "projects"


def encode_claude_project(path: Path) -> str:
    text = str(path.resolve())
    key = "".join(ch if ch.isascii() and ch.isalnum() else "-" for ch in text)
    if len(key) <= 200:
        return key
    units = text.encode("utf-16-le")
    value = 0
    for index in range(0, len(units), 2):
        value = (value * 31 + int.from_bytes(units[index:index + 2], "little")) & 0xFFFFFFFF
    if value >= 0x80000000:
        value = 0x100000000 - value
    digits = ""
    while value:
        value, digit = divmod(value, 36)
        digits = "0123456789abcdefghijklmnopqrstuvwxyz"[digit] + digits
    return f"{key[:200]}-{digits or '0'}"


def git(cwd: Path, *args: str) -> str | None:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def main_worktree(cwd: Path) -> Path:
    porcelain = git(cwd, "worktree", "list", "--porcelain")
    if porcelain:
        for line in porcelain.splitlines():
            if line.startswith("worktree "):
                return Path(line.split(" ", 1)[1]).resolve()
    common = git(cwd, "rev-parse", "--git-common-dir")
    if common:
        common_path = Path(common)
        if not common_path.is_absolute():
            common_path = (cwd / common_path).resolve()
        if common_path.name == ".git":
            return common_path.parent
    top = git(cwd, "rev-parse", "--show-toplevel")
    if top:
        return Path(top).resolve()
    return cwd.resolve()


def memory_dir_for(root: Path) -> Path:
    return PROJECTS / encode_claude_project(root) / "memory"


def resolve(cwd: Path) -> dict[str, object]:
    cwd = cwd.resolve()
    git_root = main_worktree(cwd)
    candidates: list[Path] = []
    if git_root != cwd:
        candidates.append(git_root)
    here = cwd
    while True:
        candidates.append(here)
        if here == HOME or here.parent == here:
            break
        here = here.parent

    seen: set[Path] = set()
    tried: list[str] = []
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate == HOME and cwd != HOME:
            continue
        directory = memory_dir_for(candidate)
        tried.append(str(directory))
        if (directory / "MEMORY.md").is_file():
            return {
                "cwd": str(cwd),
                "root": str(candidate),
                "dir": str(directory),
                "index": str(directory / "MEMORY.md"),
                "exists": True,
            }

    create_at = git_root if git(cwd, "rev-parse", "--is-inside-work-tree") == "true" else cwd
    directory = memory_dir_for(create_at)
    return {
        "cwd": str(cwd),
        "root": str(create_at),
        "dir": str(directory),
        "index": str(directory / "MEMORY.md"),
        "exists": False,
        "tried": tried,
    }


def main() -> int:
    as_json = False
    cwd = Path(os.environ.get("GROK_WORKSPACE_ROOT") or os.getcwd())
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in {"--json", "-j"}:
            as_json = True
            i += 1
        elif arg in {"--cwd", "-C"}:
            if i + 1 >= len(args):
                print("resolve.py: --cwd needs a path", file=sys.stderr)
                return 2
            cwd = Path(args[i + 1])
            i += 2
        elif not arg.startswith("-"):
            cwd = Path(arg)
            i += 1
        else:
            print(f"resolve.py: unknown flag {arg}", file=sys.stderr)
            return 2

    info = resolve(cwd)
    if as_json:
        print(json.dumps(info, ensure_ascii=False))
        return 0
    if info["exists"]:
        print(f"dir {info['dir']}")
        print(f"index {info['index']}")
        print(f"root {info['root']}")
    else:
        print(f"missing {info['dir']}")
        print(f"root {info['root']}")
        print("create MEMORY.md here on first write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
