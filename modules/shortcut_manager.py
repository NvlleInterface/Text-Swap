# shortcut_manager.py
import json
from config import SHORTCUTS_FILE


def load_shortcuts():
    try:
        with open(SHORTCUTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_shortcuts(shortcuts_dict):
    with open(SHORTCUTS_FILE, "w", encoding="utf-8") as f:
        json.dump(shortcuts_dict, f, indent=4, ensure_ascii=False)
