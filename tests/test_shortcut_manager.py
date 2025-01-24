import unittest
from modules.shortcut_manager import load_shortcuts, save_shortcuts

class TestShortcutManager(unittest.TestCase):
    def test_load_shortcuts(self):
        shortcuts = load_shortcuts()
        self.assertIsInstance(shortcuts, dict)

    def test_save_shortcuts(self):
        shortcuts = {"test": "value"}
        save_shortcuts(shortcuts)
        loaded_shortcuts = load_shortcuts()
        self.assertEqual(loaded_shortcuts, shortcuts)

if __name__ == "__main__":
    unittest.main()
