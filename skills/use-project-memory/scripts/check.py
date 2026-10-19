"""Usage: check.py [FILE ...] [--dir DIR] [--json] [--strict] | check.py --hook."""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

LIMITS = {"hook_chars": 80, "topic_bytes": 4096, "index_lines": 200, "index_bytes": 25600}
INDEX_LINE = re.compile(r"^\s*[-*]\s+\[[^\]]+\]\(([^)]+\.md)\)(?:\s+(?:—|;|-)\s*(.*))?\s*$")
TYPES = {"user", "feedback", "project", "reference"}
DATED_STATUS = re.compile(
    r"\bLast updated\b|\bStatus\s*:|\b(?:as of|updated(?: on)?|on|since)\s+20\d{2}-\d{2}-\d{2}\b"
    r"|\(\s*20\d{2}-\d{2}-\d{2}\s*\)|^\s*#{1,6}\s+.*20\d{2}-\d{2}-\d{2}\b"
    r"|\b(?:shipped|deployed|implemented|merged|released|landed|fixed)\s+(?:on\s+)?20\d{2}-\d{2}-\d{2}\b",
    re.IGNORECASE,
)
DATED_DETAIL = "status and dates belong in the commit, PR, or tracker; a topic states the current fact"


def name_for(path, directory):
    try:
        return str(path.resolve().relative_to(directory.resolve()))
    except ValueError:
        return path.name


def path_for(value, directory):
    path = Path(value).expanduser()
    return path if path.is_absolute() else directory / path


def linked_file_exists(directory, value):
    try:
        path = (directory / value).resolve()
        path.relative_to(directory.resolve())
    except ValueError:
        return False
    return path.is_file()


def topic_fields(lines, end):
    values = {"name": None, "description": None, "type": None}
    metadata = None
    child_indent = None
    for line in lines[1:end]:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        content = line.lstrip()
        if indent == 0:
            metadata = None
            child_indent = None
            match = re.match(r"^(name|description)\s*:\s*(.*?)\s*$", content)
            if match:
                values[match.group(1)] = match.group(2).strip().strip("\"'")
            if re.match(r"^metadata\s*:\s*$", content):
                metadata = indent
            continue
        if metadata is None or indent <= metadata:
            continue
        if child_indent is None:
            child_indent = indent
        if indent == child_indent:
            match = re.match(r"^type\s*:\s*(.*?)\s*$", content)
            if match:
                values["type"] = match.group(1).strip().strip("\"'")
    return values


def add(violations, file, line, rule, detail):
    violations.append({"file": file, "line": line, "rule": rule, "detail": detail})


def check_dated_lines(lines, name, violations, added=None):
    frontmatter = bool(lines and lines[0].strip() == "---")
    fence = None
    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        if frontmatter:
            if number > 1 and stripped == "---":
                frontmatter = False
            continue
        marker = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence:
            if marker and marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence):
                fence = None
            continue
        if marker:
            fence = marker.group(1)
            continue
        if (added is None or number in added) and DATED_STATUS.search(line):
            add(violations, name, number, "dated-status", DATED_DETAIL)


def check_index(path, directory, violations, archive=False):
    data = path.read_bytes()
    text = data.decode("utf-8", errors="replace")
    lines = text.splitlines()
    name = "ARCHIVE.md" if archive else "MEMORY.md"
    if not archive:
        check_dated_lines(lines, name, violations)
    for number, line in enumerate(lines, 1):
        match = INDEX_LINE.match(line)
        if line.strip() and not line.lstrip().startswith("#") and not match:
            add(violations, name, number, "index-prose", "not an index entry")
        if not match:
            continue
        target, hook = match.group(1), match.group(2) or ""
        if not archive and len(hook) > LIMITS["hook_chars"]:
            add(violations, name, number, "hook-length", "{} characters (limit {})".format(len(hook), LIMITS["hook_chars"]))
        if not linked_file_exists(directory, target):
            add(violations, name, number, "orphan-line", "{} does not exist in the store".format(target))
    if not archive and (len(lines) > LIMITS["index_lines"] or len(data) > LIMITS["index_bytes"]):
        add(violations, name, None, "index-budget", "{} lines (limit {}), {} bytes (limit {})".format(len(lines), LIMITS["index_lines"], len(data), LIMITS["index_bytes"]))
    return {"lines": len(lines), "bytes": len(data)}


def indexed_paths(path, directory):
    if not path.is_file():
        return set()
    paths = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = INDEX_LINE.match(line)
        if not match:
            continue
        candidate = directory / match.group(1)
        try:
            paths.add(candidate.resolve().relative_to(directory.resolve()))
        except ValueError:
            continue
    return paths


def check_topic(path, directory, violations, archived=False, data=None):
    if data is None:
        data = path.read_bytes()
    name = name_for(path, directory)
    if not archived and len(data) > LIMITS["topic_bytes"]:
        add(violations, name, None, "topic-size", "{} bytes (limit {})".format(len(data), LIMITS["topic_bytes"]))
    lines = data.decode("utf-8", errors="replace").splitlines()
    check_dated_lines(lines, name, violations)
    if not lines or lines[0].strip() != "---":
        add(violations, name, 1, "frontmatter", "missing leading --- block")
        return
    end = next((number for number in range(1, len(lines)) if lines[number].strip() == "---"), None)
    if end is None:
        add(violations, name, 1, "frontmatter", "missing closing --- block")
        return
    values = topic_fields(lines, end)
    if not values["name"]:
        add(violations, name, None, "frontmatter", "missing name")
    if not values["description"]:
        add(violations, name, None, "frontmatter", "missing description")
    if not values["type"]:
        add(violations, name, None, "frontmatter", "missing metadata.type")
    elif values["type"] not in TYPES:
        add(violations, name, None, "frontmatter", "invalid metadata.type: {}".format(values["type"]))


def check(directory, files=None):
    directory = Path(directory).expanduser().resolve()
    index_path = directory / "MEMORY.md"
    archive_path = directory / "ARCHIVE.md"
    result = {"dir": str(directory), "checked": [], "violations": [], "index": None, "limits": LIMITS}
    if not index_path.is_file():
        return result
    if files is None:
        paths = [index_path]
        if archive_path.is_file():
            paths.append(archive_path)
        paths.extend(sorted(path for path in directory.glob("*.md") if path.is_file() and path.name not in {"MEMORY.md", "ARCHIVE.md"}))
    else:
        paths = []
        seen = set()
        for value in files:
            path = path_for(value, directory)
            try:
                key = path.resolve()
            except OSError:
                key = path
            if key not in seen and path.is_file() and path.suffix == ".md":
                seen.add(key)
                paths.append(path)
    live_paths = indexed_paths(index_path, directory)
    archived_paths = indexed_paths(archive_path, directory) - live_paths
    for path in paths:
        name = name_for(path, directory)
        if path.resolve() == index_path.resolve():
            result["checked"].append("MEMORY.md")
            result["index"] = check_index(path, directory, result["violations"])
        elif path.resolve() == archive_path.resolve():
            result["checked"].append("ARCHIVE.md")
            check_index(path, directory, result["violations"], archive=True)
        else:
            result["checked"].append(name)
            try:
                archived = path.resolve().relative_to(directory) in archived_paths
            except ValueError:
                archived = False
            check_topic(path, directory, result["violations"], archived)
    return result


def added_lines(lines, original):
    remaining = {}
    for line in original.splitlines():
        remaining[line] = remaining.get(line, 0) + 1
    added = []
    for number, line in enumerate(lines, 1):
        if remaining.get(line, 0):
            remaining[line] -= 1
        else:
            added.append((number, line))
    return added


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


def is_store_file(path):
    parent = path.parent
    canonical_store = (
        parent.name == "memory"
        and parent.parent.parent.name == "projects"
        and parent.parent.parent.parent.name == ".claude"
    )
    return path.suffix == ".md" and canonical_store


def patch_sections(command):
    lines = command.splitlines()
    if len(lines) < 3 or lines[0] != "*** Begin Patch" or lines[-1] != "*** End Patch":
        return None
    sections = []
    index = 1
    while index < len(lines) - 1:
        header = re.match(r"^\*\*\* (Add File|Update File|Delete File): (.+)$", lines[index])
        if not header:
            return None
        kind, path = header.groups()
        index += 1
        if kind == "Update File" and index < len(lines) - 1 and lines[index].startswith("*** Move to: "):
            path = lines[index][len("*** Move to: "):]
            index += 1
        if not path:
            return None
        chunks = []
        chunk = None
        ended = False
        while index < len(lines) - 1 and not re.match(r"^\*\*\* (?:Add File|Update File|Delete File): ", lines[index]):
            line = lines[index]
            if kind == "Delete File":
                return None
            if line.startswith("@@") and kind == "Update File" and not ended:
                chunk = []
                chunks.append(chunk)
            elif line == "*** End of File" and kind == "Update File" and chunk is not None:
                ended = True
            elif line == "" and (ended or all(rest == "" for rest in lines[index + 1:-1])):
                pass
            elif ended:
                return None
            elif line.startswith("+") and kind in {"Update File", "Add File"}:
                if chunk is None:
                    chunk = []
                    chunks.append(chunk)
                chunk.append(("+", line[1:]))
            elif kind == "Update File" and (line.startswith("-") or line.startswith(" ") or line == ""):
                if chunk is None:
                    chunk = []
                    chunks.append(chunk)
                chunk.append((line[0] if line else " ", line[1:] if line else ""))
            else:
                return None
            index += 1
        if kind == "Update File" and not chunks:
            return None
        sections.append((kind, path, chunks))
    return sections or None


def added_patch_lines(lines, wanted):
    remaining = {}
    for line in wanted:
        remaining[line] = remaining.get(line, 0) + 1
    found = []
    for number, line in enumerate(lines, 1):
        if remaining.get(line, 0):
            remaining[line] -= 1
            found.append((number, line))
    return found


def original_patch_text(text, sections):
    lines = text.splitlines()
    if any(kind == "Add File" for kind, _ in sections):
        return "", list(enumerate(lines, 1))
    cursor = 0
    replacements = []
    added = []
    for _, chunks in sections:
        for chunk in chunks:
            new = [line for prefix, line in chunk if prefix != "-"]
            old = [line for prefix, line in chunk if prefix != "+"]
            start = next((at for at in range(cursor, len(lines) - len(new) + 1) if lines[at:at + len(new)] == new), None)
            if start is None:
                start = next((at for at in range(len(lines) - len(new) + 1) if lines[at:at + len(new)] == new), None)
            if start is None:
                return None, []
            offset = 0
            for prefix, line in chunk:
                if prefix != "-":
                    if prefix == "+":
                        added.append((start + offset + 1, line))
                    offset += 1
            replacements.append((start, start + len(new), old))
            cursor = start + len(new)
    for start, end, old in sorted(replacements, key=lambda item: item[0], reverse=True):
        lines[start:end] = old
    original = "\n".join(lines)
    if text.endswith("\n") and lines:
        original += "\n"
    return original, added


def check_hook_index_added(data, directory, lines, added, original_lines, original_bytes, violations):
    check_dated_lines(lines, "MEMORY.md", violations, {number for number, _ in added})
    for number, line in added:
        match = INDEX_LINE.match(line)
        if line.strip() and not line.lstrip().startswith("#") and not match:
            add(violations, "MEMORY.md", number, "index-prose", "not an index entry")
        if not match:
            continue
        target, hook = match.group(1), match.group(2) or ""
        if len(hook) > LIMITS["hook_chars"]:
            add(violations, "MEMORY.md", number, "hook-length", "{} characters (limit {})".format(len(hook), LIMITS["hook_chars"]))
        if not linked_file_exists(directory, target):
            add(violations, "MEMORY.md", number, "orphan-line", "{} does not exist in the store".format(target))
    if ((len(lines) > LIMITS["index_lines"] and len(lines) > original_lines)
            or (len(data) > LIMITS["index_bytes"] and len(data) > original_bytes)):
        add(violations, "MEMORY.md", None, "index-budget", "{} lines (limit {}), {} bytes (limit {})".format(len(lines), LIMITS["index_lines"], len(data), LIMITS["index_bytes"]))


def check_hook_index(data, directory, lines, original, tool_name, tool_input, violations):
    if original is None:
        if tool_name == "Write":
            added = list(enumerate(lines, 1))
        else:
            old_string = tool_input.get("old_string")
            new_string = tool_input.get("new_string")
            if not isinstance(old_string, str) or not isinstance(new_string, str):
                added = []
            else:
                added = added_edit_lines(lines, old_string, new_string)
    else:
        added = added_lines(lines, original)
    original_lines = len(original.splitlines()) if original is not None else 0
    original_bytes = len(original.encode("utf-8")) if original is not None else 0
    check_hook_index_added(data, directory, lines, added, original_lines, original_bytes, violations)


def check_hook():
    try:
        payload = json.load(sys.stdin)
    except (TypeError, ValueError, json.JSONDecodeError):
        return 0
    if not isinstance(payload, dict):
        return 0
    tool_name = payload.get("tool_name", payload.get("toolName"))
    tool_input = payload.get("tool_input", payload.get("toolInput"))
    response = payload.get("tool_response", payload.get("toolResult"))
    if not isinstance(tool_input, dict):
        return 0
    violations = []
    writes = []
    if tool_name == "apply_patch":
        cwd = payload.get("cwd")
        command = tool_input.get("command")
        if not isinstance(response, str) or not isinstance(cwd, str) or not Path(cwd).is_absolute() or not isinstance(command, str):
            return 0
        sections = patch_sections(command)
        if sections is None:
            return 0
        grouped = {}
        for kind, value, chunks in sections:
            if kind == "Delete File":
                continue
            path = Path(value).expanduser()
            if not path.is_absolute():
                path = Path(cwd) / path
            grouped.setdefault(path, []).append((kind, chunks))
        for path, file_sections in grouped.items():
            writes.append((path, None, file_sections, None, False, None))
    elif tool_name in {"Edit", "Write", "search_replace", "hashline_edit"}:
        if isinstance(response, dict) and "filePath" in response and "originalFile" in response and tool_name in {"Edit", "Write"}:
            value = response["filePath"]
            original = response["originalFile"]
            if not isinstance(tool_input.get("file_path"), str) or not isinstance(value, str) or not isinstance(original, (str, type(None))):
                return 0
            writes.append((Path(value).expanduser(), original, None, None, original is None, None))
        else:
            value = next((tool_input[key] for key in ("file_path", "target_file", "path") if isinstance(tool_input.get(key), str)), None)
            if value is None:
                return 0
            path = Path(value).expanduser()
            if not path.is_absolute():
                cwd = payload.get("cwd", payload.get("workspaceRoot"))
                if not isinstance(cwd, str) or not Path(cwd).is_absolute():
                    return 0
                path = Path(cwd) / path
            old = tool_input.get("old_string", tool_input.get("find"))
            new = tool_input.get("new_string", tool_input.get("replace"))
            content = tool_input.get("content", tool_input.get("contents"))
            if isinstance(old, str) and isinstance(new, str):
                writes.append((path, None, None, None, False, (old, new)))
            elif isinstance(content, str):
                writes.append((path, None, None, None, True, None))
            else:
                return 0
    else:
        return 0
    for path, original, patch_added, patch_removed, full_write, edit in writes:
        try:
            if not path.is_file():
                continue
            path = path.resolve()
            if not is_store_file(path) or path.name == "ARCHIVE.md":
                continue
            directory = path.parent
            data = path.read_bytes()
        except OSError:
            continue
        lines = data.decode("utf-8", errors="replace").splitlines()
        if patch_added is not None:
            original, added = original_patch_text(data.decode("utf-8", errors="replace"), patch_added)
            if original is None:
                continue
        elif edit is not None:
            old, new = edit
            current_text = data.decode("utf-8", errors="replace")
            if new and current_text.count(new) == 1:
                original = current_text.replace(new, old, 1)
                added = added_lines(lines, original)
            else:
                added = added_edit_lines(lines, old, new)
                original_bytes = len(data) - len(new.encode("utf-8")) + len(old.encode("utf-8"))
                original_lines = len(lines) - len(new.splitlines()) + len(old.splitlines())
        elif original is not None:
            added = added_lines(lines, original)
        else:
            added = list(enumerate(lines, 1)) if full_write else []
        if original is not None:
            original_bytes = len(original.encode("utf-8"))
            original_lines = len(original.splitlines())
        elif full_write:
            original_bytes = 0
            original_lines = 0
        if path.name == "MEMORY.md":
            check_hook_index_added(data, directory, lines, added, original_lines, original_bytes, violations)
            continue
        live_paths = indexed_paths(directory / "MEMORY.md", directory)
        archived_paths = indexed_paths(directory / "ARCHIVE.md", directory) - live_paths
        archived = path.relative_to(directory) in archived_paths
        current = []
        check_topic(path, directory, current, archived, data)
        added_numbers = {number for number, _ in added}
        current = [item for item in current if item["rule"] != "dated-status" or item["line"] in added_numbers]
        if original is not None:
            original_data = original.encode("utf-8")
            previous = []
            check_topic(path, directory, previous, archived, original_data)
            previous_rules = {(item["rule"], item["detail"]) for item in previous if item["rule"] != "dated-status"}
            current = [item for item in current if (
                item["rule"] == "topic-size" and len(data) > len(original_data)
                or item["rule"] == "dated-status"
                or item["rule"] not in {"topic-size", "dated-status"} and (item["rule"], item["detail"]) not in previous_rules
            )]
        elif not full_write:
            frontmatter_end = next((number for number, line in enumerate(lines, 1) if number > 1 and line.strip() == "---"), len(lines))
            current = [item for item in current if item["rule"] == "dated-status"
                       or item["rule"] == "topic-size" and len(data) > original_bytes
                       or item["rule"] == "frontmatter" and any(number <= frontmatter_end for number in added_numbers)]
        violations.extend(current)
    if not violations:
        return 0
    for violation in violations:
        print("{file}:{line}: {rule}: {detail}".format(**dict(violation, line=violation["line"] or 0)), file=sys.stderr)
    print("use-project-memory: rewrite what this write added to fit these limits; older lines are clean-memory's job.", file=sys.stderr)
    return 2


def resolved_directory():
    path = Path(__file__).with_name("resolve.py")
    spec = importlib.util.spec_from_file_location("memory_resolve", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return Path(module.resolve(Path.cwd())["dir"])


def parse_args(args):
    files, directory, json_output, strict = [], None, False, False
    index = 0
    while index < len(args):
        value = args[index]
        if value == "--dir":
            index += 1
            if index == len(args):
                raise ValueError("--dir needs a directory.")
            directory = Path(args[index]).expanduser()
        elif value == "--json":
            json_output = True
        elif value == "--strict":
            strict = True
        elif value.startswith("-"):
            raise ValueError("Unknown option: " + value)
        else:
            files.append(Path(value).expanduser())
        index += 1
    if directory is None:
        directory = files[0].parent if files else resolved_directory()
        if files:
            files = [path.resolve() for path in files]
    return directory.resolve(), files, json_output, strict


def main():
    if sys.argv[1:] == ["--hook"]:
        return check_hook()
    try:
        directory, files, json_output, strict = parse_args(sys.argv[1:])
    except ValueError as error:
        print("check.py: " + str(error), file=sys.stderr)
        return 2
    if not (directory / "MEMORY.md").is_file():
        print("No memory store.")
        return 0
    result = check(directory, files if files else None)
    if json_output:
        print(json.dumps(result, ensure_ascii=False))
    elif result["violations"]:
        for violation in result["violations"]:
            print("{file}:{line}: {rule}: {detail}".format(**dict(violation, line=violation["line"] or 0)))
        print("{} violations in {} files ({})".format(len(result["violations"]), len({item["file"] for item in result["violations"]}), result["dir"]))
    else:
        print("clean ({})".format(result["dir"]))
    return 1 if strict and result["violations"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
