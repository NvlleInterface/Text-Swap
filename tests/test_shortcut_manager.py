import unittest
import tempfile
from pathlib import Path
from unittest import mock


class TestShortcutManager(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="w", encoding="utf-8"
        )
        self.tmp.write("{}")
        self.tmp.close()
        self.patcher = mock.patch(
            "modules.shortcut_manager.SHORTCUTS_FILE", Path(self.tmp.name)
        )
        self.patcher.start()
        import modules.shortcut_manager as sm
        import importlib
        importlib.reload(sm)
        self.sm = sm

    def tearDown(self):
        self.patcher.stop()
        Path(self.tmp.name).unlink(missing_ok=True)

    def test_load_empty(self):
        result = self.sm.load_shortcuts()
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_save_and_load(self):
        data = {"sig": "Cordialement,\nAlice"}
        self.sm.save_shortcuts(data)
        loaded = self.sm.load_shortcuts()
        self.assertEqual(loaded, data)

    def test_load_missing_file(self):
        Path(self.tmp.name).unlink()
        result = self.sm.load_shortcuts()
        self.assertEqual(result, {})

    def test_unicode_shortcuts(self):
        data = {"café": "Bonne journée !"}
        self.sm.save_shortcuts(data)
        loaded = self.sm.load_shortcuts()
        self.assertEqual(loaded, data)


if __name__ == "__main__":
    unittest.main()
