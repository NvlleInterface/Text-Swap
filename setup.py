from cx_Freeze import setup, Executable

# Remplacez 'main.py' par le nom de votre script Python
executables = [Executable("main.py", base="Win32GUI")]

setup(
    name="LockIn",
    version="0.1",
    description="Assistant that helps you create more shortcuts for your daily tasks",
    executables=executables,
    options={
        "build_exe": {
            "packages": ["tkinter", "keyboard", "ttkbootstrap"],  # Ajoutez ici les packages nécessaires
            "include_files": ["shortcuts.json"]  # Ajoutez ici les fichiers nécessaires
        }
    }
)
