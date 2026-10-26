"""Exercise measure.py against temporary repositories and hook payloads."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MEASURE = Path(__file__).resolve().parents[1] / "skills/normalize-agents-md/scripts/measure.py"
TABLE_HEADER = "| file | bytes | lines | chars | longest unit | units over 600 | dated | history | flags |"


class MeasureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True)

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def measure(self, *args):
        return subprocess.run([sys.executable, str(MEASURE), str(self.root), *args], text=True, capture_output=True)

    def report(self):
        result = self.measure("--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def hook(self, path, content, *, tool="Edit", original="", old_string="", new_string="", malformed=False):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        payload = {"tool_name": tool, "tool_input": {"file_path": str(path), "old_string": old_string, "new_string": new_string},
                   "tool_response": {"filePath": str(path), "originalFile": original}}
        return subprocess.run([sys.executable, str(MEASURE), "--hook"], input="{" if malformed else json.dumps(payload), text=True, capture_output=True, cwd=self.root)

    def hook_payload(self, payload):
        return subprocess.run([sys.executable, str(MEASURE), "--hook"], input=json.dumps(payload), text=True, capture_output=True, cwd=self.root)

    def test_pointed_and_required_docs(self):
        self.write("AGENTS.md", "Read `apps/desktop/DESIGN.md` before any UI change.\n")
        self.write("apps/desktop/DESIGN.md", "# Design\n")
        self.write("services/relay/AGENTS.md", "`README.md` describes its routes and Durable Objects.\n")
        self.write("services/relay/README.md", "# Relay\n")
        docs = {doc["path"]: doc for doc in self.report()["docs"]}
        self.assertTrue(docs["apps/desktop/DESIGN.md"]["required"])
        self.assertEqual(docs["apps/desktop/DESIGN.md"]["pointed_by"], ["AGENTS.md:1"])
        self.assertFalse(docs["services/relay/README.md"]["required"])
        self.assertEqual(docs["services/relay/README.md"]["pointed_by"], ["services/relay/AGENTS.md:1"])
        self.assertIn(TABLE_HEADER, self.measure().stdout)

    def test_pointed_readme_over_target(self):
        self.write("AGENTS.md", "See `README.md` for setup.\n")
        self.write("README.md", "x" * 17000)
        result = self.report()
        self.assertEqual(result["docs"][0]["flags"], ["pointed-over-target"])
        self.assertEqual(result["summary"]["pointed_over_target"], 1)
        self.assertEqual(result["summary"]["docs_over_target"], 0)
        self.assertEqual(result["large_docs"], [])
        self.assertIn("1 pointed over target", self.measure().stdout)

    def test_unpointed_large_readme(self):
        self.write("README.md", "x" * 17000)
        result = self.report()
        self.assertEqual(result["large_docs"], [{"path": "README.md", "bytes": 17000}])
        self.assertEqual(result["summary"]["large_docs"], 1)
        output = self.measure().stdout
        self.assertIn("| large doc off the agent path | bytes |", output)
        self.assertIn("1 large docs off the agent path.", output)

    def test_readme_signal_requires_agent_facing_lines(self):
        self.write("README.md", "Settings › Agents lists the agents installed\n### Claude Code\nAI agents run here\n")
        self.assertEqual(self.report()["readmes"], [])
        self.write("README.md", "Settings › Agents lists the agents installed\n### Claude Code\nAI agents run here\n## Conventions\nRead AGENTS.md first\n")
        self.assertEqual(self.report()["readmes"][0]["agent_lines"], 2)

    def test_readme_signal_accepts_instruction_headings_for_agents(self):
        for heading in ("## Instructions for agents", "## Instructions for AI agents", "## Instructions for AI coding agents", "## Guide for coding agent"):
            with self.subTest(heading=heading):
                self.write("README.md", heading + "\n")
                self.assertEqual(self.report()["readmes"][0]["agent_lines"], 1)
        self.write("README.md", "## Agents\n## AI product\n## Coding tools\n")
        self.assertEqual(self.report()["readmes"], [])

    def test_since_reports_readme_growth(self):
        self.write("README.md", "a" * 10)
        subprocess.run(["git", "add", "README.md"], cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-q", "-m", "first"], cwd=self.root, check=True, capture_output=True)
        first = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.root, check=True, capture_output=True, text=True).stdout.strip()
        self.write("README.md", "a" * 1010)
        subprocess.run(["git", "add", "README.md"], cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-q", "-m", "second"], cwd=self.root, check=True, capture_output=True)
        result = self.measure("--since", first)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| README.md | 10 | 1010 | +1000 |", result.stdout)
        self.assertIn("Since {} (".format(first[:7]), result.stdout)
        self.assertIn("instruction files +0 bytes, docs +1000 bytes, 1 files changed.", result.stdout)
        since = json.loads(self.measure("--since", first, "--json").stdout)["since"]
        self.assertEqual(since["rows"], [{"path": "README.md", "then": 10, "now": 1010, "change": 1000}])

    def test_unresolvable_since(self):
        result = self.measure("--since", "no-such-ref-or-date")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr.strip(), "Measure.py: Cannot resolve --since: no-such-ref-or-date")
        self.assertEqual(self.measure("--since").returncode, 2)

    def test_since_accepts_only_commit_refs_or_supported_dates(self):
        self.write("README.md", "initial\n")
        subprocess.run(["git", "add", "README.md"], cwd=self.root, check=True, capture_output=True)
        commit_date = "2020-01-01T00:00:00 +0000"
        environment = {**os.environ, "GIT_AUTHOR_DATE": commit_date, "GIT_COMMITTER_DATE": commit_date}
        subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-q", "-m", "first"], cwd=self.root, check=True, capture_output=True, env=environment)
        for value in ("nonsense-ref-xyz", "3 fortnights ago", "2026-10-16 08:00Z", "2026-99-99", "2026-02-30", "2026-10-16 25:00"):
            with self.subTest(value=value):
                result = self.measure("--since", value)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(result.stderr.strip(), "Measure.py: Cannot resolve --since: " + value)
        for value in ("3 days ago", "3.days.ago", "2026-10-16 08:00", "2026-10-16T08:00:00"):
            with self.subTest(value=value):
                result = self.measure("--since", value)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Since ", result.stdout)

    def test_before_read_order_in_report_and_hook(self):
        lines = [
            "`apps/mobile/DESIGN.md` is the app's design law; before a UI change, read its Principles.",
            "- Before a UI change read `DESIGN.md`'s Principles and the section for what you change.",
            "Read `docs/x.md` before a UI change.",
            "`README.md` describes its routes.",
            "Before shipping, run `make test`; see `NOTES.md`.",
        ]
        self.write("AGENTS.md", "\n".join(lines) + "\n")
        paths = ("apps/mobile/DESIGN.md", "DESIGN.md", "docs/x.md", "README.md", "NOTES.md")
        for name in paths:
            self.write(name, "# Document\n")
        docs = {doc["path"]: doc for doc in self.report()["docs"]}
        self.assertEqual([(docs[name]["required"], docs[name]["pointed_by"]) for name in paths],
                         [(True, ["AGENTS.md:1"]), (True, ["AGENTS.md:2"]), (True, ["AGENTS.md:3"]),
                          (False, ["AGENTS.md:4"]), (False, ["AGENTS.md:5"])])
        for name in paths[:3] + paths[4:]:
            with self.subTest(name=name):
                result = self.hook(self.root / name, "# Document\n" + "x" * 601 + "\n", original="# Document\n")
                self.assertEqual(result.returncode, 0 if name == "NOTES.md" else 2, result.stderr)
                if name != "NOTES.md":
                    self.assertIn("long-unit", result.stderr)
        result = self.hook(self.root / "README.md", "# Document\n" + "x" * 17000 + "\n", original="# Document\n")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("README.md:0: over-target: 17012 bytes (target 16384)", result.stderr)

    def test_root_fallback_and_anchor(self):
        self.write("services/relay/AGENTS.md", "Read [design](docs/DESIGN.md#colors) first.\n")
        self.write("docs/DESIGN.md", "# Design\n")
        docs = self.report()["docs"]
        self.assertEqual([(doc["path"], doc["required"]) for doc in docs], [("docs/DESIGN.md", True)])

    def test_read_order_requires_same_sentence_as_reference(self):
        self.write("AGENTS.md", "If `NOTES.md` and the code disagree, the test wins.\nSee `CONTRIBUTING.md`. Read the release notes before tagging.\nRead `apps/desktop/DESIGN.md` before any UI change.\n")
        for name in ("NOTES.md", "CONTRIBUTING.md", "apps/desktop/DESIGN.md"):
            self.write(name, "# Document\n")
        docs = {doc["path"]: doc for doc in self.report()["docs"]}
        self.assertEqual([(docs[name]["required"], docs[name]["pointed_by"]) for name in ("NOTES.md", "CONTRIBUTING.md", "apps/desktop/DESIGN.md")],
                         [(False, ["AGENTS.md:1"]), (False, ["AGENTS.md:2"]), (True, ["AGENTS.md:3"])])
        for name in ("NOTES.md", "CONTRIBUTING.md"):
            with self.subTest(name=name):
                result = self.hook(self.root / name, "# Document\n" + "x" * 601 + "\n", original="# Document\n")
                self.assertEqual((result.returncode, result.stderr), (0, ""))
        result = self.hook(self.root / "apps/desktop/DESIGN.md", "# Document\n" + "x" * 601 + "\n", original="# Document\n")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("long-unit", result.stderr)

    def test_unpointed_precedence_doc_and_no_instruction_output(self):
        self.write("docs/DESIGN.md", "Where the two disagree, this file wins.\n")
        result = self.report()
        self.assertEqual(result["summary"]["required_docs"], 1)
        self.assertEqual(result["docs"][0]["pointed_by"], [])
        output = self.measure().stdout
        self.assertIn("No instruction files found", output)
        self.assertIn("| doc | required | pointed by |", output)

    def test_quoted_order_and_fenced_precedence_are_examples(self):
        self.write("AGENTS.md", 'See `docs/DESIGN.md` for examples.\nSee `docs/quoted.md` for the phrase "read before editing".\n')
        self.write("docs/DESIGN.md", "# Design\n```md\nWhere the two disagree, this file wins.\n```\n~~~~md\nThis file is the source of truth.\n~~~~\n")
        self.write("docs/quoted.md", 'The phrase "a change to this file first" is an example.\n')
        self.write("docs/grader.md", "The rewritten doc no longer says a new font is a change to this file first, and no longer says a missing component is added to this file in the same change; any precedence line it keeps applies to rules.\n")
        self.write("AGENTS.override.md", "See `docs/grader.md` for examples.\n")
        docs = {doc["path"]: doc for doc in self.report()["docs"]}
        self.assertFalse(docs["docs/DESIGN.md"]["required"])
        self.assertFalse(docs["docs/quoted.md"]["required"])
        self.assertFalse(docs["docs/grader.md"]["required"])
        self.assertEqual(docs["docs/quoted.md"]["accretion_orders"], [])
        self.assertEqual(docs["docs/grader.md"]["accretion_orders"], [])
        self.assertEqual(self.report()["summary"]["accretion_orders"], 0)

    def test_doc_does_not_inherit_instruction_flags(self):
        self.write("AGENTS.md", "Read `docs/DESIGN.md` before editing.\n")
        self.write("docs/DESIGN.md", "This file provides guidance to coding agents.\n")
        doc = self.report()["docs"][0]
        self.assertTrue(doc["required"])
        self.assertEqual(doc["flags"], [])

    def test_history_phrases_ignore_examples(self):
        path = self.write("AGENTS.md", '# Rules\nThe phrase "previously" is an example.\n~~~md\nThis used to be a rule.\n~~~\nThis was formerly a rule.\n')
        self.assertEqual(self.report()["files"][0]["history_phrases"], 1)
        old = path.read_text(encoding="utf-8")
        added = 'The example says "no longer".\n'
        result = self.hook(path, old + added, original=old, old_string="", new_string=added)
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_ignored_worktree_docs_are_not_candidates(self):
        self.write("AGENTS.md", "Read `apps/desktop/DESIGN.md` and `.claude/worktrees/x/apps/desktop/DESIGN.md` before editing.\n")
        content = "Where the two disagree, this file wins.\n"
        normal = self.write("apps/desktop/DESIGN.md", content)
        ignored = self.write(".claude/worktrees/x/apps/desktop/DESIGN.md", content)
        exclude = self.root / ".git/info/exclude"
        with exclude.open("a", encoding="utf-8") as output:
            output.write("\n.claude/worktrees/\n")
        docs = self.report()["docs"]
        self.assertEqual([doc["path"] for doc in docs], ["apps/desktop/DESIGN.md"])
        self.assertTrue(docs[0]["required"])
        self.assertEqual(self.hook(ignored, content + "Last updated: 2026-10-10.\n", original=content).returncode, 0)
        result = self.hook(normal, content + "Last updated: 2026-10-10.\n", original=content)
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_no_doc_table_without_docs(self):
        self.write("AGENTS.md", "Keep rules concise.\n")
        output = self.measure().stdout
        self.assertNotIn("| doc |", output)
        self.assertIn("0 read-path docs", output)

    def test_accretion_orders_and_exclusions(self):
        lines = [
            "Build only from the components this file names; if one is missing, add it to `src/renderer/src/design` and to this file in the same change.",
            "A new font, color, button style, bar or sheet frame is a change to this file first.",
            "A new color, size or control style goes into those files and `DESIGN.md` first.",
            "A lesson from one session goes to commit messages, issues, or the maintainer's memory store; a rule enters here only when the same mistake repeats or a review catches it.",
            "Keep `packageManager` in sync with the `corepack prepare` lines of the root `Dockerfile`.",
        ]
        self.write("AGENTS.md", "Read `DESIGN.md` before editing.\n" + "\n".join(lines) + "\n")
        self.write("DESIGN.md", "\n".join(lines) + "\n")
        result = self.report()
        self.assertEqual(result["files"][0]["accretion_orders"], [2, 3, 4])
        self.assertEqual(result["docs"][0]["accretion_orders"], [1, 2, 3])
        self.assertEqual(result["summary"]["accretion_orders"], 6)

    def test_accretion_sentence_scope_and_doc_mentions(self):
        excluded = [
            "A group is what the person keeps together in one row of the sidebar: a terminal and the pull requests, issues, docs, sites and Changes it works with. The sidebar lists pinned groups first, and goes by its first terminal.",
            "The docs describe groups. Add it first.",
            "The docs describe groups! Add it first.",
            "The docs describe groups? Add it first.",
            "A group keeps docs and goes by its first terminal.",
            "Add docs first.",
        ]
        included = [
            "It is built from `src/design` and this file; anything new was added there first.",
            "4. Build only from the components this file names; if one is missing, add it to `src/renderer/src/design` and to this file in the same change.",
            "A new color, size or control style goes into those files and `DESIGN.md` first.",
            "Update the docs in the same change.",
            "Add to the docs first.",
            "Add to docs/components first.",
        ]
        self.write("AGENTS.md", "Read `DESIGN.md` before editing.\n")
        self.write("DESIGN.md", "\n".join(excluded + included) + "\n")
        result = self.report()
        self.assertEqual(result["docs"][0]["accretion_orders"], list(range(len(excluded) + 1, len(excluded + included) + 1)))
        self.assertEqual(result["summary"]["accretion_orders"], len(included))

    def test_hook_accretion_sentence_scope_and_doc_mentions(self):
        self.write("AGENTS.md", "Read `DESIGN.md` before editing.\n")
        path = self.write("DESIGN.md", "# Design\n")
        original = "# Design\n"
        excluded = [
            "A group is what the person keeps together in one row of the sidebar: a terminal and the pull requests, issues, docs, sites and Changes it works with. The sidebar lists pinned groups first, and goes by its first terminal.",
            "The docs describe groups. Add it first.",
            "A group keeps docs and goes by its first terminal.",
        ]
        included = [
            "It is built from `src/design` and this file; anything new was added there first.",
            "4. Build only from the components this file names; if one is missing, add it to `src/renderer/src/design` and to this file in the same change.",
            "A new color, size or control style goes into those files and `DESIGN.md` first.",
            "Update the docs in the same change.",
        ]
        for line in excluded:
            with self.subTest(line=line):
                result = self.hook(path, original + line + "\n", original=original)
                self.assertEqual((result.returncode, result.stderr), (0, ""))
        for line in included:
            with self.subTest(line=line):
                result = self.hook(path, original + line + "\n", original=original)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("DESIGN.md:2: accretion-order:", result.stderr)

    def test_caps_and_json_compatibility(self):
        self.write("AGENTS.md", "Read `DESIGN.md` before editing.\n")
        self.write("DESIGN.md", "x\n" * 8300)
        result = self.report()
        self.assertTrue({"root", "scope", "files", "chains", "generators", "readmes", "docs", "summary"} <= result.keys())
        self.assertTrue({"instruction_files", "over_hard_cap", "over_target", "claude_md", "read_path_docs", "required_docs", "docs_over_target", "accretion_orders"} <= result["summary"].keys())
        self.assertIn("over-target", result["docs"][0]["flags"])
        self.assertEqual(self.measure("--strict").returncode, 0)
        self.write("AGENTS.md", "a" * 10001)
        self.assertEqual(self.measure("--strict").returncode, 1)

    def test_hook_edit_lines(self):
        self.write("AGENTS.md", "Read `DESIGN.md` before editing.\n")
        path = self.write("DESIGN.md", "# Design\n")
        old = "# Design\n"
        result = self.hook(path, old + "Last updated: 2026-10-10.\n", original=old, old_string=old, new_string=old + "Last updated: 2026-10-10.\n")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("DESIGN.md:2: status-line:", result.stderr)
        self.assertEqual(result.stdout, "")
        payload = {"tool_name": "Edit", "tool_input": {"file_path": str(path), "old_string": "", "new_string": "Last updated: 2026-10-10.\n"},
                   "tool_response": {"filePath": str(path), "originalFile": None}}
        result = subprocess.run([sys.executable, str(MEASURE), "--hook"], input=json.dumps(payload), text=True, capture_output=True, cwd=self.root)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("status-line", result.stderr)
        result = self.hook(path, old + "- A badge is never a pill.\n", original=old)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        agent = self.root / "AGENTS.md"
        added = "A new color is a change to this file first.\n"
        result = self.hook(agent, "Read `DESIGN.md` before editing.\n" + added, original="Read `DESIGN.md` before editing.\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("accretion-order", result.stderr)

    def test_status_lines_match_journal_shapes(self):
        self.write("AGENTS.md", "Read `DESIGN.md` before editing.\n")
        path = self.write("DESIGN.md", "# Design\n")
        old = "# Design\n"
        statuses = [
            "Last updated: 2026-10-10.",
            "Status: in progress.",
            "Figures as of 2026-09-25.",
            "Figures updated 2026-09-25.",
            "Figures updated on 2026-09-25.",
            "Figures on 2026-09-25.",
            "- **D25, loading** (2026-09-30): Usage drew its figures at once.",
            "## Drift found on 2026-09-25",
            "## Drift found 2026-09-25",
        ]
        for line in statuses:
            with self.subTest(line=line):
                result = self.hook(path, old + line + "\n", original=old)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("DESIGN.md:2: status-line:", result.stderr)
        self.write("DESIGN.md", old + "\n".join(statuses) + "\n")
        self.assertEqual(self.report()["docs"][0]["status_lines"], len(statuses))

    def test_rule_date_is_not_status_line(self):
        self.write("AGENTS.md", "Read `DESIGN.md` before editing.\n")
        path = self.write("DESIGN.md", "# Design\n")
        old = "# Design\n"
        rule = "- Reject tokens issued before 2024-06-01.\n"
        result = self.hook(path, old + rule, original=old, old_string="", new_string=rule)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        self.assertEqual(self.report()["docs"][0]["status_lines"], 0)

    def test_hook_skips_fenced_and_quoted_examples(self):
        self.write("AGENTS.md", "Read `DESIGN.md` before editing.\n")
        path = self.write("DESIGN.md", "# Design\n")
        old = "# Design\n"
        example = "````md\nLast updated: 2026-10-10.\nA change to this file first.\n````\n"
        result = self.hook(path, old + example, original=old, old_string="", new_string=example)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        self.assertEqual(self.report()["docs"][0]["status_lines"], 0)
        self.assertEqual(self.report()["docs"][0]["accretion_orders"], [])
        quoted = 'The example says "Last updated: 2026-10-10" and "a change to this file first".\n'
        result = self.hook(path, old + quoted, original=old, old_string="", new_string=quoted)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        self.assertEqual(self.report()["docs"][0]["status_lines"], 0)

    def test_hook_target_growth_and_shrink(self):
        self.write("AGENTS.md", "Read `DESIGN.md` before editing.\n")
        path = self.root / "DESIGN.md"
        old = "x\n" * 8100
        grown = "x\n" * 8300
        result = self.hook(path, grown, tool="Write", original=old)
        self.assertEqual(result.returncode, 2)
        self.assertIn("over-target", result.stderr)
        result = self.hook(path, old, tool="Write", original=grown)
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_hook_long_unit_classes(self):
        path = self.write("AGENTS.md", "# Rules\n")
        paragraph = "a" * 700
        result = self.hook(path, "# Rules\n" + paragraph + "\n", original="# Rules\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("long-unit", result.stderr)
        self.write("services/relay/AGENTS.md", "`README.md` describes routes.\n")
        readme = self.root / "services/relay/README.md"
        result = self.hook(readme, "# Relay\n\n" + paragraph + "\n", original="# Relay\n\n")
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_hook_ignores_unrelated_paths_and_bad_payloads(self):
        for name in ("src/app.ts", ".claude/projects/example/memory/topic.md"):
            with self.subTest(name=name):
                result = self.hook(self.root / name, "Last updated: 2026-10-10.\n")
                self.assertEqual((result.returncode, result.stderr), (0, ""))
        result = self.hook(self.root / "AGENTS.md", "Last updated: 2026-10-10.\n", malformed=True)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        outside = Path(self.temp.name) / "outside.md"
        result = self.hook(outside, "Last updated: 2026-10-10.\n")
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_hook_list_input_exits_without_traceback(self):
        path = self.write("AGENTS.md", "Last updated: 2026-10-10.\n")
        payload = {"tool_name": "Edit", "tool_input": [], "tool_response": {"filePath": str(path), "originalFile": ""}}
        result = subprocess.run([sys.executable, str(MEASURE), "--hook"], input=json.dumps(payload), text=True, capture_output=True, cwd=self.root)
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_codex_patch_checks_added_instruction_line(self):
        self.write("AGENTS.md", "# Rules\nStatus: shipped (2026-10-19)\n")
        payload = {"tool_name": "apply_patch", "tool_input": {"command": "*** Begin Patch\n*** Update File: AGENTS.md\n@@\n+Status: shipped (2026-10-19)\n*** End Patch"}, "tool_response": "Success", "cwd": str(self.root)}
        result = self.hook_payload(payload)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("AGENTS.md:2: status-line:", result.stderr)

    def test_codex_patch_skips_non_markdown_and_malformed_patch(self):
        self.write("AGENTS.md", "# Rules\nStatus: shipped (2026-10-19)\n")
        self.write("src/app.ts", "const status = 'shipped';\n")
        payload = {"tool_name": "apply_patch", "tool_input": {"command": "*** Begin Patch\n*** Update File: src/app.ts\n@@\n+const status = 'shipped';\n*** End Patch"}, "tool_response": "Success", "cwd": str(self.root)}
        result = self.hook_payload(payload)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        payload["tool_input"]["command"] = "*** Begin Patch\n*** Update File: AGENTS.md\n+Status: shipped (2026-10-19)\n*** End Patch"
        result = self.hook_payload(payload)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("AGENTS.md:2: status-line:", result.stderr)
        payload["tool_input"]["command"] = "*** Update File: AGENTS.md\n+Status: shipped (2026-10-19)\n*** End Patch"
        result = self.hook_payload(payload)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        payload["tool_input"]["command"] = ["*** Begin Patch"]
        result = self.hook_payload(payload)
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_codex_patch_end_of_file_after_added_lines(self):
        self.write("AGENTS.md", "# Rules\nStatus: shipped (2026-10-19)\n")
        command = "*** Begin Patch\n*** Update File: AGENTS.md\n@@\n+Status: shipped (2026-10-19)\n*** End of File\n*** End Patch"
        payload = {"tool_name": "apply_patch", "tool_input": {"command": command}, "tool_response": "Success", "cwd": str(self.root)}
        result = self.hook_payload(payload)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("AGENTS.md:2: status-line:", result.stderr)

    def test_codex_patch_checks_all_markdown_files_and_readme_growth(self):
        self.write("AGENTS.md", "`README.md` is its manual.\n")
        self.write("docs/DESIGN.md", "# Design\nStatus: shipped (2026-10-19)\n")
        readme = "x\n" * 8500
        self.write("README.md", readme)
        command = "*** Begin Patch\n*** Update File: docs/DESIGN.md\n@@\n+Status: shipped (2026-10-19)\n*** Add File: README.md\n" + "+x\n" * 8500 + "*** End Patch"
        payload = {"tool_name": "apply_patch", "tool_input": {"command": command}, "tool_response": "Success", "cwd": str(self.root)}
        result = self.hook_payload(payload)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("docs/DESIGN.md:2: status-line:", result.stderr)
        self.assertIn("README.md:0: over-target: 17000 bytes (target 16384)", result.stderr)
        payload["tool_input"]["command"] = "*** Begin Patch\n*** Update File: README.md\n@@\n-x\n*** End Patch"
        self.write("README.md", "x\n" * 8499)
        result = self.hook_payload(payload)
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_codex_patch_move_checks_destination(self):
        self.write("docs/DESIGN.md", "# Design\nStatus: shipped (2026-10-19)\n")
        command = "*** Begin Patch\n*** Update File: docs/old.md\n*** Move to: docs/DESIGN.md\n@@\n+Status: shipped (2026-10-19)\n*** End Patch"
        payload = {"tool_name": "apply_patch", "tool_input": {"command": command}, "tool_response": "Success", "cwd": str(self.root)}
        result = self.hook_payload(payload)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("docs/DESIGN.md:2: status-line:", result.stderr)
        payload["tool_input"]["command"] = command.replace("\n@@\n", "\n")
        result = self.hook_payload(payload)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("docs/DESIGN.md:2: status-line:", result.stderr)

    def test_codex_patch_distinguishes_fenced_duplicate_status(self):
        status = "Status: shipped (2026-10-19)"
        payload = {"tool_name": "apply_patch", "tool_input": {}, "tool_response": "Success", "cwd": str(self.root)}
        self.write("AGENTS.md", "# Rules\n```\n" + status + "\n```\n" + status + "\n")
        payload["tool_input"]["command"] = "*** Begin Patch\n*** Update File: AGENTS.md\n@@\n " + status + "\n ```\n+" + status + "\n*** End Patch"
        result = self.hook_payload(payload)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("AGENTS.md:5: status-line:", result.stderr)
        self.write("AGENTS.md", "# Rules\n```\n" + status + "\n```\n" + status + "\n")
        payload["tool_input"]["command"] = "*** Begin Patch\n*** Update File: AGENTS.md\n@@\n ```\n+" + status + "\n ```\n " + status + "\n*** End Patch"
        result = self.hook_payload(payload)
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_codex_patch_groups_sections_before_growth_check(self):
        self.write("README.md", "x" * 17000 + "\nhi\n")
        command = "*** Begin Patch\n*** Update File: README.md\n@@\n+hi\n*** Update File: README.md\n@@\n-" + "x" * 18000 + "\n+" + "x" * 17000 + "\n*** End Patch"
        payload = {"tool_name": "apply_patch", "tool_input": {"command": command}, "tool_response": "Success", "cwd": str(self.root)}
        result = self.hook_payload(payload)
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_codex_patch_multiple_chunks_skips_unmatched_file(self):
        self.write("README.md", "# Intro\n")
        self.write("AGENTS.md", "Keep.\nStatus: shipped (2026-10-19)\n")
        command = "*** Begin Patch\n*** Update File: README.md\n@@\n+Missing line\n*** Update File: AGENTS.md\n@@\n Keep.\n@@\n+Status: shipped (2026-10-19)\n*** End Patch"
        payload = {"tool_name": "apply_patch", "tool_input": {"command": command}, "tool_response": "Success", "cwd": str(self.root)}
        result = self.hook_payload(payload)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("AGENTS.md:2: status-line:", result.stderr)
        self.assertNotIn("README.md:", result.stderr)

    def test_codex_patch_blank_context_and_trailing_blanks(self):
        self.write("AGENTS.md", "Keep.\n\nStatus: shipped (2026-10-19)\n")
        payload = {"tool_name": "apply_patch", "tool_input": {}, "tool_response": "Success", "cwd": str(self.root)}
        for ending in ("*** End Patch", "\n*** End Patch", "*** End of File\n\n*** End Patch"):
            with self.subTest(ending=ending):
                payload["tool_input"]["command"] = "*** Begin Patch\n*** Update File: AGENTS.md\n@@\n Keep.\n\n+Status: shipped (2026-10-19)\n" + ending
                result = self.hook_payload(payload)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("AGENTS.md:3: status-line:", result.stderr)

    def test_grok_search_replace_snake_and_camel_case(self):
        self.write("DESIGN.md", "# Design\nStatus: shipped (2026-10-19)\n")
        payloads = [
            {"tool_name": "search_replace", "tool_input": {"target_file": "DESIGN.md", "find": "# Design\n", "replace": "# Design\nStatus: shipped (2026-10-19)\n"}, "tool_response": "Success", "cwd": str(self.root)},
            {"toolName": "search_replace", "toolInput": {"path": "DESIGN.md", "old_string": "# Design\n", "new_string": "# Design\nStatus: shipped (2026-10-19)\n"}, "toolResult": "Success", "workspaceRoot": str(self.root)},
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                result = self.hook_payload(payload)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("DESIGN.md:2: status-line:", result.stderr)

    def test_grok_inline_replacement_checks_whole_line(self):
        self.write("README.md", "Feature shipped on 2026-10-19.\n")
        payload = {"tool_name": "search_replace", "tool_input": {"target_file": "README.md", "find": "pending", "replace": "shipped on 2026-10-19"}, "tool_response": "Success", "cwd": str(self.root)}
        result = self.hook_payload(payload)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("README.md:1: status-line:", result.stderr)

    def test_grok_hashline_edit_growth_and_whole_file_without_original(self):
        self.write("README.md", "x\n" * 8500)
        payload = {"tool_name": "hashline_edit", "tool_input": {"file_path": "README.md", "find": "x\n", "replace": "x\n" * 200}, "tool_response": "Success", "cwd": str(self.root)}
        result = self.hook_payload(payload)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("README.md:0: over-target: 17000 bytes (target 16384)", result.stderr)
        payload = {"toolName": "Write", "toolInput": {"path": "README.md", "contents": "x\n" * 8500}, "toolResult": "Success", "workspaceRoot": str(self.root)}
        result = self.hook_payload(payload)
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_unpointed_readme_growth_and_status(self):
        path = self.root / "README.md"
        result = self.hook(path, "x\n" * 8500, original="x\n" * 8300)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("README.md:0: over-target: 17000 bytes (target 16384)", result.stderr)
        result = self.hook(path, "x\n" * 8500, original="x\n" * 8499)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        result = self.hook(path, "x\n" * 1000, original="x\n" * 999)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        result = self.hook(path, "x\n" * 1000 + "Last updated 2026-10-19\n", original="x\n" * 1000)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("README.md:1001: status-line:", result.stderr)

    def test_status_lines_since_and_release_verbs(self):
        path = self.root / "README.md"
        for status in ("since 2026-10-19", "deployed 2026-10-15", "shipped on 2026-10-19", "implemented 2026-10-19", "merged 2026-10-19", "released 2026-10-19", "landed 2026-10-19", "fixed 2026-10-19"):
            with self.subTest(status=status):
                result = self.hook(path, "# Project\n" + status + "\n", original="# Project\n")
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("README.md:2: status-line:", result.stderr)


if __name__ == "__main__":
    unittest.main()
