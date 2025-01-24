import threading
from modules.shortcut_manager import load_shortcuts, save_shortcuts
from modules.ui import manage_shortcuts
from modules.keyboard_listener import start_keyboard_listener

# Charger les raccourcis
shortcuts = load_shortcuts()

# Variable pour suivre l'état de l'application
app_active = False

# Lancer l'écoute globale dans un thread séparé
keyboard_thread = threading.Thread(target=start_keyboard_listener, args=(shortcuts, lambda: app_active), daemon=True)
keyboard_thread.start()

# Lancer l'interface de gestion des raccourcis dans le thread principal
manage_shortcuts(shortcuts, lambda: app_active)
