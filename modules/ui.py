# ui.py
import sys
import threading
from pathlib import Path

import customtkinter as ctk
from tkinter import messagebox
import pystray
from PIL import Image, ImageDraw

from modules.shortcut_manager import save_shortcuts
from modules.keyboard_listener import start_keyboard_listener

# ── Thème ──────────────────────────────────────────────────────────────────── #
THEME_FILE = str(Path(__file__).parent.parent / "theme_retro.json")
ICON_FILE  = Path(__file__).parent.parent / "textswap-icon.png"
MONO_FONT  = "Courier New" if sys.platform == "win32" else "DejaVu Sans Mono"

# Palette — paires [light, dark] → CTk switche automatiquement au toggle
C_BG         = ["#f8f3ec", "#080808"]
C_PANEL      = ["#ede7db", "#0f0f0f"]
C_BORDER     = ["#c8bfb0", "#2a2a2a"]
C_ACCENT     = ["#c05a0a", "#f97316"]
C_ACCENT_DIM = ["#8a3d08", "#7a3808"]
C_TEXT       = ["#2e1f0a", "#c8b89a"]
C_TEXT_DIM   = ["#8a7a60", "#4a3a28"]
C_ROW        = ["#f3ede4", "#0d0d0d"]
C_ROW_ALT    = ["#ebe4da", "#111111"]
C_ROW_SEL    = ["#fde8cc", "#1c0f03"]
C_SEP        = ["#d8d0c0", "#1e1e1e"]
C_HDR_BG     = ["#e5ddd0", "#0c0c0c"]
C_RED        = ["#8b1a1a", "#8b1a1a"]
C_RED_HOV    = ["#b22222", "#b22222"]
ACCENT_LINE  = "#f97316"


def _create_tray_image():
    if ICON_FILE.exists():
        return Image.open(ICON_FILE).resize((64, 64)).convert("RGB")
    img = Image.new("RGB", (64, 64), color="#080808")
    d = ImageDraw.Draw(img)
    d.rectangle([3, 3, 61, 61], outline="#f97316", width=2)
    d.text((16, 18), "TS", fill="#f97316")
    return img


def _font(size=12, bold=False):
    return ctk.CTkFont(family=MONO_FONT, size=size, weight="bold" if bold else "normal")


def _label(parent, text, bold=False, size=12, text_color=None, **kw):
    return ctk.CTkLabel(
        parent, text=text, font=_font(size, bold),
        text_color=text_color if text_color is not None else C_TEXT,
        **kw,
    )


def _btn(parent, text, command, width=120, red=False):
    return ctk.CTkButton(
        parent, text=text, command=command, width=width, height=30,
        font=_font(12), corner_radius=0, border_width=1,
        fg_color=C_RED        if red else C_PANEL,
        hover_color=C_RED_HOV if red else C_ACCENT,
        border_color=C_RED    if red else C_ACCENT,
        text_color=C_TEXT,
    )


def manage_shortcuts(shortcuts):
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme(THEME_FILE)

    window = ctk.CTk()
    window.title("TEXT SWAP  //  v0.2")
    window.geometry("920x560")
    window.minsize(700, 420)
    window.configure(fg_color=C_BG)

    # Icône fenêtre — ICO temporaire pour Windows (iconbitmap est plus fiable qu'iconphoto)
    if ICON_FILE.exists():
        try:
            import tempfile
            _img = Image.open(ICON_FILE).convert("RGBA")
            _ico_path = Path(tempfile.gettempdir()) / "textswap_icon.ico"
            _img.resize((32, 32)).save(str(_ico_path), format="ICO", sizes=[(32, 32)])
            window.iconbitmap(str(_ico_path))
        except Exception:
            pass

    selected_key = [None]
    tray_icon    = [None]
    mode_state   = ["Dark"]

    # ── BARRE TITRE ─────────────────────────────────────────────────────── #
    title_bar = ctk.CTkFrame(window, fg_color=C_PANEL, corner_radius=0, border_width=0)
    title_bar.pack(fill="x")
    ctk.CTkFrame(title_bar, height=2, fg_color=ACCENT_LINE, corner_radius=0).pack(fill="x")

    _label(title_bar, "  TEXT SWAP  //  v0.2", bold=True, size=14,
           text_color=C_ACCENT).pack(side="left", pady=5, padx=4)
    _label(title_bar, "raccourci + espace pour expanser  ",
           size=11, text_color=C_TEXT_DIM).pack(side="right", pady=5)

    def toggle_mode():
        new = "Light" if mode_state[0] == "Dark" else "Dark"
        mode_state[0] = new
        ctk.set_appearance_mode(new)
        mode_btn.configure(text="[ ☀ ]" if new == "Dark" else "[ ● ]")

    mode_btn = _btn(title_bar, "[ ● ]", toggle_mode, width=52)
    mode_btn.pack(side="right", padx=(0, 8), pady=4)

    # ── CORPS PRINCIPAL (deux colonnes) ─────────────────────────────────── #
    body = ctk.CTkFrame(window, fg_color="transparent", corner_radius=0)
    body.pack(fill="both", expand=True, padx=10, pady=(8, 10))
    body.columnconfigure(1, weight=1)
    body.rowconfigure(0, weight=1)

    # ── PANNEAU GAUCHE : formulaire + boutons ────────────────────────────── #
    LEFT_W = 280
    left_panel = ctk.CTkFrame(body, fg_color=C_PANEL, corner_radius=0,
                               border_width=1, border_color=C_BORDER, width=LEFT_W)
    left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
    left_panel.pack_propagate(False)

    # — Titre panneau gauche
    ctk.CTkFrame(left_panel, height=1, fg_color=C_ACCENT_DIM, corner_radius=0).pack(fill="x")
    _label(left_panel, " NOUVEAU RACCOURCI", bold=True, size=14,
           text_color=C_ACCENT).pack(anchor="w", padx=8, pady=(6, 5))
    ctk.CTkFrame(left_panel, height=1, fg_color=C_ACCENT_DIM, corner_radius=0).pack(fill="x")

    # — Champ raccourci (label + entry inline, hauteur fixe comme les lignes du tableau)
    row_key = ctk.CTkFrame(left_panel, fg_color=C_BG, corner_radius=0,
                           border_width=1, border_color=C_ACCENT, height=28)
    row_key.pack(fill="x", padx=8, pady=(6, 0))
    row_key.pack_propagate(False)
    _label(row_key, " raccourci :", size=11, text_color=C_ACCENT, width=96, anchor="w").pack(
        side="left", pady=0, padx=0
    )
    ctk.CTkFrame(row_key, width=1, fg_color=C_ACCENT, corner_radius=0).pack(
        side="left", fill="y", pady=0
    )
    key_entry = ctk.CTkEntry(
        row_key, border_width=0, corner_radius=0,
        font=_font(13), fg_color=C_BG,
        text_color=C_TEXT, placeholder_text_color=C_TEXT_DIM,
        placeholder_text="ex: sig",
    )
    key_entry.pack(side="left", fill="x", expand=True, pady=0, padx=4)

    # — Champ expansion (label simple + textbox)
    _label(left_panel, " expansion :", size=11, text_color=C_ACCENT).pack(
        anchor="w", padx=8, pady=(6, 1)
    )
    value_entry = ctk.CTkTextbox(
        left_panel, height=84, wrap="word",
        font=_font(13), corner_radius=0, border_width=1,
        border_color=C_ACCENT, fg_color=C_BG, text_color=C_TEXT,
    )
    value_entry.pack(fill="x", padx=8, pady=(0, 6))

    # — Séparateur
    ctk.CTkFrame(left_panel, height=1, fg_color=C_ACCENT_DIM, corner_radius=0).pack(fill="x")

    # — Boutons actions
    btn_frame = ctk.CTkFrame(left_panel, fg_color="transparent", corner_radius=0)
    btn_frame.pack(fill="x", padx=8, pady=6)

    def add_shortcut():
        key = key_entry.get().strip()
        value = value_entry.get("1.0", "end").strip()
        if not key or not value:
            messagebox.showwarning("Attention", "Remplissez les deux champs.")
            return
        if key in shortcuts:
            messagebox.showinfo("Info", f"'{key}' existe déjà.")
            return
        shortcuts[key] = value
        save_shortcuts(shortcuts)
        key_entry.delete(0, "end")
        value_entry.delete("1.0", "end")
        selected_key[0] = None
        refresh_list()

    def update_shortcut():
        if not selected_key[0]:
            messagebox.showwarning("Attention", "Sélectionnez un raccourci dans le tableau.")
            return
        new_key   = key_entry.get().strip()
        new_value = value_entry.get("1.0", "end").strip()
        if not new_value:
            messagebox.showwarning("Attention", "Saisissez une valeur.")
            return
        # Si la clé a changé, supprimer l'ancienne
        if new_key and new_key != selected_key[0]:
            del shortcuts[selected_key[0]]
            selected_key[0] = new_key
        shortcuts[selected_key[0]] = new_value
        save_shortcuts(shortcuts)
        refresh_list()

    def delete_shortcut():
        if not selected_key[0]:
            messagebox.showwarning("Attention", "Sélectionnez un raccourci dans le tableau.")
            return
        if messagebox.askyesno("Supprimer", f"Supprimer '{selected_key[0]}' ?"):
            del shortcuts[selected_key[0]]
            save_shortcuts(shortcuts)
            selected_key[0] = None
            key_entry.delete(0, "end")
            value_entry.delete("1.0", "end")
            refresh_list()

    def clear_form():
        selected_key[0] = None
        key_entry.delete(0, "end")
        value_entry.delete("1.0", "end")
        refresh_list()

    _btn(btn_frame, "+ ajouter",   add_shortcut,    width=LEFT_W - 16).pack(fill="x", pady=(0, 2))
    _btn(btn_frame, "~ modifier",  update_shortcut, width=LEFT_W - 16).pack(fill="x", pady=(0, 2))
    _btn(btn_frame, "x supprimer", delete_shortcut, width=LEFT_W - 16, red=True).pack(fill="x", pady=(0, 2))
    _btn(btn_frame, "∅ vider",     clear_form,      width=LEFT_W - 16).pack(fill="x")

    # ── PANNEAU DROIT : filtre + tableau ─────────────────────────────────── #
    right_panel = ctk.CTkFrame(body, fg_color=C_PANEL, corner_radius=0,
                                border_width=1, border_color=C_BORDER)
    right_panel.grid(row=0, column=1, sticky="nsew")

    # — Barre filtre / compteur
    filter_bar = ctk.CTkFrame(right_panel, fg_color=C_HDR_BG, corner_radius=0)
    filter_bar.pack(fill="x")
    ctk.CTkFrame(filter_bar, height=1, fg_color=C_ACCENT_DIM, corner_radius=0).pack(fill="x")

    search_bar_inner = ctk.CTkFrame(filter_bar, fg_color="transparent", corner_radius=0, height=30)
    search_bar_inner.pack(fill="x", padx=8, pady=3)
    search_bar_inner.pack_propagate(False)

    _label(search_bar_inner, "filtre :", size=11, text_color=C_ACCENT).pack(side="left", padx=(0, 4))
    search_var = ctk.StringVar()
    ctk.CTkEntry(
        search_bar_inner, height=28, font=_font(12),
        corner_radius=0, border_width=1,
        fg_color=C_BG, border_color=C_BORDER,
        text_color=C_TEXT, placeholder_text_color=C_TEXT_DIM,
        placeholder_text="rechercher...",
        textvariable=search_var,
    ).pack(side="left", fill="x", expand=True)
    search_var.trace_add("write", lambda *_: refresh_list())

    count_label = _label(search_bar_inner, "0 entrée(s)", size=12, text_color=C_TEXT)
    count_label.pack(side="right", padx=(8, 0))

    # — En-tête colonnes (hauteur fixe, comme les lignes)
    col_key_w = 160
    hdr = ctk.CTkFrame(right_panel, fg_color=C_HDR_BG, corner_radius=0, height=26)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    _label(hdr, " RACCOURCI", bold=True, size=12,
           text_color=C_ACCENT, width=col_key_w, anchor="w").pack(side="left", pady=0)
    ctk.CTkFrame(hdr, width=1, fg_color=C_ACCENT_DIM, corner_radius=0).pack(
        side="left", fill="y", pady=0
    )
    _label(hdr, " EXPANSION", bold=True, size=12,
           text_color=C_ACCENT, anchor="w").pack(side="left", pady=0, padx=4)
    ctk.CTkFrame(right_panel, height=1, fg_color=C_ACCENT_DIM, corner_radius=0).pack(fill="x")

    # — Liste défilante
    list_scroll = ctk.CTkScrollableFrame(
        right_panel, fg_color=C_BG, corner_radius=0,
        scrollbar_button_color=C_ACCENT_DIM,
        scrollbar_button_hover_color=C_ACCENT,
    )
    list_scroll.pack(fill="both", expand=True)

    row_widgets = []

    def on_row_click(k, v, rf, idx):
        for i, (r, _, _) in enumerate(row_widgets):
            r.configure(fg_color=C_ROW if i % 2 == 0 else C_ROW_ALT)
        rf.configure(fg_color=C_ROW_SEL)
        selected_key[0] = k
        key_entry.delete(0, "end")
        key_entry.insert(0, k)
        value_entry.delete("1.0", "end")
        value_entry.insert("1.0", v)

    def refresh_list():
        nonlocal row_widgets
        for rf, _, _ in row_widgets:
            rf.destroy()
        row_widgets.clear()

        filter_text = search_var.get().lower()
        idx = 0
        for k, v in shortcuts.items():
            if filter_text and filter_text not in k.lower() and filter_text not in v.lower():
                continue
            bg = C_ROW if idx % 2 == 0 else C_ROW_ALT
            rf = ctk.CTkFrame(list_scroll, fg_color=bg, corner_radius=0, height=26)
            rf.pack(fill="x", pady=0)
            rf.pack_propagate(False)

            lbl_k = ctk.CTkLabel(
                rf, text=f" {k}", width=col_key_w, anchor="w",
                font=_font(12, bold=True), text_color=C_ACCENT,
            )
            lbl_k.pack(side="left", pady=0, padx=0)

            ctk.CTkFrame(rf, width=1, fg_color=C_SEP, corner_radius=0).pack(
                side="left", fill="y", pady=0
            )

            disp = v.replace("\n", " ↵ ")
            if len(disp) > 80:
                disp = disp[:77] + "…"
            lbl_v = ctk.CTkLabel(
                rf, text=f" {disp}", anchor="w",
                font=_font(12), text_color=C_TEXT,
            )
            lbl_v.pack(side="left", pady=0, fill="x", expand=True)

            _idx = idx
            for w in (rf, lbl_k, lbl_v):
                w.bind("<Button-1>", lambda e, k=k, v=v, rf=rf, i=_idx: on_row_click(k, v, rf, i))
            row_widgets.append((rf, k, v))
            idx += 1

        total = len(shortcuts)
        count_label.configure(
            text=f"{idx}/{total}" if filter_text else f"{total} entrée(s)"
        )

    # ── SYSTEM TRAY ─────────────────────────────────────────────────────── #
    def show_window():
        window.deiconify()
        window.lift()
        window.focus_force()

    def quit_app(icon, item):
        icon.stop()
        window.quit()

    def on_close():
        window.withdraw()
        icon = pystray.Icon(
            "text_swap", _create_tray_image(), "Text Swap",
            menu=pystray.Menu(
                pystray.MenuItem("Afficher", lambda: window.after(0, show_window)),
                pystray.MenuItem("Quitter",  quit_app),
            ),
        )
        tray_icon[0] = icon
        icon.run_detached()

    window.protocol("WM_DELETE_WINDOW", on_close)

    # ── DÉMARRAGE ───────────────────────────────────────────────────────── #
    threading.Thread(
        target=start_keyboard_listener, args=(shortcuts, None), daemon=True
    ).start()

    refresh_list()
    window.mainloop()
