# config.py
from pathlib import Path

# Chemin absolu vers shortcuts.json, résolu depuis ce fichier
# (indépendant du répertoire de travail courant)
SHORTCUTS_FILE = Path(__file__).parent / "shortcuts.json"

# Apparence CustomTkinter : forcé en "Dark" pour le thème retro
APPEARANCE_MODE = "Dark"
