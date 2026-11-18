"""Exercise distill-session's episodes.py matcher and folder hash."""
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
SCRIPT = Path(__file__).resolve().parent.parent / "skills/distill-session/scripts/episodes.py"
spec = importlib.util.spec_from_file_location("episodes", SCRIPT)
episodes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(episodes)


class EpisodeTests(unittest.TestCase):
    def test_read_matcher(self):
        cases = {
            "cat /x/.agents/skills/read-source/SKILL.md": ["read-source"],
            "sed -n '1,200p' /x/skills/verify-ui/SKILL.md": ["verify-ui"],
            "rg foo .; cat /x/skills/diagnose-root/SKILL.md": ["diagnose-root"],
            "python3 -c \"print(open('/x/skills/inspect-db/SKILL.md').read())\"": ["inspect-db"],
            '{"target_file":"/x/.grok/skills/find-icon/SKILL.md"}': ["find-icon"],
            'printf "%s" /x/skills/ship-pr/SKILL.md': [],
            "rg -n foo /x/skills/ship-pr/SKILL.md": [],
            "# see skills/ship-pr/SKILL.md\nls": [],
            "cat verify-pr/examples/merge.md": [],
        }
        for command, expected in cases.items():
            with self.subTest(command=command):
                self.assertEqual(episodes.READ.findall(command), expected)

    def test_codex_listing_is_not_an_episode_and_exclude_applies(self):
        with tempfile.TemporaryDirectory() as home:
            day = Path(home, ".codex/sessions/2026/11/18")
            day.mkdir(parents=True)
            rows = [
                {"type": "session_meta", "payload": {"cwd": "/repo"}},
                {"type": "response_item", "payload": {"type": "message", "content": [{"type": "input_text", "text": "skills/ship-pr/SKILL.md"}]}},
                {"type": "response_item", "payload": {"type": "custom_tool_call", "name": "exec", "input": "cat /h/.agents/skills/verify-pr/SKILL.md"}},
            ]
            path = day / "rollout-2026-11-18T00-00-00-abc.jsonl"
            path.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
            original = episodes.HOME
            episodes.HOME = home
            try:
                found = episodes.episodes({"ship-pr", "verify-pr"}, 7, "")
                self.assertEqual([(e["harness"], e["skill"], e["line"]) for e in found], [("codex", "verify-pr", 3)])
                self.assertEqual(episodes.episodes({"verify-pr"}, 7, "abc"), [])
            finally:
                episodes.HOME = original

    def test_hash_ignores_hidden_and_cache_dirs(self):
        with tempfile.TemporaryDirectory() as root:
            skill = Path(root, "demo")
            (skill / ".cache").mkdir(parents=True)
            (skill / "SKILL.md").write_text("# Demo\n")
            before = episodes.folder_hash(str(skill))
            (skill / ".cache/state").write_text("changed")
            (skill / "__pycache__").mkdir()
            (skill / "__pycache__/x.pyc").write_bytes(b"0")
            self.assertEqual(episodes.folder_hash(str(skill)), before)
            (skill / "SKILL.md").write_text("# Demo edited\n")
            self.assertNotEqual(episodes.folder_hash(str(skill)), before)


if __name__ == "__main__":
    unittest.main()
