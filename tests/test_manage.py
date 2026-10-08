import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("manage", Path(__file__).parents[1] / "tools/manage.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        self.target = self.base / "installed"
        self.profile = self.base / "profile.json"
        self.profile.write_text('{"skills":["one"]}')
        self.source = self.repo / "skills/one"
        self.source.mkdir(parents=True)
        (self.source / "SKILL.md").write_text("original")
        (self.repo / "catalog.json").write_text(json.dumps({"skills": {
            "one": {"path": "skills/one", "status": "selected"}
        }}))
        self.patcher = patch.object(m, "REPO", self.repo)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def run_apply(self):
        m.apply(m.plan(self.profile, self.target), self.target)

    def test_preview_is_read_only(self):
        self.assertEqual(m.plan(self.profile, self.target)[0][-1], "install")
        self.assertFalse(self.target.exists())

    def test_install_idempotent_update_backup(self):
        self.run_apply()
        self.assertEqual(m.plan(self.profile, self.target)[0][-1], "unchanged")
        (self.source / "SKILL.md").write_text("updated")
        self.run_apply()
        self.assertEqual((self.target / "one/SKILL.md").read_text(), "updated")
        backups = list(self.base.glob("skill-central-backup-*/one/SKILL.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "original")

    def test_unmanaged_and_local_edits_blocked(self):
        self.target.mkdir()
        (self.target / "one").mkdir()
        with self.assertRaises(ValueError):
            m.plan(self.profile, self.target)
        (self.target / "one").rmdir()
        self.run_apply()
        (self.target / "one/SKILL.md").write_text("local edit")
        with self.assertRaises(ValueError):
            m.plan(self.profile, self.target)

    def test_missing_skill_preflight(self):
        self.profile.write_text('{"skills":["one","missing"]}')
        with self.assertRaises(KeyError):
            m.plan(self.profile, self.target)
        self.assertFalse(self.target.exists())

    def test_bad_names_duplicates_and_repository_target(self):
        for names in [["../one"], ["one", "one"]]:
            self.profile.write_text(json.dumps({"skills": names}))
            with self.assertRaises(ValueError):
                m.plan(self.profile, self.target)
        self.profile.write_text('{"skills":["one"]}')
        with self.assertRaises(ValueError):
            m.plan(self.profile, self.repo / "installed")

    def test_candidates_require_explicit_flag(self):
        catalog = self.repo / "catalog.json"
        catalog.write_text(catalog.read_text().replace("selected", "candidate"))
        with self.assertRaises(ValueError):
            m.plan(self.profile, self.target)
        self.assertEqual(m.plan(self.profile, self.target, True)[0][-1], "install")

    def test_runtime_files_excluded(self):
        (self.source / "__pycache__").mkdir()
        (self.source / "__pycache__/a.pyc").write_bytes(b"cache")
        self.run_apply()
        self.assertFalse((self.target / "one/__pycache__").exists())

    def test_mid_apply_failure_restores_previous_copy(self):
        self.run_apply()
        (self.source / "SKILL.md").write_text("updated")
        rows = m.plan(self.profile, self.target)
        original_rename = Path.rename

        def fail_stage(path, target):
            if "skill-central-stage-" in str(path) and path.name == "one":
                raise OSError("simulated rename failure")
            return original_rename(path, target)

        with patch.object(Path, "rename", fail_stage):
            with self.assertRaises(OSError):
                m.apply(rows, self.target)
        self.assertEqual((self.target / "one/SKILL.md").read_text(), "original")


if __name__ == "__main__":
    unittest.main()
