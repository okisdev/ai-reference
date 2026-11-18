"""List skill invocation episodes from every harness store on this machine, or hash installed skill folders.

episodes.py episodes --skills a,b,c [--days 7] [--exclude <session id>]
episodes.py hashes [<skills root>...]

Both print JSON to stdout and read only. Run on another machine with `ssh <host> python3 - <args> < episodes.py`.
"""
import glob
import hashlib
import json
import os
import re
import socket
import sys
import time

HOME = os.path.expanduser("~")
INSTALLED_ROOTS = [HOME + "/.agents/skills", HOME + "/.claude/skills", HOME + "/.codex/skills"]


def text_of(content):
    if isinstance(content, str):
        return content
    parts = []
    for block in content or []:
        if isinstance(block, dict) and block.get("type") in ("text", "input_text", "output_text"):
            parts.append(block.get("text", ""))
    return "\n".join(parts)


def claude_episodes(path, skills, host):
    users, calls = [], []
    for number, line in enumerate(open(path, errors="ignore"), 1):
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if number <= 3 and row.get("isSidechain"):
            return []
        message = row.get("message") or {}
        if row.get("type") == "user" and not row.get("isMeta"):
            content = message.get("content")
            if isinstance(content, list) and content and isinstance(content[0], dict) and content[0].get("type") == "tool_result":
                continue
            text = text_of(content)
            if not text.strip() or text.startswith("<system-reminder") or "Base directory for this skill" in text:
                continue
            command = re.search(r"<command-name>/?([\w:-]+)</command-name>", text)
            if command and command.group(1).split(":")[-1] in skills:
                calls.append((number, command.group(1).split(":")[-1], text[:300]))
            else:
                users.append((number, text))
        elif row.get("type") == "assistant":
            for block in message.get("content") or []:
                if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                    tool_input = block.get("input") or {}
                    name = str(tool_input.get("skill", "")).split(":")[-1]
                    if name in skills:
                        calls.append((number, name, str(tool_input.get("args", ""))[:300]))
    project = os.path.basename(os.path.dirname(path))
    return [dict(host=host, harness="claude", file=path, line=number, project=project, skill=name, args=args,
                 ask=[(n, t[:400]) for n, t in users if n < number][-1:],
                 next=[(n, t[:400]) for n, t in users if n > number][:3])
            for number, name, args in calls]


def read_calls(path, harness):
    """Yield (line, command text) for each tool call the agent made."""
    for number, line in enumerate(open(path, errors="ignore"), 1):
        if "SKILL.md" not in line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if harness == "codex":
            payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
            if row.get("type") == "response_item" and payload.get("type") in ("function_call", "custom_tool_call", "local_shell_call"):
                yield number, json.dumps(payload.get("arguments") or payload.get("input") or payload.get("action") or "")
        elif row.get("type") == "assistant":
            for call in row.get("tool_calls") or []:
                yield number, str(call.get("arguments", ""))


READ = re.compile(r"(?:\b(?:cat|head|tail|nl|less|bat|sed -n '[^']*'|sed -n \S+)\s+(?:-\S+\s+)*|\bopen\(|target_file\W+|file_path\W+)['\"]?[^\s'\"|;&]*skills/([a-z0-9-]+)/SKILL\.md")


def peer_episodes(path, skills, host, harness, cwd):
    seen, episodes = set(), []
    for number, command in read_calls(path, harness):
        for name in READ.findall(command.replace('\\"', '"')):
            if name in skills and name not in seen:
                seen.add(name)
                episodes.append(dict(host=host, harness=harness, file=path, line=number, project=cwd, skill=name, args="", ask=[], next=[]))
    return episodes


def episodes(skills, days, exclude):
    host = socket.gethostname().split(".")[0]
    cutoff = time.time() - days * 86400
    found = []
    for path in glob.glob(HOME + "/.claude/projects/*/*.jsonl"):
        if os.path.getmtime(path) >= cutoff and not (exclude and exclude in path):
            found += claude_episodes(path, skills, host)
    for path in glob.glob(HOME + "/.codex/sessions/*/*/*/*.jsonl"):
        if os.path.getmtime(path) >= cutoff and not (exclude and exclude in path):
            first = open(path, errors="ignore").readline()
            cwd = re.search(r'"cwd":"([^"]+)"', first)
            found += peer_episodes(path, skills, host, "codex", cwd.group(1) if cwd else "")
    for path in glob.glob(HOME + "/.grok/sessions/*/*/chat_history.jsonl"):
        if os.path.getmtime(path) >= cutoff and not (exclude and exclude in path):
            cwd = os.path.basename(os.path.dirname(os.path.dirname(path))).replace("%2F", "/")
            found += peer_episodes(path, skills, host, "grok", cwd)
    for episode in found:
        episode["size"] = os.path.getsize(episode["file"])
    return found


def folder_hash(folder):
    digest = hashlib.sha256()
    for directory, names, files in os.walk(folder):
        names[:] = sorted(n for n in names if not n.startswith(".") and n != "__pycache__")
        for name in sorted(files):
            if name.startswith(".") or name.endswith(".pyc"):
                continue
            full = os.path.join(directory, name)
            digest.update(os.path.relpath(full, folder).encode())
            digest.update(open(full, "rb").read())
    return digest.hexdigest()[:12]


def hashes(roots):
    result = {}
    for root in roots:
        for skill in sorted(glob.glob(os.path.join(os.path.expanduser(root), "*", "SKILL.md"))):
            folder = os.path.dirname(skill)
            result[os.path.join(root, os.path.basename(folder))] = folder_hash(os.path.realpath(folder))
    return result


def main(argv):
    if argv[:1] == ["hashes"]:
        json.dump(hashes(argv[1:] or INSTALLED_ROOTS), sys.stdout, indent=1)
        return 0
    if argv[:1] != ["episodes"] or "--skills" not in argv:
        print(__doc__, file=sys.stderr)
        return 2
    option = lambda name, default: argv[argv.index(name) + 1] if name in argv else default
    skills = set(option("--skills", "").split(","))
    json.dump(episodes(skills, float(option("--days", "7")), option("--exclude", "")), sys.stdout, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
