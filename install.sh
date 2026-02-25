#!/bin/bash
# install.sh — Installation de Text Swap sur Linux
# Usage : sudo ./install.sh

set -e

# ── Vérifications ─────────────────────────────────────────────────────────── #
if [ "$EUID" -ne 0 ]; then
    echo "[!] Ce script doit être lancé avec sudo :"
    echo "    sudo ./install.sh"
    exit 1
fi

REAL_USER="${SUDO_USER:-$USER}"
REAL_HOME=$(eval echo "~$REAL_USER")
INSTALL_DIR="/opt/text-swap"
BIN_LINK="/usr/local/bin/text-swap"
DESKTOP_FILE="/usr/share/applications/text-swap.desktop"
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║       TEXT SWAP — Installation       ║"
echo "╚══════════════════════════════════════╝"
echo ""

# ── Détection du gestionnaire de paquets ──────────────────────────────────── #
echo "[1/5] Détection du système..."

if command -v apt-get &>/dev/null; then
    echo "      → Ubuntu / Debian détecté"
    apt-get install -y python3 python3-pip python3-tk gir1.2-appindicator3-0.1 \
        libnotify-bin 2>/dev/null || true

elif command -v dnf &>/dev/null; then
    echo "      → Fedora / RHEL détecté"
    dnf install -y python3 python3-pip python3-tkinter libappindicator-gtk3 \
        libnotify 2>/dev/null || true

elif command -v pacman &>/dev/null; then
    echo "      → Arch Linux détecté"
    pacman -Sy --noconfirm python python-pip tk libappindicator-gtk3 \
        libnotify 2>/dev/null || true

else
    echo "      [!] Gestionnaire de paquets non reconnu."
    echo "          Installez manuellement : python3, python3-pip, python3-tk"
    echo "          et le paquet AppIndicator de votre distro."
fi

# ── Copie des fichiers ─────────────────────────────────────────────────────── #
echo "[2/5] Copie dans $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
cp -r "$SOURCE_DIR/." "$INSTALL_DIR/"
chown -R "$REAL_USER:$REAL_USER" "$INSTALL_DIR"

# Créer shortcuts.json vide si absent
if [ ! -f "$INSTALL_DIR/shortcuts.json" ]; then
    echo "{}" > "$INSTALL_DIR/shortcuts.json"
    chown "$REAL_USER:$REAL_USER" "$INSTALL_DIR/shortcuts.json"
fi

# ── Dépendances Python ─────────────────────────────────────────────────────── #
echo "[3/5] Installation des dépendances Python..."
sudo -u "$REAL_USER" pip3 install -r "$INSTALL_DIR/requirements.txt" --quiet

# ── Groupe input (pynput sans sudo) ───────────────────────────────────────── #
echo "[4/5] Configuration du groupe 'input'..."
if id "$REAL_USER" &>/dev/null; then
    usermod -aG input "$REAL_USER"
    echo "      → $REAL_USER ajouté au groupe 'input'"
fi

# ── Lanceur et entrée desktop ─────────────────────────────────────────────── #
echo "[5/5] Création du lanceur..."

# Commande /usr/local/bin/text-swap
cat > "$BIN_LINK" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
exec python3 main.py "\$@"
EOF
chmod +x "$BIN_LINK"

# Entrée .desktop (menu application)
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=Text Swap
Comment=Expanseur de texte — tapez un raccourci et appuyez sur espace
Exec=$BIN_LINK
Icon=$INSTALL_DIR/icon.png
Terminal=false
Type=Application
Categories=Utility;
StartupNotify=false
Keywords=text;expand;shortcut;macro;
EOF

# Actualiser la base des applications
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# ── Résumé ─────────────────────────────────────────────────────────────────── #
echo ""
echo "╔══════════════════════════════════════╗"
echo "║       Installation terminée !        ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "  Commande : text-swap"
echo "  Dossier  : $INSTALL_DIR"
echo ""
echo "  [!] IMPORTANT : déconnectez-vous puis reconnectez-vous"
echo "      pour activer le groupe 'input' (nécessaire au"
echo "      listener clavier sans sudo)."
echo ""
echo "  Sur Wayland, si le listener ne fonctionne pas :"
echo "  gsettings set org.gnome.desktop.interface toolkit-accessibility true"
echo ""
