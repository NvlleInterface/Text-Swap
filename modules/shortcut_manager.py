import json
from config import SHORTCUTS_FILE

# Charger les raccourcis depuis un fichier JSON
def load_shortcuts():
    try:
        with open(SHORTCUTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Sauvegarder les raccourcis dans un fichier JSON
def save_shortcuts(shortcuts_dict):
    with open(SHORTCUTS_FILE, "w") as file:
        json.dump(shortcuts_dict, file, indent=4)
