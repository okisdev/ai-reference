#!/usr/bin/env python3
"""Run skill Context probes without GitHub credentials or a GitHub remote."""
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PROBE = re.compile(r"!`([^`\n]*)`")


def probes():
    for path in sorted((REPO / "skills").glob("*/SKILL.md")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for match in PROBE.finditer(line):
                yield path.relative_to(REPO), number, match.group(1)


def git(*args, cwd, env):
    subprocess.run(["git", *args], cwd=cwd, env=env, text=True,
                   capture_output=True, check=True)


def main():
    found = list(probes())
    zsh = shutil.which("zsh")
    if not zsh:
        print("zsh not found: Context probes also run under zsh, so install it before this check")
        return 1
    shells = ["/bin/bash", zsh]
    failures = []

    with tempfile.TemporaryDirectory(prefix="check-probes-") as temporary:
        root = Path(temporary)
        environments = []
        for name in ("empty", "git-no-remote"):
            directory = root / name
            directory.mkdir()
            home = root / (name + "-home")
            home.mkdir()
            env = os.environ.copy()
            env.update({"HOME": str(home), "GH_CONFIG_DIR": str(home)})
            for variable in ("GH_TOKEN", "GITHUB_TOKEN", "GH_ENTERPRISE_TOKEN"):
                env.pop(variable, None)
            if name == "git-no-remote":
                git("init", "-q", cwd=directory, env=env)
                git("config", "user.name", "Probe Fixture", cwd=directory, env=env)
                git("config", "user.email", "probe@example.invalid", cwd=directory, env=env)
                tree = subprocess.run(["git", "mktree"], cwd=directory, env=env,
                                      input="", text=True, capture_output=True, check=True).stdout.strip()
                commit = subprocess.run(["git", "commit-tree", tree, "-m", "fixture"],
                                        cwd=directory, env=env, text=True, capture_output=True, check=True).stdout.strip()
                git("update-ref", "HEAD", commit, cwd=directory, env=env)
            environments.append((name, directory, env))

        for name, directory, env in environments:
            for path, number, command in found:
                for shell in shells:
                    with subprocess.Popen([shell, "-c", command], cwd=directory, env=env,
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          text=True, start_new_session=True) as process:
                        try:
                            _, stderr = process.communicate(timeout=15)
                        except subprocess.TimeoutExpired:
                            try:
                                os.killpg(process.pid, signal.SIGKILL)
                            except ProcessLookupError:
                                pass
                            _, stderr = process.communicate()
                            failures.append((path, number, shell, name, "timeout after 15s", stderr))
                            continue
                        if process.returncode:
                            failures.append((path, number, shell, name, str(process.returncode), stderr))

    for path, number, shell, name, status, stderr in failures:
        first_line = stderr.splitlines()[0] if stderr.splitlines() else "(no stderr)"
        print("{}:{}: {} in {}: exit status {}: {}".format(path, number, shell, name, status, first_line))
    for name in ("empty", "git-no-remote"):
        print("{}: {} probes, {} runs".format(name, len(found), len(found) * len(shells)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
