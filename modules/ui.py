# ui.py
import tkinter as tk
from tkinter import ttk, messagebox, Text
from ttkbootstrap import Style
from modules.shortcut_manager import load_shortcuts, save_shortcuts
from config import THEME
import pyautogui
import threading
import queue
from modules.keyboard_listener import start_keyboard_listener

def manage_shortcuts(shortcuts, get_app_active):
    global app_active
    app_active = False
    update_queue = queue.Queue()

    def on_focus_in(event):
        global app_active
        app_active = True
        print("Focus In")  # Ajout de débogage

    def on_focus_out(event):
        global app_active
        app_active = False
        print("Focus Out")  # Ajout de débogage

    def on_select(event):
        selected_item = shortcuts_list.selection()
        if selected_item:
            key, value = shortcuts_list.item(selected_item, "values")
            print(f"Selected key: {key}, value: {value}")  # Ajout de débogage
            key_entry.delete(0, tk.END)
            key_entry.insert(0, key)
            value_entry.delete(1.0, tk.END)
            value_entry.insert(tk.END, value)

    def refresh_shortcuts_list():
        for item in shortcuts_list.get_children():
            shortcuts_list.delete(item)
        for key, value in shortcuts.items():
            shortcuts_list.insert("", "end", values=(key, value))

    def add_shortcut():
        key = key_entry.get().strip()
        value = value_entry.get(1.0, tk.END).strip()
        if not key or not value:
            messagebox.showwarning("Attention", "Veuillez remplir les deux champs.")
            return
        if key in shortcuts:
            messagebox.showinfo("Info", f"Le raccourci '{key}' existe déjà.")
            return
        shortcuts[key] = value
        save_shortcuts(shortcuts)
        refresh_shortcuts_list()
        key_entry.delete(0, tk.END)
        value_entry.delete(1.0, tk.END)
        key_entry.focus_set()
        messagebox.showinfo("Succès", f"Le raccourci '{key}' a été ajouté avec succès.")

    def update_shortcut():
        selected_item = shortcuts_list.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un raccourci à modifier.")
            return
        key_to_update = shortcuts_list.item(selected_item, "values")[0]
        new_value = value_entry.get(1.0, tk.END).strip()
        if not new_value:
            messagebox.showwarning("Attention", "Veuillez saisir une nouvelle valeur.")
            return
        shortcuts[key_to_update] = new_value
        save_shortcuts(shortcuts)
        refresh_shortcuts_list()
        messagebox.showinfo("Succès", f"Le raccourci '{key_to_update}' a été mis à jour avec succès.")

    def delete_shortcut():
        selected_item = shortcuts_list.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un raccourci à supprimer.")
            return
        key_to_delete = shortcuts_list.item(selected_item, "values")[0]
        del shortcuts[key_to_delete]
        save_shortcuts(shortcuts)
        refresh_shortcuts_list()
        messagebox.showinfo("Succès", f"Le raccourci '{key_to_delete}' a été supprimé avec succès.")

    window = tk.Tk()
    window.title("Text Swap")  # Mettre à jour le titre de la fenêtre
    window.geometry("1000x800")  # Augmenter la taille de la fenêtre

    # Appliquer un thème moderne avec ttkbootstrap
    style = Style(theme=THEME)

    window.bind("<FocusIn>", on_focus_in)
    window.bind("<FocusOut>", on_focus_out)

    # Ajouter des widgets avec des styles
    label = ttk.Label(window, text="Raccourci :", style="TLabel")
    label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    key_entry = ttk.Entry(window, width=40, style="TEntry")
    key_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    key_entry.insert(0, "Entrez un mot-clé pour déclencher votre raccourci")
    key_entry.bind("<FocusIn>", lambda event: key_entry.delete(0, tk.END) if key_entry.get() == "Entrez un mot-clé pour déclencher votre raccourci" else None)

    label_value = ttk.Label(window, text="Expression complète :", style="TLabel")
    label_value.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Remplacer Entry par Text pour augmenter la hauteur
    value_entry = Text(window, width=30, height=5, wrap=tk.WORD)  # Réduire la longueur et augmenter la hauteur
    value_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    value_entry.insert(1.0, "Saisissez le texte à insérer")
    value_entry.bind("<FocusIn>", lambda event: value_entry.delete(1.0, tk.END) if value_entry.get(1.0, tk.END) == "Saisissez le texte à insérer" else None)

    # Ajouter les boutons Ajouter, Modifier et Supprimer entre le champ de texte "Expression complète" et la zone de stockage
    ttk.Button(window, text="Ajouter", command=add_shortcut, style="TButton").grid(row=2, column=1, pady=10, padx=10, sticky="w")

    # Créer un frame pour contenir les boutons Modifier et Supprimer
    button_frame = ttk.Frame(window)
    button_frame.grid(row=2, column=2, pady=10, padx=10, sticky="n")

    ttk.Button(button_frame, text="Modifier", command=update_shortcut, style="TButton").grid(row=0, column=0, pady=5, sticky="ew")
    ttk.Button(button_frame, text="Supprimer", command=delete_shortcut, style="danger.TButton").grid(row=1, column=0, pady=5, sticky="ew")

    # Ajouter le Treeview pour afficher les raccourcis et les expressions complètes
    shortcuts_list = ttk.Treeview(window, columns=("Raccourci", "Expression complète"), show="headings", height=10)
    shortcuts_list.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
    shortcuts_list.heading("Raccourci", text="Raccourci")
    shortcuts_list.heading("Expression complète", text="Expression complète")

    # Attacher l'événement de sélection
    shortcuts_list.bind("<<TreeviewSelect>>", on_select)

    # Démarrer le thread de capture des événements de clavier
    listener_thread = threading.Thread(target=start_keyboard_listener, args=(shortcuts, get_app_active, update_queue), daemon=True)
    listener_thread.start()

    # Rafraîchir la liste des raccourcis au démarrage
    refresh_shortcuts_list()

    # Démarrer la boucle principale de tkinter
    window.mainloop()
