# keyboard_listener.py
import keyboard
from modules.shortcut_manager import load_shortcuts, save_shortcuts
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import pyautogui
import threading
import queue

def start_keyboard_listener(shortcuts, get_app_active, update_queue):
    buffer = ""

    def on_key_event(event):
        nonlocal buffer
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "space":
                if buffer in shortcuts:
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
    keyboard.wait()
