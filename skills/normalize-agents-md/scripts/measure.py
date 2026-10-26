"""Usage: measure.py [SCOPE] [--json] [--strict] | measure.py --hook.
Reports instruction files, read-path docs, chains, Next.js generators, and agent-facing READMEs.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

SKIPPED_DIRECTORIES = {"node_modules", ".git", "dist", "build", ".next", ".turbo", "vendor"}
EXACT_NAMES = {"AGENTS.md", "AGENTS.override.md", "AGENT.md", "CLAUDE.md", "CLAUDE.local.md", "GEMINI.md", ".cursorrules", "Agents.md", "Claude.md"}
MANAGED_BLOCKS = (("nextjs-agent-rules", "<!-- BEGIN:nextjs-agent-rules -->", "<!-- END:nextjs-agent-rules -->"), ("next-legacy", "<!-- NEXT-AGENTS-MD-START -->", "<!-- NEXT-AGENTS-MD-END -->"), ("ruler", "# START Ruler Generated Files", "# END Ruler Generated Files"))
NEXT_CONFIG_NAMES = {"next.config.js", "next.config.mjs", "next.config.cjs", "next.config.ts", "next.config.mts"}
README_NAMES = {"README.md", "Readme.md", "readme.md"}
MANIFEST_NAMES = {"package.json", "pyproject.toml", "Cargo.toml", "go.mod", "Package.swift"}
AGENT_SIGNAL = re.compile(r"AGENTS\.md|CLAUDE\.md|\.cursorrules|copilot-instructions|^\s*#{1,6}\s+.*\b(?:for agents|for (?:ai |coding )+agents?|instructions for agents|instructions for (?:ai |coding )+agents?|agent instructions|for claude|for codex|for cursor|for copilot|conventions?|rules|gotchas?|guidelines?|contributing)\b|^\s*(?:[-*+]\s+|\d+[.)]\s+)?(?:Never|Always|Do not|Don't|Must|You must)\b", re.IGNORECASE)
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
LIST_ITEM = re.compile(r"^\s*(?:[-*]\s+|\d+\.\s+)")
TABLE_ROW = re.compile(r"^\s*\|")
DATED_REFERENCE = re.compile(r"20\d\d-\d\d-\d\d|#\d{2,}|\b\d+(?:\.\d+)?\s*(?:seconds?|milliseconds?|ms|KB|MB|GB|%)", re.IGNORECASE)
NEXT_AGENT_RULES_OFF = re.compile(r"agentRules\s*:\s*false")
PLACEHOLDER = re.compile(r"^#\s+(?:AGENTS|AGENT|CLAUDE|GEMINI)\.md\b|This file provides guidance to|guidance for (?:Claude Code|coding agents|AI coding agents)|^\s*(?:[-*]\s*)?(?:(?-i:TODO)\b|fill (?:me )?in\b)", re.IGNORECASE | re.MULTILINE)
GROWTH_FLOOR = 256
HISTORY_PHRASES = ("used to", "once hid", "previously", "no longer", "formerly", "the failure this rule names")
READ_ORDER = re.compile(r"\bread\b[^\n]{0,120}\b(?:before|first)\b|\bbefore\b[^\n]{0,120}\bread\b|\bbefore (?:any|every|changing|editing|adding|touching)\b", re.IGNORECASE)
PRECEDENCE = re.compile(r"this file wins|where the two disagree|this file is the source of truth|\bchange to this file\b[^.\n]{0,80}\bfirst\b", re.IGNORECASE)
ACCRETION = re.compile(r"\bin the same change\b|\bchange to this file\b[^.\n]{0,80}\bfirst\b|\b(?:goes|go|added|add)\b[^\n]{0,80}\bfirst\b|\bkeep\b[^.\n]{0,80}\bin sync\b|\b(?:always|also) update\b", re.IGNORECASE)
DOC_MENTION = re.compile(r"this file|those files|README|DESIGN|\.mdx?\b|\bthe docs\b|\bdocs/", re.IGNORECASE)
STATUS_LINE = re.compile(r"\bLast updated\b|\bStatus\s*:|\b(?:as of|since|updated(?: on)?|on|(?:shipped|deployed|implemented|merged|released|landed|fixed)(?: on)?)\s+20\d\d-\d\d-\d\d\b|\(\s*20\d\d-\d\d-\d\d\s*\)|^\s*#{1,6}\s+.*20\d\d-\d\d-\d\d\b", re.IGNORECASE)
DOC_PATH = re.compile(r"(?<![\w.])(?:\.{1,2}/)*(?:[\w.\-]+/)*[\w.\-]+\.md\b")
MARKDOWN_LINK = re.compile(r"\]\(\s*<?([^\s)>]+\.md(?:#[^\s)>]*)?)>?(?:\s+[^)]*)?\)")
BACKTICK = re.compile(r"`([^`]+)`")
INLINE_SPAN = re.compile(r'(`+).*?\1|"[^"]*"')
NEGATED_CLAIM = re.compile(r"\bno longer says?\b[^.;]*", re.IGNORECASE)
SINCE_DATE = re.compile(r"(?:[0-9]{4}-[0-9]{2}-[0-9]{2}(?:[ T][0-9]{2}:[0-9]{2}(?::[0-9]{2})?)?|[0-9]+([ .])(?:seconds?|minutes?|hours?|days?|weeks?|months?|years?)\1ago)")
CODEX_CAP = 32768
GROK_CAP = 10000
DOC_TARGET = 16384
HOOK_CLOSING = "normalize-agents-md: docs state what must stay true and change when the owner decides; put what a change did in its commit or PR, replace a sentence the change made false instead of appending, and settle a file past its target before adding."


def parse_args(args):
    scope, json_output, strict, since = None, False, False, None
    position = 0
    while position < len(args):
        arg = args[position]
        if arg == "--json":
            json_output = True
        elif arg == "--strict":
            strict = True
        elif arg == "--since":
            position += 1
            if position == len(args) or args[position].startswith("--"):
                raise ValueError("--since requires a value.")
            since = args[position]
        elif arg.startswith("-"):
            raise ValueError("Unknown option: " + arg)
        elif scope is None:
            scope = arg
        else:
            raise ValueError("Only one scope may be supplied.")
        position += 1
    return Path(scope).expanduser().resolve() if scope else Path.cwd().resolve(), json_output, strict, since


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


def units_for(text):
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
    return found


def unit_metrics(text):
    lengths = [len(value) for value in units_for(text)]
    return len(lengths), max(lengths, default=0), sum(length > 600 for length in lengths)


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


def prose_lines(text):
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        match = FENCE.match(line)
        if fence:
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                fence = None
        elif match:
            fence = match.group(1)
        else:
            yield number, line, NEGATED_CLAIM.sub("", INLINE_SPAN.sub("", line))


def record_for(path, root):
    data = path.read_bytes()
    text = data.decode("utf-8", errors="replace")
    count, longest, over_600 = unit_metrics(text)
    managed = managed_blocks(text)
    flags = ["generated-only"] if not without_managed_blocks(text).strip() else []
    if "generated-only" not in flags and PLACEHOLDER.search(without_managed_blocks(text)):
        flags.append("placeholder")
    return {"path": relative_path(path, root), "bytes": len(data), "chars": len(text), "lines": len(text.splitlines()), "symlink_target": os.readlink(path) if path.is_symlink() else None, "managed_blocks": managed, "imports": import_count(text), "stub": text.strip() == "@AGENTS.md", "units": count, "longest_unit": longest, "units_over_600": over_600, "dated_references": len(DATED_REFERENCE.findall(text)), "history_phrases": sum(line.lower().count(phrase) for _, _, line in prose_lines(text) for phrase in HISTORY_PHRASES), "accretion_orders": accretion_lines(text), "status_lines": status_count(text), "flags": flags}


def accretion_lines(text):
    return [number for number, _, line in prose_lines(text) if is_accretion_order(line)]


def is_accretion_order(line):
    return any(ACCRETION.search(sentence) and DOC_MENTION.search(sentence) for sentence in re.split(r"[.!?]\s+", line))


def status_count(text):
    return sum(bool(STATUS_LINE.search(line)) for _, _, line in prose_lines(text))


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


def referenced_docs(line, source, root):
    values = [match.group(1) for match in MARKDOWN_LINK.finditer(line)]
    values.extend(match.group(1) for match in BACKTICK.finditer(line))
    values.extend(match.group() for match in DOC_PATH.finditer(line))
    found = set()
    for value in values:
        value = value.split("#", 1)[0]
        if not value.endswith(".md"):
            continue
        for base in (source.parent, root):
            path = (base / value).resolve()
            if eligible_doc(path, root):
                found.add(path)
                break
    return found


def required_referenced_docs(line, source, root):
    return {target for sentence in re.split(r"[.!?]\s+", line)
            if READ_ORDER.search(NEGATED_CLAIM.sub("", INLINE_SPAN.sub("", sentence)))
            for target in referenced_docs(sentence, source, root)}


def eligible_doc(path, root):
    try:
        resolved = path.resolve()
        parts = resolved.relative_to(root).parts
    except ValueError:
        return False
    return (resolved.suffix == ".md" and resolved.is_file()
            and not any(part in SKIPPED_DIRECTORIES for part in parts[:-1])
            and not is_instruction_file(resolved, root))


def markdown_candidates(scope, root, in_repository):
    if in_repository:
        result = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "*.md"], cwd=root, capture_output=True, check=False)
        paths = (root / os.fsdecode(name) for name in result.stdout.split(b"\0") if name) if result.returncode == 0 else ()
    else:
        def walked():
            for base, names, files in os.walk(scope, topdown=True, followlinks=False):
                names[:] = [name for name in names if name not in SKIPPED_DIRECTORIES]
                yield from (Path(base) / name for name in files if name.endswith(".md"))

        paths = walked()
    candidates = set()
    for path in paths:
        resolved = path.resolve()
        try:
            resolved.relative_to(scope)
        except ValueError:
            continue
        if resolved.is_file():
            candidates.add(resolved)
    return candidates


def doc_record(path, root, required, pointed_by):
    record = record_for(path, root)
    record["flags"] = []
    record["required"] = required
    record["pointed_by"] = sorted(pointed_by)
    if record["bytes"] > DOC_TARGET:
        if required:
            record["flags"].append("over-target")
        elif pointed_by:
            record["flags"].append("pointed-over-target")
    return record


def discover_docs(scope, root, instruction_paths, in_repository):
    docs = {}
    candidates = {path for path in markdown_candidates(scope, root, in_repository) if eligible_doc(path, root)}
    for path in instruction_paths:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for number, raw, _ in prose_lines(text):
            required = required_referenced_docs(raw, path, root)
            for target in referenced_docs(raw, path, root):
                if target not in candidates:
                    continue
                entry = docs.setdefault(target, {"required": False, "pointed_by": set()})
                entry["required"] |= target in required
                entry["pointed_by"].add("{}:{}".format(relative_path(path, root), number))
    for path in candidates:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if any(PRECEDENCE.search(line) for _, _, line in prose_lines(text)):
            docs.setdefault(path, {"required": False, "pointed_by": set()})["required"] = True
    records = []
    for path, entry in docs.items():
        try:
            records.append(doc_record(path, root, entry["required"], entry["pointed_by"]))
        except OSError:
            continue
    return sorted(records, key=lambda record: record["path"])


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


def doc_lines(docs):
    lines = ["", "| doc | required | pointed by | bytes | longest unit | units over 600 | accretion orders | status lines | flags |", "| --- | --- | --- | ---: | ---: | ---: | --- | ---: | --- |"]
    for doc in docs:
        lines.append("| {path} | {required} | {pointed} | {bytes} | {longest} | {over} | {orders} | {status} | {flags} |".format(
            path=doc["path"].replace("|", "\\|"), required=str(doc["required"]).lower(),
            pointed=", ".join(doc["pointed_by"]) or "none", bytes=doc["bytes"],
            longest=doc["longest_unit"], over=doc["units_over_600"],
            orders=", ".join(map(str, doc["accretion_orders"])) or "none",
            status=doc["status_lines"], flags=", ".join(doc["flags"]) or "none"))
    return lines


def large_doc_lines(large_docs):
    lines = ["", "| large doc off the agent path | bytes |", "| --- | ---: |"]
    lines.extend("| {} | {} |".format(doc["path"].replace("|", "\\|"), doc["bytes"]) for doc in large_docs)
    return lines


def docs_summary(summary):
    return " {read_path_docs} read-path docs, {required_docs} required, {docs_over_target} over target, {pointed_over_target} pointed over target, {accretion_orders} accretion orders.".format(**summary)


def apply_flags(records, actual_paths, chains, root):
    codex_files = {chain["files"][-1] for chain in chains if chain["bytes"] > CODEX_CAP and chain["files"]}
    has_agents = any(path.name == "AGENTS.md" for path in actual_paths.values())
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
        if has_agents and path.name in {"CLAUDE.md", "CLAUDE.local.md"}:
            flags.append("claude-md")
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


def markdown(records, chains, generators, readmes, docs, large_docs, summary):
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
    if docs:
        lines.extend(doc_lines(docs))
    if large_docs:
        lines.extend(large_doc_lines(large_docs))
    lines.extend(["", "{instruction_files} instruction files, {over_hard_cap} over a hard cap, {over_target} over target, {claude_md} CLAUDE files keeping Claude Code off AGENTS.md.".format(**summary)])
    if generators:
        lines[-1] += " {count} generators, {on} on, {blocks} with a block.".format(count=len(generators), on=sum(generator["state"] == "on" for generator in generators), blocks=sum(generator["block"] != "none" for generator in generators))
    if readmes:
        lines[-1] += " {count} READMEs carry agent-facing lines.".format(count=len(readmes))
    lines[-1] += docs_summary(summary)
    lines[-1] += " {large_docs} large docs off the agent path.".format(**summary)
    return "\n".join(lines)


def resolve_since(value, root, in_repository):
    if not in_repository:
        raise ValueError("Cannot resolve --since: " + value)
    if SINCE_DATE.fullmatch(value) and value[4:5] == "-":
        try:
            datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Cannot resolve --since: " + value)
    try:
        result = subprocess.run(["git", "rev-parse", "--verify", "--quiet", value + "^{commit}"], cwd=root, capture_output=True, text=True, check=False)
        ref = result.stdout.strip() if result.returncode == 0 else ""
        if not ref and SINCE_DATE.fullmatch(value):
            result = subprocess.run(["git", "rev-list", "-1", "--before=" + value, "HEAD"], cwd=root, capture_output=True, text=True, check=False)
            ref = result.stdout.strip() if result.returncode == 0 else ""
        if not ref:
            raise ValueError("Cannot resolve --since: " + value)
        date = subprocess.run(["git", "show", "-s", "--format=%cs", ref], cwd=root, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        raise ValueError("Cannot resolve --since: " + value)
    return ref, date


def growth_report(scope, root, ref, date, records, docs, large_docs, in_repository):
    instruction_paths = {record["path"] for record in records}
    paths = instruction_paths | {doc["path"] for doc in docs + large_docs}
    paths.update(relative_path(path, root) for path in markdown_candidates(scope, root, in_repository)
                 if eligible_doc(path, root) and path.name in {"README.md", "DESIGN.md", "ARCHITECTURE.md"})
    result = subprocess.run(["git", "ls-tree", "-r", "-l", "-z", ref], cwd=root, capture_output=True, check=True)
    historic = set()
    for entry in result.stdout.split(b"\0"):
        if not entry:
            continue
        header, name = entry.split(b"\t", 1)
        mode, kind, _, size = header.split()
        if kind != b"blob":
            continue
        path = root / os.fsdecode(name)
        try:
            path.relative_to(scope)
        except ValueError:
            continue
        if any(part in SKIPPED_DIRECTORIES for part in path.relative_to(root).parts[:-1]):
            continue
        historic.add(relative_path(path, root))
        if is_instruction_file(path, root):
            instruction_paths.add(relative_path(path, root))
            paths.add(relative_path(path, root))
        elif path.suffix == ".md" and (path.name in {"README.md", "DESIGN.md", "ARCHITECTURE.md"} or size != b"-" and int(size) > DOC_TARGET):
            paths.add(relative_path(path, root))
    for name in instruction_paths & historic:
        result = subprocess.run(["git", "show", "{}:{}".format(ref, name)], cwd=root, capture_output=True, check=False)
        if result.returncode:
            continue
        source = root / name
        for _, line, _ in prose_lines(result.stdout.decode("utf-8", errors="replace")):
            values = [match.group(1) for match in MARKDOWN_LINK.finditer(line)]
            values.extend(match.group(1) for match in BACKTICK.finditer(line))
            values.extend(match.group() for match in DOC_PATH.finditer(line))
            for value in values:
                value = value.split("#", 1)[0]
                if not value.endswith(".md"):
                    continue
                for base in (source.parent, root):
                    target = (base / value).resolve()
                    try:
                        target.relative_to(scope)
                    except ValueError:
                        continue
                    candidate = relative_path(target, root)
                    if candidate in historic and not is_instruction_file(target, root):
                        paths.add(candidate)
                        break
    rows = []
    for name in paths:
        path = root / name
        now = path.lstat().st_size if path.is_file() or path.is_symlink() else 0
        result = subprocess.run(["git", "cat-file", "-s", "{}:{}".format(ref, name)], cwd=root, capture_output=True, text=True, check=False)
        then = int(result.stdout.strip()) if result.returncode == 0 else 0
        rows.append({"path": name, "then": then, "now": now, "change": now - then})
    rows.sort(key=lambda row: (-abs(row["change"]), row["path"]))
    return {"ref": ref, "date": date, "rows": rows,
            "instruction_change": sum(row["change"] for row in rows if row["path"] in instruction_paths),
            "doc_change": sum(row["change"] for row in rows if row["path"] not in instruction_paths)}


def growth_lines(since):
    lines = ["", "| file | bytes then | bytes now | change |", "| --- | ---: | ---: | ---: |"]
    lines.extend("| {} | {} | {} | {:+d} |".format(row["path"].replace("|", "\\|"), row["then"], row["now"], row["change"]) for row in since["rows"][:25])
    lines.append("")
    lines.append("Since {} ({}): instruction files {:+d} bytes, docs {:+d} bytes, {} files changed.".format(since["ref"][:7], since["date"], since["instruction_change"], since["doc_change"], sum(row["change"] != 0 for row in since["rows"])))
    return lines


def added_lines(lines, original):
    before = original.splitlines()
    prefix = 0
    while prefix < min(len(before), len(lines)) and before[prefix] == lines[prefix]:
        prefix += 1
    suffix = 0
    while suffix < min(len(before), len(lines)) - prefix and before[-suffix - 1] == lines[-suffix - 1]:
        suffix += 1
    old_end = len(before) - suffix
    new_end = len(lines) - suffix
    matcher = SequenceMatcher(None, before[prefix:old_end], lines[prefix:new_end], autojunk=False)
    return [(prefix + number + 1, lines[prefix + number]) for tag, _, _, start, end in matcher.get_opcodes()
            if tag in {"insert", "replace"} for number in range(start, end)]


def added_edit_lines(lines, old_string, new_string):
    new_lines = new_string.splitlines()
    old_remaining = {}
    for line in old_string.splitlines():
        old_remaining[line] = old_remaining.get(line, 0) + 1
    wanted = []
    for line in new_lines:
        if old_remaining.get(line, 0):
            old_remaining[line] -= 1
        else:
            wanted.append(line)
    if new_lines:
        starts = [number for number in range(len(lines) - len(new_lines) + 1) if lines[number:number + len(new_lines)] == new_lines]
        if len(starts) == 1:
            remaining = {}
            for line in wanted:
                remaining[line] = remaining.get(line, 0) + 1
            added = []
            for number, line in enumerate(new_lines, starts[0] + 1):
                if remaining.get(line, 0):
                    remaining[line] -= 1
                    added.append((number, line))
            return added
    remaining = {}
    for line in wanted:
        remaining[line] = remaining.get(line, 0) + 1
    added = []
    for number, line in enumerate(lines, 1):
        if remaining.get(line, 0):
            remaining[line] -= 1
            added.append((number, line))
    return added


def patch_files(command):
    if not isinstance(command, str):
        return None
    lines = command.splitlines()
    if len(lines) < 3 or lines[0] != "*** Begin Patch" or lines[-1] != "*** End Patch":
        return None
    sections = []
    section = None
    hunk = False
    body = lines[1:-1]
    after_eof = False
    for position, line in enumerate(body):
        match = re.fullmatch(r"\*\*\* (Add|Update|Delete) File: (.+)", line)
        if match:
            section = {"operation": match.group(1), "path": match.group(2), "source_path": match.group(2), "chunks": []}
            sections.append(section)
            hunk = match.group(1) == "Add"
            after_eof = False
        elif section is None:
            return None
        elif line.startswith("*** Move to: ") and section["operation"] == "Update" and not hunk:
            section["path"] = line[len("*** Move to: "):]
        elif line.startswith("@@") and section["operation"] == "Update":
            section["chunks"].append([])
            hunk = True
            after_eof = False
        elif line == "*** End of File" and section["operation"] == "Update" and hunk:
            after_eof = True
        elif line == "" and (after_eof or not any(body[position + 1:])):
            continue
        elif section["operation"] == "Add" and line.startswith("+"):
            if not section["chunks"]:
                section["chunks"].append([])
            section["chunks"][-1].append(("+", line[1:]))
        elif section["operation"] == "Update" and (line[:1] in {"+", "-", " "} or line == ""):
            if not section["chunks"]:
                section["chunks"].append([])
            hunk = True
            after_eof = False
            section["chunks"][-1].append((line[:1] if line else " ", line[1:] if line else ""))
        else:
            return None
    if not sections or any(not section["path"].strip() for section in sections):
        return None
    return sections


def patch_original(text, sections):
    if any(section["operation"] == "Add" for section in sections):
        return ""
    lines = text.splitlines(keepends=True)
    cursor = 0
    for section in sections:
        for chunk in section["chunks"]:
            new = [value for sign, value in chunk if sign != "-"]
            old = [value for sign, value in chunk if sign != "+"]
            plain = [line.rstrip("\r\n") for line in lines]
            start = next((index for index in range(cursor, len(lines) - len(new) + 1) if plain[index:index + len(new)] == new), None)
            if start is None:
                start = next((index for index in range(len(lines) - len(new) + 1) if plain[index:index + len(new)] == new), None)
            if start is None:
                return None
            matched = lines[start:start + len(new)]
            ending = "\r\n" if any(line.endswith("\r\n") for line in matched) else "\n"
            replacement = [value + ending for value in old]
            if matched and not matched[-1].endswith(("\r", "\n")) and replacement:
                replacement[-1] = old[-1]
            lines[start:start + len(new)] = replacement
            cursor = start + len(replacement)
    return "".join(lines)


def is_store_file(path):
    parent = path.parent
    return (path.suffix == ".md" and parent.name == "memory"
            and parent.parent.parent.name == "projects"
            and parent.parent.parent.parent.name == ".claude")


def hook_class(path, root, text):
    ignored = subprocess.run(["git", "check-ignore", "-q", "--", relative_path(path, root)], cwd=root, check=False)
    if ignored.returncode == 0:
        return None
    if is_instruction_file(path, root):
        return "instruction"
    if any(PRECEDENCE.search(line) for _, _, line in prose_lines(text)):
        return "required"
    pointed = False
    directory = path.parent
    while True:
        for name in ("AGENTS.md", "AGENTS.override.md", "CLAUDE.md"):
            source = directory / name
            if not source.is_file():
                continue
            for _, raw, _ in prose_lines(source.read_text(encoding="utf-8", errors="replace")):
                if path in referenced_docs(raw, source, root):
                    if path in required_referenced_docs(raw, source, root):
                        return "required"
                    pointed = True
        if directory == root:
            break
        directory = directory.parent
    if pointed:
        return "pointed"
    return "person" if path.name in README_NAMES | {"DESIGN.md", "ARCHITECTURE.md"} else None


def hook_findings(path, root, text, data, original, added, kind, original_size=None):
    findings = []
    prose = {number: line for number, _, line in prose_lines(text)}
    for number, _ in added:
        if number not in prose:
            continue
        line = prose[number]
        if STATUS_LINE.search(line):
            findings.append((number, "status-line", "added status line"))
        if is_accretion_order(line):
            findings.append((number, "accretion-order", "added accretion order"))
        if kind == "instruction" or kind == "required" and path.name not in README_NAMES:
            if any(phrase in line.lower() for phrase in HISTORY_PHRASES):
                findings.append((number, "history", "added history phrase"))
    if original_size is None and original is not None:
        original_size = len(original.encode("utf-8"))
    if original_size is not None:
        target = (8192 if path.parent == root else 5120) if kind == "instruction" else DOC_TARGET
        if len(data) > target and len(data) - original_size >= GROWTH_FLOOR:
            findings.append((0, "over-target", "{} bytes (target {})".format(len(data), target)))
    if kind == "instruction" or kind == "required" and path.name not in README_NAMES:
        added_numbers = {number for number, _ in added}
        for unit in units_for(text):
            if len(unit) <= 600:
                continue
            number = text[:text.find(unit)].count("\n") + 1
            if original is not None and unit in original:
                continue
            if original is None and not any(line in added_numbers for line in range(number, number + unit.count("\n") + 1)):
                continue
            findings.append((number, "long-unit", "{} characters (limit 600)".format(len(unit))))
    return findings


def check_hook():
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            return 0
        tool_name = payload.get("tool_name", payload.get("toolName"))
        tool_input = payload.get("tool_input", payload.get("toolInput"))
        response = payload.get("tool_response", payload.get("toolResult"))
        if not isinstance(tool_input, dict) or not ("tool_response" in payload or "toolResult" in payload):
            return 0
        targets = []
        if tool_name == "apply_patch":
            cwd = payload.get("cwd")
            if not isinstance(response, str) or not isinstance(cwd, str) or not Path(cwd).is_absolute():
                return 0
            sections = patch_files(tool_input.get("command"))
            if sections is None:
                return 0
            grouped = {}
            for section in sections:
                path = Path(section["path"])
                if not path.is_absolute():
                    path = Path(cwd) / path
                if section["operation"] != "Delete":
                    grouped.setdefault(path.resolve(), []).append(section)
            targets.extend((path, None, "patch", parts) for path, parts in grouped.items())
        elif tool_name in {"Edit", "Write"} and isinstance(response, dict) and "filePath" in response and "originalFile" in response:
            input_path = tool_input.get("file_path")
            response_path = response["filePath"]
            original = response["originalFile"]
            if not isinstance(input_path, str) or not isinstance(response_path, str) or not isinstance(original, (str, type(None))):
                return 0
            targets.append((Path(response_path).expanduser().resolve(), original, "claude", tool_input))
        elif tool_name in {"search_replace", "hashline_edit", "Edit", "Write"}:
            input_path = next((tool_input[key] for key in ("file_path", "target_file", "path") if isinstance(tool_input.get(key), str)), None)
            if not input_path:
                return 0
            path = Path(input_path).expanduser()
            if not path.is_absolute():
                base = payload.get("cwd") or payload.get("workspaceRoot")
                if not isinstance(base, str) or not Path(base).is_absolute():
                    return 0
                path = Path(base) / path
            old = tool_input.get("old_string", tool_input.get("find"))
            new = tool_input.get("new_string", tool_input.get("replace"))
            content = tool_input.get("content", tool_input.get("contents"))
            if isinstance(old, str) and isinstance(new, str):
                targets.append((path.resolve(), None, "grok_edit", (old, new)))
            elif isinstance(content, str):
                targets.append((path.resolve(), None, "grok_write", None))
            else:
                return 0
        else:
            return 0
        output = []
        for path, original, source, details in targets:
            if path.suffix != ".md" or is_store_file(path) or not path.is_file():
                continue
            root, in_repository = repository_root(path.parent)
            if not in_repository or any(part in SKIPPED_DIRECTORIES for part in path.relative_to(root).parts[:-1]):
                continue
            data = path.read_bytes()
            text = data.decode("utf-8", errors="replace")
            lines = text.splitlines()
            kind = hook_class(path, root, text)
            if kind is None:
                continue
            original_size = None
            if source == "patch":
                original = patch_original(text, details)
                if original is None:
                    continue
                added = added_lines(lines, original)
            elif source == "claude":
                if original is not None:
                    added = added_lines(lines, original)
                elif tool_name == "Write":
                    added = list(enumerate(lines, 1))
                    original = ""
                else:
                    old = details.get("old_string")
                    new = details.get("new_string")
                    if not isinstance(old, str) or not isinstance(new, str):
                        return 0
                    added = added_edit_lines(lines, old, new)
                    original = text.replace(new, old, 1) if text.count(new) == 1 else None
            elif source == "grok_edit":
                old, new = details
                if text.count(new) == 1:
                    original = text.replace(new, old, 1)
                    added = added_lines(lines, original)
                else:
                    added = added_edit_lines(lines, old, new)
                    original_size = len(data) - len(new.encode("utf-8")) + len(old.encode("utf-8"))
            else:
                added = list(enumerate(lines, 1))
            for number, rule, detail in hook_findings(path, root, text, data, original, added, kind, original_size):
                output.append("{}:{}: {}: {}".format(relative_path(path, root), number, rule, detail))
        for line in output:
            print(line, file=sys.stderr)
        if output:
            print(HOOK_CLOSING, file=sys.stderr)
            return 2
    except Exception:
        return 0
    return 0


def main():
    if sys.argv[1:] == ["--hook"]:
        return check_hook()
    try:
        scope, json_output, strict, since_value = parse_args(sys.argv[1:])
    except ValueError as error:
        print("Measure.py: " + str(error), file=sys.stderr)
        return 2
    if not scope.is_dir():
        print("Measure.py: Scope is not a directory: " + str(scope), file=sys.stderr)
        return 2
    root, in_repository = repository_root(scope)
    try:
        ref, date = resolve_since(since_value, root, in_repository) if since_value is not None else (None, None)
    except ValueError as error:
        print("Measure.py: " + str(error), file=sys.stderr)
        return 2
    records, paths, generator_paths, readme_paths = discover(scope, root, in_repository)
    docs = discover_docs(scope, root, paths.values(), in_repository)
    read_path_names = {doc["path"] for doc in docs}
    large_docs = sorted(({"path": relative_path(path, root), "bytes": path.stat().st_size}
                         for path in markdown_candidates(scope, root, in_repository)
                         if eligible_doc(path, root) and relative_path(path, root) not in read_path_names and path.stat().st_size > DOC_TARGET),
                        key=lambda doc: (-doc["bytes"], doc["path"]))
    directories = {path.parent for path in paths.values() if path.name in {"AGENTS.md", "AGENTS.override.md"}}
    chains = sorted((chain_for(directory, root) for directory in directories), key=lambda chain: chain["directory"])
    apply_flags(records, paths, chains, root)
    generators = discover_generators(generator_paths, root, records)
    readmes = discover_readmes(readme_paths, root)
    records.sort(key=lambda record: (-record["bytes"], record["path"]))
    summary = {"instruction_files": len(records), "over_hard_cap": sum("grok-cap" in record["flags"] or "codex-chain" in record["flags"] for record in records), "over_target": sum("over-target" in record["flags"] for record in records), "claude_md": sum("claude-md" in record["flags"] for record in records), "read_path_docs": len(docs), "required_docs": sum(doc["required"] for doc in docs), "docs_over_target": sum("over-target" in doc["flags"] for doc in docs), "pointed_over_target": sum("pointed-over-target" in doc["flags"] for doc in docs), "large_docs": len(large_docs), "accretion_orders": sum(len(record["accretion_orders"]) for record in records + docs)}
    since = growth_report(scope, root, ref, date, records, docs, large_docs, in_repository) if ref else None
    if json_output:
        output = {"root": str(root), "scope": str(scope), "files": records, "chains": chains, "generators": generators, "readmes": readmes, "docs": docs, "large_docs": large_docs, "summary": summary}
        if since:
            output["since"] = since
        print(json.dumps(output, ensure_ascii=False))
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
        if docs:
            print("\n".join(doc_lines(docs)))
        if large_docs:
            print("\n".join(large_doc_lines(large_docs)))
        if docs or large_docs:
            print("\n" + docs_summary(summary).strip() + " {large_docs} large docs off the agent path.".format(**summary))
    else:
        print(markdown(records, chains, generators, readmes, docs, large_docs, summary))
    if since and not json_output:
        print("\n".join(growth_lines(since)))
    return 1 if strict and summary["over_hard_cap"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
