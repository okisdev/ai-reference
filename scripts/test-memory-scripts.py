#!/usr/bin/env python3
"""Usage: python3 scripts/test-memory-scripts.py. Contract test for use-project-memory check.py and clean-memory audit.py."""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[1]
CHECK = REPO / "skills/use-project-memory/scripts/check.py"
AUDIT = REPO / "skills/clean-memory/scripts/audit.py"

FM = "---\nname: {name}\ndescription: \"{name} fact\"\nmetadata:\n  node_type: memory\n  type: {type}\n---\n\n{body}\n"
HOOK_80 = "OPEN 边界" + "x" * 73
HOOK_81 = "OPEN " + "y" * 76
failures = []


def expect(condition, label):
    if not condition:
        failures.append(label)


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)


def write(directory, name, text):
    (directory / name).write_text(text, encoding="utf-8")


def build_bad(directory):
    directory.mkdir()
    write(directory, "MEMORY.md", "\n".join([
        "# Memory index",
        "",
        "- [Good](good.md) — " + HOOK_80,
        "- [Long](long-hook.md) — " + HOOK_81,
        "- [Missing](missing.md) — OPEN orphan link",
        "- [Big](big.md) — OPEN big topic",
        "- [No frontmatter](nofm.md) — OPEN no frontmatter",
        "- [Bad type](badtype.md) — OPEN bad type",
        "- [Top type](toptype.md) — OPEN top level type",
        "Some prose that is not an index bullet",
        "",
    ]))
    write(directory, "good.md", FM.format(name="good", type="project", body="A fact, cited at `a.py:1`."))
    write(directory, "long-hook.md", FM.format(name="long-hook", type="feedback", body="Short."))
    write(directory, "big.md", FM.format(name="big", type="project", body="z" * 5000))
    write(directory, "nofm.md", "No frontmatter here.\n")
    write(directory, "badtype.md", FM.format(name="badtype", type="note", body="Short."))
    write(directory, "toptype.md", "---\nname: toptype\ndescription: \"x\"\ntype: project\n---\n\nShort.\n")
    write(directory, "ARCHIVE.md", "\n".join([
        "# Archive",
        "- [Old](old.md) — CLOSED " + "w" * 120,
        "- [Gone](gone.md) — CLOSED archived link to a missing file",
        "Archive prose that is not an index bullet",
        "",
    ]))
    write(directory, "old.md", FM.format(name="old", type="project", body="o" * 5000))


def build_good(directory):
    directory.mkdir()
    write(directory, "MEMORY.md", "- [Good](good.md) — " + HOOK_80 + "\n- [Other](other.md) — SHIPPED other\n")
    write(directory, "good.md", FM.format(name="good", type="project", body="A fact."))
    write(directory, "other.md", FM.format(name="other", type="reference", body="Another fact."))


def build_budget(directory):
    directory.mkdir()
    lines = ["- [T{0}](t{0}.md) — OPEN t{0}".format(index) for index in range(201)]
    write(directory, "MEMORY.md", "\n".join(lines) + "\n")
    for index in range(201):
        write(directory, "t{}.md".format(index), FM.format(name="t{}".format(index), type="project", body="x"))


with tempfile.TemporaryDirectory() as temporary:
    base = Path(temporary)
    bad, good, budget, repo = base / "bad", base / "good", base / "budget", base / "repo"
    build_bad(bad)
    build_good(good)
    build_budget(budget)
    repo.mkdir()

    result = run(CHECK, "--dir", bad, "--json", "--strict")
    expect(result.returncode == 1, "check --strict on bad store exits 1, got {}".format(result.returncode))
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        data = {}
        failures.append("check --json prints JSON: " + result.stdout[:200] + result.stderr[:200])
    found = {(item.get("file"), item.get("rule")) for item in data.get("violations", [])}
    for pair in [("MEMORY.md", "hook-length"), ("MEMORY.md", "orphan-line"), ("MEMORY.md", "index-prose"), ("big.md", "topic-size"), ("nofm.md", "frontmatter"), ("badtype.md", "frontmatter"), ("toptype.md", "frontmatter")]:
        expect(pair in found, "violation {} reported".format(pair))
    for pair in [("ARCHIVE.md", "index-prose"), ("ARCHIVE.md", "orphan-line")]:
        expect(pair in found, "violation {} reported".format(pair))
    for pair in [("ARCHIVE.md", "hook-length"), ("ARCHIVE.md", "frontmatter"), ("ARCHIVE.md", "topic-size"), ("ARCHIVE.md", "index-budget")]:
        expect(pair not in found, "no {} violation: ARCHIVE.md is checked as an archive index".format(pair))
    for clean in ["good.md", "long-hook.md", "old.md"]:
        expect(not any(item.get("file") == clean for item in data.get("violations", [])), clean + " has no violation")
    hook_lines = [item for item in data.get("violations", []) if item.get("rule") == "hook-length"]
    expect(len(hook_lines) == 1, "exactly one hook-length violation (80 characters passes, 81 fails), got {}".format(len(hook_lines)))
    expect(len([item for item in data.get("violations", []) if item.get("file") == "nofm.md"]) == 1, "a file without frontmatter yields exactly one violation")
    expect(data.get("limits") == {"hook_chars": 80, "topic_bytes": 4096, "index_lines": 200, "index_bytes": 25600}, "limits object matches the contract")
    expect(isinstance(data.get("index"), dict) and data["index"].get("lines") == 10, "index lines counted, got {}".format(data.get("index")))

    result = run(CHECK, "--dir", bad)
    expect(result.returncode == 0, "check without --strict exits 0")
    expect("topic-size" in result.stdout and "violations" in result.stdout, "text output names rules and a summary line")

    result = run(CHECK, bad / "big.md", "--json")
    data = json.loads(result.stdout or "{}")
    expect({item.get("file") for item in data.get("violations", [])} == {"big.md"}, "FILE mode checks only the named file")
    expect(data.get("index") is None, "FILE mode without MEMORY.md reports index null")

    result = run(CHECK, bad / "ARCHIVE.md", "--json")
    data = json.loads(result.stdout or "{}")
    rules = {(item.get("file"), item.get("rule")) for item in data.get("violations", [])}
    expect(rules == {("ARCHIVE.md", "index-prose"), ("ARCHIVE.md", "orphan-line")}, "FILE mode on ARCHIVE.md runs only the archive checks, got {}".format(sorted(rules)))

    result = run(CHECK, bad / "old.md", "--json")
    data = json.loads(result.stdout or "{}")
    expect(not data.get("violations"), "an archived topic is exempt from the topic size limit in FILE mode too")

    result = run(CHECK, "--dir", good, "--strict")
    expect(result.returncode == 0 and "clean" in result.stdout, "clean store passes --strict and prints clean")

    result = run(CHECK, "--dir", budget, "--json", "--strict")
    data = json.loads(result.stdout or "{}")
    expect(any(item.get("rule") == "index-budget" for item in data.get("violations", [])), "index over 200 lines reports index-budget")

    result = run(CHECK, "--bogus")
    expect(result.returncode == 2, "unknown flag exits 2")

    result = run(CHECK, "--dir", base / "nowhere")
    expect(result.returncode == 0 and "No memory store" in result.stdout, "missing store prints No memory store and exits 0")

    spec = importlib.util.spec_from_file_location("memory_check", CHECK)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expect(hasattr(module, "LIMITS") and hasattr(module, "check"), "module exposes LIMITS and check()")
    if hasattr(module, "check"):
        expect(any(item["rule"] == "topic-size" for item in module.check(bad)["violations"]), "check(directory) returns the same violations")

    def hook(payload):
        return subprocess.run([sys.executable, str(CHECK), "--hook"], input=payload if isinstance(payload, str) else json.dumps(payload), capture_output=True, text=True)

    store = base / ".claude" / "projects" / "hook-project" / "memory"
    store.parent.mkdir(parents=True)
    build_bad(store)
    index = store / "MEMORY.md"
    before = index.read_text(encoding="utf-8")
    long_line = "- [New](good.md) — " + "n" * 90
    index.write_text(before + long_line + "\n", encoding="utf-8")
    result = hook({"tool_name": "Edit", "tool_input": {"file_path": str(index), "old_string": "x", "new_string": long_line}, "tool_response": {"filePath": str(index), "originalFile": before}})
    expect(result.returncode == 2, "hook exits 2 when the lines an edit added break the format, got {}".format(result.returncode))
    expect("hook-length" in result.stderr and ":11:" in result.stderr, "hook names the added line and its number: " + result.stderr[:300])
    expect(result.stderr.count("hook-length") == 1 and "index-prose" not in result.stderr and "orphan-line" not in result.stderr, "hook ignores the older violations already in the index")

    good_line = "- [Fine](good.md) — OPEN fine"
    index.write_text(before + good_line + "\n", encoding="utf-8")
    result = hook({"tool_name": "Edit", "tool_input": {"file_path": str(index), "old_string": "x", "new_string": good_line}, "tool_response": {"filePath": str(index), "originalFile": before}})
    expect(result.returncode == 0 and not result.stderr.strip(), "hook passes a compliant added line in an index with older violations")

    fresh = base / ".claude" / "projects" / "fresh-project" / "memory"
    fresh.mkdir(parents=True)
    (fresh / "MEMORY.md").write_text("- [Long](long.md) — " + "q" * 90 + "\n", encoding="utf-8")
    result = hook({"tool_name": "Write", "tool_input": {"file_path": str(fresh / "MEMORY.md"), "content": ""}, "tool_response": {"type": "create", "filePath": str(fresh / "MEMORY.md"), "originalFile": None}})
    expect(result.returncode == 2 and "hook-length" in result.stderr and "orphan-line" in result.stderr, "a new index file has every line checked")

    result = hook({"tool_name": "Write", "tool_input": {"file_path": str(store / "big.md"), "content": ""}, "tool_response": {"type": "update", "filePath": str(store / "big.md"), "originalFile": "old"}})
    expect(result.returncode == 2 and "topic-size" in result.stderr, "hook reports an oversized topic write")
    result = hook({"tool_name": "Write", "tool_input": {"file_path": str(store / "good.md"), "content": ""}, "tool_response": {"type": "update", "filePath": str(store / "good.md"), "originalFile": "old"}})
    expect(result.returncode == 0 and not result.stderr.strip(), "hook passes a compliant topic write")
    result = hook({"tool_name": "Write", "tool_input": {"file_path": str(store / "old.md"), "content": ""}, "tool_response": {"type": "update", "filePath": str(store / "old.md"), "originalFile": "old"}})
    expect(result.returncode == 0, "hook exempts an archived topic from the size limit")
    result = hook({"tool_name": "Edit", "tool_input": {"file_path": str(store / "ARCHIVE.md"), "old_string": "a", "new_string": "b"}, "tool_response": {"filePath": str(store / "ARCHIVE.md"), "originalFile": ""}})
    expect(result.returncode == 0 and not result.stderr.strip(), "hook skips ARCHIVE.md")
    result = hook({"tool_name": "Write", "tool_input": {"file_path": str(repo / "notes.md"), "content": ""}, "tool_response": {"type": "create", "filePath": str(repo / "notes.md"), "originalFile": None}})
    expect(result.returncode == 0 and not result.stderr.strip() and not result.stdout.strip(), "hook ignores files outside a memory store")
    lookalike = base / "lookalike"
    build_bad(lookalike)
    result = hook({"tool_name": "Write", "tool_input": {"file_path": str(lookalike / "big.md"), "content": ""}, "tool_response": {"type": "update", "filePath": str(lookalike / "big.md"), "originalFile": "old"}})
    expect(result.returncode == 0 and not result.stderr.strip(), "hook ignores a directory that merely holds a MEMORY.md outside .claude/projects/<name>/memory")
    result = hook("not json")
    expect(result.returncode == 0, "hook exits 0 on a payload it cannot parse")

    result = run(AUDIT, repo, "--memory", bad, "--strict")
    expect(result.returncode == 1, "audit --strict fails on format violations")
    expect("Format problems" in result.stdout and "topic-size" in result.stdout, "audit prints a Format problems section")
    result = run(AUDIT, repo, "--memory", bad, "--json")
    data = json.loads(result.stdout or "{}")
    expect(bool(data.get("format", {}).get("violations")), "audit JSON carries format.violations")
    expect(data.get("summary", {}).get("format_violations") == len(data.get("format", {}).get("violations", [])), "summary.format_violations matches")
    big = next((topic for topic in data.get("topics", []) if topic.get("topic") == "big"), {})
    expect("oversized" in big.get("flags", []), "a 5000 byte topic is flagged oversized (limit from check.py)")
    anchors_repo = base / "anchors-repo"
    (anchors_repo / "src").mkdir(parents=True)
    (anchors_repo / "src" / "live.ts").write_text("x\n", encoding="utf-8")
    (anchors_repo / "app" / "[[...slug]]").mkdir(parents=True)
    (anchors_repo / "app" / "[[...slug]]" / "page.tsx").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(anchors_repo)], check=True)
    subprocess.run(["git", "-C", str(anchors_repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(anchors_repo), "remote", "add", "origin", "https://github.com/self-owner/self-repo.git"], check=True)
    anchors_store = base / "anchors-store"
    anchors_store.mkdir()
    write(anchors_store, "MEMORY.md", "- [Anchors](anchors.md) — OPEN anchors\n")
    body = "\n".join([
        "Live at `src/live.ts:14-63` and `src/live.ts:246,251` and `src/live.ts:resolveRegistryItemUrl`.",
        "Upstream `registry/foo.ts` lives in shadcn-ui/ui, not here.",
        "See https://github.com/vercel/streamdown for `lib/parse.ts`.",
        "Routes like `app/[[...slug]]/page.tsx` and mentions like `[[alice]]` are syntax, not links.",
        "The parser in vercel/streamdown keeps `lib/tokens.ts` separate.",
        "Uses the master/detail layout for `src/missing.ts`.",
        "Upstream skill smoke/SKILL.md reads `src/missing2.ts`.",
        "Tracked in self-owner/self-repo#5 and self-owner/other-repo#3, with scope-owner/tools#12 upstream.",
        "The `@scope-owner/react` package reads `src/missing3.ts`.",
        "See self-owner/self-repo for `src/missing4.ts`.",
        "No citation here.",
    ])
    write(anchors_store, "anchors.md", "---\nname: anchors\ndescription: \"a\"\nmetadata:\n  type: project\n  originSessionId: 1a2b3c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d\n---\n\n" + body + "\n")
    result = run(AUDIT, anchors_repo, "--memory", anchors_store, "--json")
    data = json.loads(result.stdout or "{}")
    dead = [item.get("anchor") for item in data.get("dead_anchors", [])]
    expect(sorted(dead) == ["src/missing.ts", "src/missing2.ts", "src/missing3.ts", "src/missing4.ts"], "line ranges and symbol suffixes resolve, named repositories count as cross repo, prose slashes, file tokens, npm scopes, and this repository's own slug do not, got dead {}".format(dead))
    topic = next((item for item in data.get("topics", []) if item.get("topic") == "anchors"), {})
    expect(topic.get("shas") == [], "uuid fragments in frontmatter are not SHAs, got {}".format(topic.get("shas")))
    expect(not data.get("index", {}).get("broken_links"), "[[...slug]] and code-span [[alice]] are not broken links, got {}".format(data.get("index", {}).get("broken_links")))

    result = run(AUDIT, repo, "--memory", good, "--strict")
    expect(result.returncode == 0, "audit --strict passes on a clean store, got {}: {}".format(result.returncode, result.stdout[-300:]))

if failures:
    print("FAIL")
    for item in failures:
        print(" - " + item)
    raise SystemExit(1)
print("PASS all memory check contract assertions")
