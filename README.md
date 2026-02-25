# Text Swap

> Tapez un mot-clé, appuyez sur espace — Text Swap le remplace par le texte complet.

```
 _____ ____ _  _ _____    ____ _ _ _ ____ ____
 |  |  |___  \/   |      [__  | | | |__| |__/
 |  |  |___ _/\_  |      ___] |_|_| |  | |  \
```

---

## Installation

### Windows

```bat
pip install -r requirements.txt
python main.py
```

### Linux

#### 1. Dépendances système

**Ubuntu / Debian**
```bash
sudo apt-get install -y python3 python3-pip python3-tk gir1.2-appindicator3-0.1
```

**Fedora**
```bash
sudo dnf install -y python3 python3-pip python3-tkinter libappindicator-gtk3
```

**Arch Linux**
```bash
sudo pacman -Sy python python-pip tk libappindicator-gtk3
```

#### 2. Dépendances Python

```bash
pip3 install -r requirements.txt
```

#### 3. Accès clavier sans sudo (pynput)

Sur Linux, `pynput` a besoin que votre utilisateur soit dans le groupe `input` :

```bash
sudo usermod -aG input $USER
```

> Déconnectez-vous et reconnectez-vous pour appliquer le changement.

**Wayland (GNOME 45+)** : si le listener ne fonctionne pas, activez l'accessibilité :
```bash
gsettings set org.gnome.desktop.interface toolkit-accessibility true
```

#### 4. System tray (GNOME)

Installez l'extension GNOME **AppIndicator and KStatusNotifierItem Support** :
```bash
# via le gestionnaire d'extensions, ou :
sudo gnome-extensions install appindicatorsupport@rgcjonas.gmail.com
```

#### 5. Installation rapide (script)

Un script d'installation complet est disponible :

```bash
sudo ./install.sh
```

Il installe les dépendances système, configure les groupes, crée un lanceur desktop et une commande `text-swap` dans `/usr/local/bin`.

---

## Lancement

```bash
python main.py         # Windows
python3 main.py        # Linux
text-swap              # Linux après install.sh
```

---

## Utilisation

| Action | Description |
|---|---|
| Tapez un mot-clé + `Espace` | Déclenche l'expansion |
| `Retour arrière` | Corrige le mot-clé en cours de frappe |
| Toute autre touche spéciale | Remet le buffer à zéro |
| Fermer la fenêtre | Réduit dans le system tray |
| Tray → Quitter | Ferme complètement l'app |

---

## Build (exécutable)

```bash
pip install pyinstaller
pyinstaller main.spec
# → dist/TextSwap (Linux) ou dist/TextSwap.exe (Windows)
```

---

## Stack

- **UI** : [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- **Keyboard** : [pynput](https://pynput.readthedocs.io/)
- **Tray** : [pystray](https://github.com/moses-palmer/pystray)
- **Notifications** : [plyer](https://github.com/kivy/plyer)
