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


def check_index(path, directory, violations, archive=False):
    data = path.read_bytes()
    text = data.decode("utf-8", errors="replace")
    lines = text.splitlines()
    name = "ARCHIVE.md" if archive else "MEMORY.md"
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


def check_topic(path, directory, violations, archived=False):
    data = path.read_bytes()
    name = name_for(path, directory)
    if not archived and len(data) > LIMITS["topic_bytes"]:
        add(violations, name, None, "topic-size", "{} bytes (limit {})".format(len(data), LIMITS["topic_bytes"]))
    lines = data.decode("utf-8", errors="replace").splitlines()
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


def check_hook_index(path, directory, lines, original, tool_name, tool_input, violations):
    if original is None:
        if tool_name == "Write":
            added = list(enumerate(lines, 1))
        else:
            old_string = tool_input.get("old_string")
            new_string = tool_input.get("new_string")
            if not isinstance(old_string, str) or not isinstance(new_string, str):
                return
            added = added_edit_lines(lines, old_string, new_string)
    else:
        added = added_lines(lines, original)
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


def check_hook():
    try:
        payload = json.load(sys.stdin)
        tool_name = payload["tool_name"]
        tool_input = payload["tool_input"]
        response = payload["tool_response"]
        input_path = tool_input["file_path"]
        response_path = response["filePath"]
        original = response["originalFile"]
    except (KeyError, TypeError, json.JSONDecodeError):
        return 0
    if tool_name not in {"Edit", "Write"} or not isinstance(input_path, str) or not isinstance(response_path, str) or not isinstance(original, (str, type(None))):
        return 0
    path = Path(response_path).expanduser()
    if not path.is_file():
        return 0
    try:
        path = path.resolve()
    except OSError:
        return 0
    if not is_store_file(path) or path.name == "ARCHIVE.md":
        return 0
    directory = path.parent
    try:
        lines = path.read_bytes().decode("utf-8", errors="replace").splitlines()
    except OSError:
        return 0
    violations = []
    if path.name == "MEMORY.md":
        check_hook_index(path, directory, lines, original, tool_name, tool_input, violations)
    else:
        live_paths = indexed_paths(directory / "MEMORY.md", directory)
        archived_paths = indexed_paths(directory / "ARCHIVE.md", directory) - live_paths
        try:
            archived = path.relative_to(directory) in archived_paths
        except ValueError:
            archived = False
        check_topic(path, directory, violations, archived)
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
