"""Usage: audit.py [REPO] [--memory DIR] [--json] [--strict] [--gh] [--stale-days N]."""
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

EXTENSIONS = (".ts", ".tsx", ".js", ".mjs", ".cjs", ".py", ".md", ".mdx", ".json", ".yaml", ".yml", ".toml", ".sh", ".css", ".swift", ".rs", ".go", ".sql", ".plist", ".entitlements")
GENERIC_NAMES = {"package.json", "README.md", "index.ts", "SKILL.md", "CLAUDE.md", "AGENTS.md", "MEMORY.md"}
STATUS_NAMES = {"SHIPPED", "CLOSED", "OPEN", "PARKED", "DISPROVEN", "SUPERSEDED", "VERIFIED", "BLOCKED"}
INDEX_LINE = re.compile(r"^\s*[-*]\s+\[[^\]]+\]\(([^)]+\.md)\)(?:\s+(?:—|;|-)\s*(.*))?\s*$")
BACKTICK = re.compile(r"`([^`]+)`")
LINE_SUFFIX = re.compile(r":\d+$")
SHA = re.compile(r"(?<![A-Za-z0-9_])([0-9a-f]{7,40})(?![A-Za-z0-9_])")
URL = re.compile(r"(?:[A-Za-z][A-Za-z0-9+.-]*://)\S+")
REF = re.compile(r"(?<![\w/])#(\d{2,})(?!\w)")
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")

def run(command, cwd, data=None):
    try:
        return subprocess.run(command, cwd=str(cwd), input=data, capture_output=True, text=True, check=False)
    except OSError:
        return None
def parse_args(args):
    repo, memory, json_output, strict, use_gh, stale_days = None, None, False, False, False, 60
    index = 0
    while index < len(args):
        value = args[index]
        if value == "--memory":
            index += 1
            if index == len(args):
                raise ValueError("--memory needs a directory.")
            memory = Path(args[index]).expanduser()
        elif value in {"--json", "--strict", "--gh"}:
            json_output, strict, use_gh = json_output or value == "--json", strict or value == "--strict", use_gh or value == "--gh"
        elif value == "--stale-days":
            index += 1
            try:
                stale_days = int(args[index])
            except (IndexError, ValueError):
                raise ValueError("--stale-days needs an integer.")
            if stale_days < 0:
                raise ValueError("--stale-days cannot be negative.")
        elif value.startswith("-"):
            raise ValueError("Unknown option: " + value)
        elif repo is None:
            repo = Path(value).expanduser()
        else:
            raise ValueError("Only one repository may be supplied.")
        index += 1
    return (repo or Path.cwd()).resolve(), memory, json_output, strict, use_gh, stale_days
def root_for(repository):
    result = run(["git", "rev-parse", "--show-toplevel"], repository)
    return Path(result.stdout.strip()).resolve() if result and result.returncode == 0 and result.stdout.strip() else repository.resolve()
def encoded(root):
    return "".join("-" if char in "/." or ord(char) > 127 else char for char in str(root.resolve()))
def memory_for(root, supplied):
    if supplied is not None: return supplied.resolve()
    home = Path(os.environ.get("HOME", str(Path.home())))
    resolver = home / ".agents" / "skills" / "use-project-memory" / "scripts" / "resolve.py"
    result = run(["python3", str(resolver)], root) if resolver.is_file() else None
    if result and result.returncode == 0:
        for line in result.stdout.splitlines():
            if line.startswith("dir "):
                return Path(line[4:]).expanduser().resolve()
    return home / ".claude" / "projects" / encoded(root) / "memory"
def date_for(value):
    if not value: return None
    try:
        return dt.datetime.fromisoformat(value.strip().strip('"\'').replace("Z", "+00:00")).date()
    except ValueError: return None

def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---": return {}
    end = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), None)
    if end is None: return {}
    values, metadata = {}, False
    for line in lines[1:end]:
        if re.match(r"^metadata\s*:\s*$", line):
            metadata = True
            continue
        if line and not line[0].isspace():
            metadata = False
        match = re.match(r"^(\s*)(name|description|type|modified|verified)\s*:\s*(.*?)\s*$", line)
        if not match:
            continue
        indent, key, value = match.groups()
        if key in {"name", "description"} and not indent:
            values[key] = value.strip().strip('"\'')
        elif metadata and indent and key in {"type", "modified", "verified"}:
            values[key] = value.strip().strip('"\'')
    return values

def index_entries(text):
    return [{"file": match.group(1), "hook": match.group(2) or "", "line": line} for line in text.splitlines() for match in [INDEX_LINE.match(line)] if match]

def status_for(hook):
    values = re.findall(r"\b(?:SHIPPED|CLOSED|OPEN|PARKED|DISPROVEN|SUPERSEDED|VERIFIED|BLOCKED|pending)\b", hook, re.IGNORECASE)
    return [value for value in values if value in STATUS_NAMES or value.lower() == "pending"]

def path_anchors(text):
    found = []
    for match in BACKTICK.finditer(text):
        token = match.group(1)
        core = LINE_SUFFIX.sub("", token)
        invalid = any(value in token for value in ("://", "<", ">", "*", "{", "$")) or any(char.isspace() for char in token)
        excluded = core.startswith(("node_modules/", "dist/", "~", "/", "@")) or (core.startswith(".") and "/" not in core) or "/node_modules/" in core or "/dist/" in core or core in GENERIC_NAMES or core.lower() in {"agents.md", "agent.md", "claude.md", "gemini.md", "claude.local.md", "agents.override.md"}
        if not core or not ("/" in core or core.endswith(EXTENSIONS)) or invalid or excluded:
            continue
        start = text.rfind("\n", 0, match.start()) + 1
        end = text.find("\n", match.end())
        found.append({"anchor": token, "path": core, "line": core != token, "context": text[start:len(text) if end == -1 else end]})
    return found


HISTORY_PHRASES = ("used to", "previously", "formerly", "no longer", "removed", "deleted", "moved to", "moved from", "renamed", "before the split", "was at", "replaced by", "retired", "old path")


def sibling_repositories(root):
    try:
        return {path.name for path in root.parent.iterdir() if path.is_dir() and path.name != root.name and (path / ".git").exists()}
    except OSError:
        return set()


def anchor_scope(anchor, siblings):
    context = anchor["context"].lower()
    if any(re.search(r"(?<![\w-])" + re.escape(name.lower()) + r"(?![\w-])", context) for name in siblings):
        return "cross-repo"
    if any(phrase in context for phrase in HISTORY_PHRASES):
        return "historical"
    return "repo"

def sha_anchors(text):
    urls, found = [(match.start(), match.end()) for match in URL.finditer(text)], []
    for match in SHA.finditer(text):
        value = match.group(1)
        if not value.isdigit() and not any(start <= match.start(1) < end for start, end in urls): found.append(value)
    return found

def ref_anchors(text):
    return [match.group(1) for match in REF.finditer(text)]

def tracked_paths(root):
    result = run(["git", "ls-files", "-z"], root)
    return set(result.stdout.split("\0")) - {""} if result and result.returncode == 0 else set()

def resolved_path(anchor, root, tracked, basenames):
    candidate = root / anchor
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError:
        return None
    if candidate.exists() or anchor in tracked:
        return anchor.rstrip("/")
    matches = [path for path in tracked if path.endswith("/" + anchor)]
    if matches:
        return sorted(matches)[0]
    return sorted(basenames[anchor])[0] if "/" not in anchor and anchor in basenames else None

def newest_changes(root, modified):
    if not modified: return {}
    result = run(["git", "log", "--since=" + min(modified).isoformat(), "--name-only", "--format=%cs"], root)
    if not result or result.returncode != 0:
        return {}
    newest, current = {}, None
    for line in result.stdout.splitlines():
        possible = date_for(line)
        if possible and re.fullmatch(r"\d{4}-\d{2}-\d{2}", line):
            current = possible
        elif current and line:
            newest[line] = max(newest.get(line, current), current)
    return newest

def sha_status(root, shas):
    if not shas: return {}
    result = run(["git", "cat-file", "--batch-check"], root, "".join(value + "^{commit}\n" for value in sorted(shas)))
    if not result or result.returncode != 0:
        return {value: "unknown" for value in shas}
    values = {source: "known" if len(line.split()) > 1 and line.split()[1] == "commit" else "unknown" for source, line in zip(sorted(shas), result.stdout.splitlines())}
    return {value: values.get(value, "unknown") for value in shas}

def refs_status(root, refs, use_gh):
    if not use_gh: return {}, len(refs)
    statuses, lookups = {}, 0
    for value in sorted(set(refs), key=int):
        if lookups >= 60: break
        issue = run(["gh", "issue", "view", value, "--json", "state", "--jq", ".state"], root)
        lookups += 1
        if issue and issue.returncode == 0 and issue.stdout.strip():
            statuses[value] = issue.stdout.strip()
            continue
        if lookups >= 60:
            statuses[value] = "unknown"
            continue
        pull = run(["gh", "pr", "view", value, "--json", "state", "--jq", ".state"], root)
        lookups += 1
        statuses[value] = pull.stdout.strip() if pull and pull.returncode == 0 and pull.stdout.strip() else "unknown"
    return statuses, sum(1 for value in refs if value not in statuses)

def cleanup(root, memory):
    sidecar = memory / ".clean-memory.json"
    try:
        last_run = json.loads(sidecar.read_text(encoding="utf-8")).get("last_run") if sidecar.is_file() else None
    except (OSError, json.JSONDecodeError):
        last_run = None
    when = date_for(last_run)
    if not when: return None, None
    result = run(["git", "rev-list", "--count", "--since=" + when.isoformat(), "HEAD"], root)
    try:
        commits = int(result.stdout.strip()) if result and result.returncode == 0 else 0
    except ValueError:
        commits = 0
    return (dt.date.today() - when).days, commits

def leakage(root):
    found, needle = [], root.name
    for directory in (Path.home() / ".codex" / "memories", Path.home() / ".grok" / "memory"):
        if not directory.is_dir(): continue
        for path in directory.rglob("*.md"):
            try:
                count = sum(needle in line for line in path.read_text(encoding="utf-8", errors="replace").splitlines())
            except OSError:
                continue
            if count: found.append({"file": str(path), "lines": count})
    return sorted(found, key=lambda value: value["file"])

def record_topics(memory, entries, archive_entries, root, stale_days):
    files = sorted(path for path in memory.glob("*.md") if path.name not in {"MEMORY.md", "ARCHIVE.md"} and path.is_file())
    indexed = {Path(entry["file"]).name for entry in entries}
    archived = {Path(entry["file"]).name for entry in archive_entries}
    top_levels = {path.name for path in root.iterdir()}
    siblings = sibling_repositories(root)
    tracked = tracked_paths(root)
    basenames = {}
    for path in tracked:
        basenames.setdefault(Path(path).name, set()).add(path)
    raw = []
    for path in files:
        try:
            data = path.read_bytes()
        except OSError:
            continue
        text, metadata = data.decode("utf-8", errors="replace"), frontmatter(data.decode("utf-8", errors="replace"))
        modified = date_for(metadata.get("modified"))
        verified = date_for(metadata.get("verified"))
        age_from = verified or modified or dt.datetime.fromtimestamp(path.stat().st_mtime).date()
        hook = next((entry["hook"] for entry in entries if Path(entry["file"]).name == path.name), "")
        paths, seen = [], set()
        for anchor in path_anchors(text):
            if anchor["path"] in seen or not (anchor["path"].endswith(EXTENSIONS) or anchor["path"].lstrip("./").split("/", 1)[0] in top_levels):
                continue
            seen.add(anchor["path"])
            anchor["scope"] = anchor_scope(anchor, siblings)
            anchor["resolved"] = resolved_path(anchor["path"], root, tracked, basenames)
            paths.append(anchor)
        raw.append({"topic": path.stem, "bytes": len(data), "frontmatter_name": metadata.get("name"), "type": metadata.get("type"), "modified": metadata.get("modified"), "verified": metadata.get("verified"), "modified_date": modified, "age_days": (dt.date.today() - age_from).days, "index_hook": hook, "status": status_for(hook), "paths": paths, "shas": sha_anchors(text), "refs": ref_anchors(text), "uncited": not sha_anchors(text) and not ref_anchors(text) and not any(anchor["line"] for anchor in paths), "stale": (dt.date.today() - age_from).days > stale_days, "oversized": len(data) > 8192, "orphan_file": path.name not in indexed and path.name not in archived, "archived": path.name in archived and path.name not in indexed})
    newest = newest_changes(root, [record["modified_date"] for record in raw if record["modified_date"]])
    for record in raw:
        for anchor in record["paths"]:
            anchor["dead"] = anchor["resolved"] is None and anchor["scope"] == "repo"
            anchor["drifted"] = bool(anchor["scope"] == "repo" and anchor["resolved"] and record["modified_date"] and newest.get(anchor["resolved"], record["modified_date"]) > record["modified_date"])
    all_shas = {value for record in raw for value in record["shas"]}
    sha_states = sha_status(root, all_shas)
    return raw, sha_states

def report(root, memory, stale_days, use_gh):
    index_path, archive_path = memory / "MEMORY.md", memory / "ARCHIVE.md"
    index_text = index_path.read_text(encoding="utf-8", errors="replace")
    archive_text = archive_path.read_text(encoding="utf-8", errors="replace") if archive_path.is_file() else ""
    entries, archive_entries = index_entries(index_text), index_entries(archive_text)
    topics, sha_states = record_topics(memory, entries, archive_entries, root, stale_days)
    all_refs = [value for topic in topics for value in topic["refs"]]
    ref_states, skipped = refs_status(root, all_refs, use_gh)
    orphan_lines = [entry["line"] for entry in entries if not (memory / entry["file"]).is_file()]
    orphan_files = [topic["topic"] + ".md" for topic in topics if topic["orphan_file"]]
    names = {topic["topic"] for topic in topics} | {topic["frontmatter_name"] for topic in topics if topic["frontmatter_name"]}
    broken = []
    for path in memory.glob("*.md"):
        if not path.is_file():
            continue
        try:
            matches = WIKILINK.finditer(path.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
        for match in matches:
            target = match.group(1).split("|", 1)[0].strip()
            if target not in names:
                broken.append({"file": path.name, "link": target})
    over_budget = len(index_text.splitlines()) > 200 or len(index_text.encode("utf-8")) > 25600
    live = [topic for topic in topics if not topic["archived"]]
    dead = [{"topic": topic["topic"], "anchor": anchor["anchor"]} for topic in live for anchor in topic["paths"] if anchor["dead"]]
    path_total = sum(anchor["scope"] == "repo" for topic in live for anchor in topic["paths"])
    path_dead = len(dead)
    path_drifted = sum(anchor["drifted"] for topic in live for anchor in topic["paths"])
    path_cross = sum(anchor["scope"] == "cross-repo" for topic in live for anchor in topic["paths"])
    path_historical = sum(anchor["scope"] == "historical" for topic in live for anchor in topic["paths"])
    sha_total = sum(len(topic["shas"]) for topic in live)
    sha_unknown = sum(sha_states.get(value) == "unknown" for topic in live for value in topic["shas"])
    ref_total = len(all_refs)
    ref_closed = sum(ref_states.get(value) in {"CLOSED", "MERGED"} for value in all_refs)
    uncited, stale = sum(topic["uncited"] for topic in live), sum(topic["stale"] for topic in live)
    cleanup_days, cleanup_commits = cleanup(root, memory)
    mass_drift = path_total >= 20 and path_dead / path_total > 0.30
    index_bytes = len(index_text.encode("utf-8"))
    summary = {"topics": len(topics), "archived": len(topics) - len(live), "index_lines": len(index_text.splitlines()), "index_bytes": index_bytes, "archive_lines": len(archive_text.splitlines()), "paths": {"total": path_total, "dead": path_dead, "drifted": path_drifted, "cross_repo": path_cross, "historical": path_historical}, "shas": {"total": sha_total, "unknown": sha_unknown}, "refs": {"total": ref_total, "closed_or_merged": ref_closed, "skipped": skipped}, "uncited": uncited, "stale": stale, "orphans": len(orphan_lines) + len(orphan_files), "last_cleanup_days": cleanup_days, "commits_since_cleanup": cleanup_commits, "mass_drift": mass_drift}
    for topic in topics:
        topic["path_total"] = sum(anchor["scope"] == "repo" for anchor in topic["paths"])
        topic["path_dead"] = sum(anchor["dead"] for anchor in topic["paths"])
        topic["path_excluded"] = sum(anchor["scope"] != "repo" for anchor in topic["paths"])
        topic["path_drifted"] = sum(anchor["drifted"] for anchor in topic["paths"])
        topic["sha_unknown"] = sum(sha_states.get(value) == "unknown" for value in topic["shas"])
        topic["ref_closed"] = sum(ref_states.get(value) in {"CLOSED", "MERGED"} for value in topic["refs"])
        topic["flags"] = [name for name, enabled in (("uncited", topic["uncited"]), ("stale", topic["stale"]), ("oversized", topic["oversized"]), ("orphan-file", topic["orphan_file"]), ("archived", topic["archived"]), ("excluded:" + str(topic["path_excluded"]), topic["path_excluded"] > 0)) if enabled]
    return {"root": str(root), "memory": str(memory), "topics": topics, "dead_anchors": sorted(dead, key=lambda value: (value["topic"], value["anchor"])), "index": {"lines": len(index_text.splitlines()), "bytes": index_bytes, "archive_lines": len(archive_text.splitlines()), "orphan_lines": orphan_lines, "orphan_files": orphan_files, "broken_links": broken, "over_budget": over_budget}, "leakage": leakage(root), "summary": summary}
def markdown(data):
    summary = data["summary"]
    cleanup = "last cleanup never" if summary["last_cleanup_days"] is None else "last cleanup {} days ago ({} commits since)".format(summary["last_cleanup_days"], summary["commits_since_cleanup"])
    print("{topics} topics ({archived} archived), {index_lines} index lines ({index_bytes} B), {archive_lines} archive lines; live paths {paths[total]} ({paths[dead]} dead, {paths[drifted]} drifted; {paths[cross_repo]} cross-repo and {paths[historical]} historical excluded), shas {shas[total]} ({shas[unknown]} unknown), refs {refs[total]} ({refs[closed_or_merged]} closed or merged, {refs[skipped]} not looked up); {uncited} uncited, {stale} stale; orphans {orphans}; {cleanup}; mass drift {mass}.".format(**summary, cleanup=cleanup, mass="yes" if summary["mass_drift"] else "no"))
    print("\n| topic | bytes | age days | status | paths dead/total | drifted | shas unknown | refs closed | flags |\n| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |")
    topics = sorted(data["topics"], key=lambda value: (-value["path_dead"], -value["path_drifted"], -value["age_days"], value["topic"]))
    for topic in topics:
        values = dict(topic, status=",".join(topic["status"]) or "-", flags=",".join(topic["flags"]) or "none")
        print("| {topic} | {bytes} | {age_days} | {status} | {path_dead}/{path_total} | {path_drifted} | {sha_unknown} | {ref_closed} | {flags} |".format(**values))
    print("\nDead anchors")
    if data["dead_anchors"]:
        for item in data["dead_anchors"][:60]:
            print(item["topic"] + " -> " + item["anchor"])
        if len(data["dead_anchors"]) > 60:
            print("and {} more".format(len(data["dead_anchors"]) - 60))
    else:
        print("none")
    print("\nIndex problems")
    problems = data["index"]
    for line in problems["orphan_lines"]:
        print("orphan line: " + line)
    for item in problems["broken_links"]:
        print("broken link: {file} -> {link}".format(**item))
    if problems["over_budget"]:
        print("over budget: {} lines, {} B".format(problems["lines"], problems["bytes"]))
    if not (problems["orphan_lines"] or problems["broken_links"] or problems["over_budget"] or problems["orphan_files"]):
        print("none")
    for item in problems["orphan_files"]:
        print("orphan file: " + item)
    if data["leakage"]:
        print("\nLeakage\n\n| file | lines |\n| --- | ---: |")
        for item in data["leakage"]:
            print("| {file} | {lines} |".format(**item))
def main():
    try:
        repository, supplied, json_output, strict, use_gh, stale_days = parse_args(sys.argv[1:])
    except ValueError as error:
        print("audit.py: " + str(error), file=sys.stderr)
        return 2
    root = root_for(repository)
    memory = memory_for(root, supplied)
    if not memory.is_dir() or not (memory / "MEMORY.md").is_file():
        print("No memory store for {}.".format(root))
        return 0
    data = report(root, memory, stale_days, use_gh)
    if json_output:
        print(json.dumps(data, ensure_ascii=False, default=str))
    else:
        markdown(data)
    return 1 if strict and (data["index"]["over_budget"] or data["summary"]["orphans"] or data["summary"]["mass_drift"]) else 0
if __name__ == "__main__":
    raise SystemExit(main())
