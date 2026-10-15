"""Exercise measure.py against temporary repositories and Claude hook payloads."""

import json
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

    def test_root_fallback_and_anchor(self):
        self.write("services/relay/AGENTS.md", "Read [design](docs/DESIGN.md#colors) first.\n")
        self.write("docs/DESIGN.md", "# Design\n")
        docs = self.report()["docs"]
        self.assertEqual([(doc["path"], doc["required"]) for doc in docs], [("docs/DESIGN.md", True)])

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
        grown = "x\n" * 8200
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


if __name__ == "__main__":
    unittest.main()
