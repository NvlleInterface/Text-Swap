# main.py
import tkinter as tk
from tkinter import ttk
from modules.ui import manage_shortcuts
from modules.shortcut_manager import load_shortcuts
from ttkbootstrap import Style

def get_app_active():
    # Cette fonction doit retourner True si l'application est active, False sinon.
    # Vous pouvez implémenter cette fonction en fonction de vos besoins spécifiques.
    return True

def main():
    # Charger les raccourcis depuis le fichier JSON
    shortcuts = load_shortcuts()

    # Lancer l'interface utilisateur pour gérer les raccourcis
    manage_shortcuts(shortcuts, get_app_active)

if __name__ == "__main__":
    main()
