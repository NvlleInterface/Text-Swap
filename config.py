# config.py
import sys
from pathlib import Path

# En mode PyInstaller (frozen), stocker shortcuts.json à côté de l'exe
# En mode développement, à côté du fichier source
if getattr(sys, 'frozen', False):
    _APP_DIR = Path(sys.executable).parent
else:
    _APP_DIR = Path(__file__).parent

SHORTCUTS_FILE = _APP_DIR / "shortcuts.json"
APPEARANCE_MODE = "Dark"
