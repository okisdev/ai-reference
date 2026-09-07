"""Usage: measure.py [SCOPE] [--json] [--strict]. Reports instruction files, chains, Next.js generators, and READMEs that carry agent-facing lines."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

SKIPPED_DIRECTORIES = {"node_modules", ".git", "dist", "build", ".next", ".turbo", "vendor"}
EXACT_NAMES = {"AGENTS.md", "AGENTS.override.md", "AGENT.md", "CLAUDE.md", "CLAUDE.local.md", "GEMINI.md", ".cursorrules", "Agents.md", "Claude.md"}
MANAGED_BLOCKS = (("nextjs-agent-rules", "<!-- BEGIN:nextjs-agent-rules -->", "<!-- END:nextjs-agent-rules -->"), ("next-legacy", "<!-- NEXT-AGENTS-MD-START -->", "<!-- NEXT-AGENTS-MD-END -->"), ("ruler", "# START Ruler Generated Files", "# END Ruler Generated Files"))
NEXT_CONFIG_NAMES = {"next.config.js", "next.config.mjs", "next.config.cjs", "next.config.ts", "next.config.mts"}
README_NAMES = {"README.md", "Readme.md", "readme.md"}
MANIFEST_NAMES = {"package.json", "pyproject.toml", "Cargo.toml", "go.mod", "Package.swift"}
AGENT_SIGNAL = re.compile(r"AGENTS\.md|CLAUDE\.md|\bClaude\b|\bCodex\b|\bCursor\b|\bCopilot\b|coding agents?|AI agents?|^#{1,6} .*\b(?:agents?|conventions?|rules|gotchas?|guidelines?)\b", re.IGNORECASE)
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
LIST_ITEM = re.compile(r"^\s*(?:[-*]\s+|\d+\.\s+)")
TABLE_ROW = re.compile(r"^\s*\|")
DATED_REFERENCE = re.compile(r"20\d\d-\d\d-\d\d|#\d{2,}|\b\d+(?:\.\d+)?\s*(?:seconds?|milliseconds?|ms|KB|MB|GB|%)", re.IGNORECASE)
NEXT_AGENT_RULES_OFF = re.compile(r"agentRules\s*:\s*false")
PLACEHOLDER = re.compile(r"^#\s+(?:AGENTS|AGENT|CLAUDE|GEMINI)\.md\b|This file provides guidance to|guidance for (?:Claude Code|coding agents|AI coding agents)|^\s*(?:[-*]\s*)?(?:(?-i:TODO)\b|fill (?:me )?in\b)", re.IGNORECASE | re.MULTILINE)
HISTORY_PHRASES = ("used to", "once hid", "previously", "no longer", "formerly", "the failure this rule names")
CODEX_CAP = 32768
GROK_CAP = 10000


def parse_args(args):
    scope, json_output, strict = None, False, False
    for arg in args:
        if arg == "--json":
            json_output = True
        elif arg == "--strict":
            strict = True
        elif arg.startswith("-"):
            raise ValueError("Unknown option: " + arg)
        elif scope is None:
            scope = arg
        else:
            raise ValueError("Only one scope may be supplied.")
    return Path(scope).expanduser().resolve() if scope else Path.cwd().resolve(), json_output, strict


def repository_root(scope):
    try:
        result = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=scope, capture_output=True, text=True, check=False)
    except OSError:
        return scope, False
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip()).resolve(), True
    return scope, False


def relative_path(path, root):
    value = os.path.relpath(path, root)
    return "." if value == "." else value.replace(os.sep, "/")


def ignored_directories(root, directories):
    if not directories:
        return set()
    values = "\0".join(relative_path(directory, root) for directory in directories) + "\0"
    try:
        result = subprocess.run(["git", "check-ignore", "-z", "--stdin"], cwd=root, input=values, capture_output=True, text=True, check=False)
    except OSError:
        return set()
    return {value.rstrip("/") for value in result.stdout.split("\0") if value}


def inside_ignored_directory(path, root, ignored):
    value = relative_path(path.parent, root)
    while value not in {"", "."}:
        if value in ignored:
            return True
        value = value.rsplit("/", 1)[0] if "/" in value else "."
    return False


def is_instruction_file(path, root):
    name = path.name
    if name in EXACT_NAMES:
        return True
    parts = path.relative_to(root).parts
    if len(parts) >= 2 and parts[-2:] == (".github", "copilot-instructions.md"):
        return True
    for first, second in zip(parts, parts[1:]):
        if (first, second) == (".cursor", "rules") and name.endswith(".mdc"):
            return True
        if (first, second) == (".claude", "rules") and name.endswith(".md"):
            return True
        if (first, second) == (".github", "instructions") and name.endswith(".instructions.md"):
            return True
    return False


def import_count(text):
    count, fence = 0, None
    for line in text.splitlines():
        match = FENCE.match(line)
        if fence:
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                fence = None
        elif match:
            fence = match.group(1)
        else:
            value = line.lstrip()
            count += len(value) > 1 and value[0] == "@" and not value[1].isspace()
    return count


def unit_metrics(text):
    found, current, fenced, fence = [], [], [], None

    def add(lines):
        value = "\n".join(lines).strip()
        if value:
            found.append(value)

    for line in text.splitlines():
        match = FENCE.match(line)
        if fence:
            fenced.append(line)
            if len(fenced) > 1 and match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                add(fenced)
                fence, fenced = None, []
        elif match:
            if current:
                add(current)
                current = []
            fence, fenced = match.group(1), [line]
        elif not line.strip():
            if current:
                add(current)
                current = []
        elif LIST_ITEM.match(line):
            if current:
                add(current)
            current = [line]
        elif TABLE_ROW.match(line):
            if current:
                add(current)
                current = []
            add([line])
        else:
            current.append(line)
    if current:
        add(current)
    if fenced:
        add(fenced)
    lengths = [len(value) for value in found]
    return len(found), max(lengths, default=0), sum(length > 600 for length in lengths)


def managed_blocks(text):
    return [name for name, start, end in MANAGED_BLOCKS if text.find(start) != -1 and text.find(start) < text.find(end)]


def without_managed_blocks(text):
    for _, start, end in MANAGED_BLOCKS:
        position = text.find(start)
        while position != -1:
            closing = text.find(end, position + len(start))
            if closing == -1:
                break
            text = text[:position] + text[closing + len(end):]
            position = text.find(start)
    return text


def record_for(path, root):
    data = path.read_bytes()
    text = data.decode("utf-8", errors="replace")
    count, longest, over_600 = unit_metrics(text)
    managed = managed_blocks(text)
    flags = ["generated-only"] if not without_managed_blocks(text).strip() else []
    if "generated-only" not in flags and PLACEHOLDER.search(without_managed_blocks(text)):
        flags.append("placeholder")
    return {"path": relative_path(path, root), "bytes": len(data), "chars": len(text), "lines": len(text.splitlines()), "symlink_target": os.readlink(path) if path.is_symlink() else None, "managed_blocks": managed, "imports": import_count(text), "stub": text.strip() == "@AGENTS.md", "units": count, "longest_unit": longest, "units_over_600": over_600, "dated_references": len(DATED_REFERENCE.findall(text)), "history_phrases": sum(text.lower().count(phrase) for phrase in HISTORY_PHRASES), "flags": flags}


def chain_for(directory, root):
    locations, current = [root], root
    for part in directory.relative_to(root).parts:
        current = current / part
        locations.append(current)
    files, total, truncated = [], 0, None
    for location in locations:
        override, agent = location / "AGENTS.override.md", location / "AGENTS.md"
        selected = override if override.is_file() else agent if agent.is_file() else None
        if selected is not None:
            size = len(selected.read_bytes())
            if truncated is None and total + size > CODEX_CAP:
                truncated = {"file": relative_path(selected, root), "bytes_lost": size - max(CODEX_CAP - total, 0)}
            total += size
            files.append(relative_path(selected, root))
    return {"directory": relative_path(directory, root), "bytes": total, "files": files, "truncated": truncated}


def discover(scope, root, in_repository):
    candidates, generators, readmes, directories = [], [], [], []
    for base, names, files in os.walk(scope, topdown=True, followlinks=False):
        names[:] = [name for name in names if name not in SKIPPED_DIRECTORIES]
        directory = Path(base)
        directories.extend(directory / name for name in names)
        instruction_files = [directory / name for name in files if is_instruction_file(directory / name, root)]
        candidates.extend(instruction_files)
        generators.extend(directory / name for name in files if name in NEXT_CONFIG_NAMES)
        if directory == root or instruction_files or any(name in MANIFEST_NAMES for name in files):
            readmes.extend(directory / name for name in files if name in README_NAMES)
    ignored = ignored_directories(root, directories) if in_repository else set()
    records, actual_paths = [], {}
    for path in candidates:
        if inside_ignored_directory(path, root, ignored):
            continue
        try:
            record = record_for(path, root)
        except OSError:
            continue
        records.append(record)
        actual_paths[record["path"]] = path
    return records, actual_paths, [path for path in generators if not inside_ignored_directory(path, root, ignored)], [path for path in readmes if not inside_ignored_directory(path, root, ignored)]


def discover_readmes(paths, root):
    readmes = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        agent_lines = sum(1 for line in text.splitlines() if AGENT_SIGNAL.search(line))
        if agent_lines:
            readmes.append({"path": relative_path(path, root), "bytes": len(text.encode("utf-8")), "agent_lines": agent_lines})
    return sorted(readmes, key=lambda readme: (-readme["agent_lines"], readme["path"]))


def readme_lines(readmes):
    lines = ["", "| readme | bytes | agent-facing lines |", "| --- | ---: | ---: |"]
    lines.extend("| {path} | {bytes} | {agent_lines} |".format(**readme) for readme in readmes)
    return lines


def apply_flags(records, actual_paths, chains, root):
    codex_files = {chain["files"][-1] for chain in chains if chain["bytes"] > CODEX_CAP and chain["files"]}
    for record in records:
        flags, path = record["flags"], actual_paths[record["path"]]
        if record["chars"] > GROK_CAP:
            flags.append("grok-cap")
        if record["path"] in codex_files:
            flags.append("codex-chain")
        if record["bytes"] > (8192 if path.parent == root else 5120):
            flags.append("over-target")
        if record["stub"]:
            flags.append("stub")
        if record["symlink_target"] is not None:
            flags.append("symlink")
        flags.extend("managed:" + name for name in record["managed_blocks"])
        if record["imports"]:
            flags.append("imports:" + str(record["imports"]))


def has_next_marker(path):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return any(marker in text for name, start, end in MANAGED_BLOCKS if name.startswith("next") for marker in (start, end))


def discover_generators(paths, root, records):
    records_by_path = {record["path"]: record for record in records}
    generators = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        directory = path.parent
        agent = records_by_path.get(relative_path(directory / "AGENTS.md", root))
        if agent is not None and "generated-only" in agent["flags"]:
            block = "generated-only"
        elif has_next_marker(directory / "AGENTS.md") or has_next_marker(directory / "CLAUDE.md"):
            block = "yes"
        else:
            block = "none"
        generators.append({"directory": relative_path(directory, root), "state": "off" if NEXT_AGENT_RULES_OFF.search(text) else "on", "block": block, "template": any(part in {"template", "templates"} for part in directory.relative_to(root).parts)})
    return sorted(generators, key=lambda generator: generator["directory"])


def markdown(records, chains, generators, readmes, summary):
    lines = ["| file | bytes | lines | chars | longest unit | units over 600 | dated | history | flags |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |"]
    for record in records:
        values = {"path": record["path"].replace("|", "\\|"), "bytes": record["bytes"], "lines": record["lines"], "chars": record["chars"], "longest": record["longest_unit"], "over": record["units_over_600"], "dated": record["dated_references"], "history": record["history_phrases"], "flags": ", ".join(record["flags"]) or "none"}
        lines.append("| {path} | {bytes} | {lines} | {chars} | {longest} | {over} | {dated} | {history} | {flags} |".format(**values))
    visible = [chain for chain in chains if len(chain["files"]) > 1 or chain["bytes"] > CODEX_CAP]
    if visible:
        lines.extend(["", "| directory | chain bytes | files in chain | truncated |", "| --- | ---: | ---: | --- |"])
        for chain in visible:
            truncated = "none" if chain["truncated"] is None else "{file} ({bytes_lost} bytes lost)".format(**chain["truncated"])
            lines.append("| {directory} | {bytes} | {count} | {truncated} |".format(directory=chain["directory"], bytes=chain["bytes"], count=len(chain["files"]), truncated=truncated))
    if generators:
        lines.extend(["", "| generator | state | block | template |", "| --- | --- | --- | --- |"])
        for generator in generators:
            lines.append("| {directory} | {state} | {block} | {template} |".format(directory=generator["directory"], state=generator["state"], block=generator["block"], template=str(generator["template"]).lower()))
    if readmes:
        lines.extend(readme_lines(readmes))
    lines.extend(["", "{instruction_files} instruction files, {over_hard_cap} over a hard cap, {over_target} over target.".format(**summary)])
    if generators:
        lines[-1] += " {count} generators, {on} on, {blocks} with a block.".format(count=len(generators), on=sum(generator["state"] == "on" for generator in generators), blocks=sum(generator["block"] != "none" for generator in generators))
    if readmes:
        lines[-1] += " {count} READMEs carry agent-facing lines.".format(count=len(readmes))
    return "\n".join(lines)


def main():
    try:
        scope, json_output, strict = parse_args(sys.argv[1:])
    except ValueError as error:
        print("Measure.py: " + str(error), file=sys.stderr)
        return 2
    if not scope.is_dir():
        print("Measure.py: Scope is not a directory: " + str(scope), file=sys.stderr)
        return 2
    root, in_repository = repository_root(scope)
    records, paths, generator_paths, readme_paths = discover(scope, root, in_repository)
    directories = {path.parent for path in paths.values() if path.name in {"AGENTS.md", "AGENTS.override.md"}}
    chains = sorted((chain_for(directory, root) for directory in directories), key=lambda chain: chain["directory"])
    apply_flags(records, paths, chains, root)
    generators = discover_generators(generator_paths, root, records)
    readmes = discover_readmes(readme_paths, root)
    records.sort(key=lambda record: (-record["bytes"], record["path"]))
    summary = {"instruction_files": len(records), "over_hard_cap": sum("grok-cap" in record["flags"] or "codex-chain" in record["flags"] for record in records), "over_target": sum("over-target" in record["flags"] for record in records)}
    if json_output:
        print(json.dumps({"root": str(root), "scope": str(scope), "files": records, "chains": chains, "generators": generators, "readmes": readmes, "summary": summary}, ensure_ascii=False))
    elif not records:
        print("No instruction files found under " + str(scope) + ".")
        if generators:
            print("\n| generator | state | block | template |\n| --- | --- | --- | --- |")
            for generator in generators:
                print("| {directory} | {state} | {block} | {template} |".format(directory=generator["directory"], state=generator["state"], block=generator["block"], template=str(generator["template"]).lower()))
            print("\n{count} generators, {on} on, {blocks} with a block.".format(count=len(generators), on=sum(generator["state"] == "on" for generator in generators), blocks=sum(generator["block"] != "none" for generator in generators)))
        if readmes:
            print("\n".join(readme_lines(readmes)))
            print("\n{count} READMEs carry agent-facing lines.".format(count=len(readmes)))
    else:
        print(markdown(records, chains, generators, readmes, summary))
    return 1 if strict and summary["over_hard_cap"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
