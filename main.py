# main.py
from modules.ui import manage_shortcuts
from modules.shortcut_manager import load_shortcuts


def main():
    shortcuts = load_shortcuts()
    manage_shortcuts(shortcuts)


if __name__ == "__main__":
    main()
