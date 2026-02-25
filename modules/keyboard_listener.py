# keyboard_listener.py
import threading
from pynput import keyboard
from pynput.keyboard import Controller, Key

_controller = Controller()


def _notify(word, expansion):
    """Affiche une notification système (non-bloquant, silencieux si indisponible)."""
    try:
        from plyer import notification
        msg = expansion if len(expansion) <= 60 else expansion[:57] + "..."
        notification.notify(
            title="Text Swap",
            message=f"[ {word} ]  {msg}",
            app_name="Text Swap",
            timeout=2,
        )
    except Exception:
        pass


def start_keyboard_listener(shortcuts, update_queue):
    """
    Écoute globalement les touches saisies. Quand un mot-clé est tapé
    suivi d'une espace, efface le mot-clé+espace et tape l'expression complète.
    """
    buffer = []

    def on_press(key):
        try:
            char = key.char
        except AttributeError:
            char = None

        if key == Key.space:
            word = "".join(buffer)
            if word in shortcuts:
                # Effacer : longueur du mot-clé + l'espace
                for _ in range(len(word) + 1):
                    _controller.press(Key.backspace)
                    _controller.release(Key.backspace)
                _controller.type(shortcuts[word])
                # Notification asynchrone (ne bloque pas l'injection)
                threading.Thread(
                    target=_notify, args=(word, shortcuts[word]), daemon=True
                ).start()
            buffer.clear()

        elif key == Key.backspace:
            if buffer:
                buffer.pop()

        elif char is not None and len(char) == 1:
            buffer.append(char)

        else:
            # Toute autre touche spéciale (flèches, ctrl, etc.) remet le buffer à zéro
            buffer.clear()

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()
