import keyboard

def start_keyboard_listener(shortcuts, get_app_active):
    buffer = ""

    def on_key_event(event):
        nonlocal buffer
        print(f"Event: {event}")  # Ajout de débogage
        if not get_app_active():
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == "space":
                    print(f"Buffer: {buffer}")  # Ajout de débogage
                    if buffer in shortcuts:
                        print(f"Replacing {buffer} with {shortcuts[buffer]}")  # Ajout de débogage
                        keyboard.write("\b" * (len(buffer) + 1))
                        keyboard.write(shortcuts[buffer])
                    buffer = ""
                elif event.name == "backspace":
                    buffer = buffer[:-1]
                elif len(event.name) == 1:
                    buffer += event.name
                else:
                    buffer = ""

    keyboard.hook(on_key_event)
