# main.py
import sys
from PySide6.QtWidgets import QApplication, QInputDialog, QLineEdit
from gui.windows import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # IP de la tablette
    remarkable_ip = "192.168.178.60"

    # Fenêtre pour demander le mot de passe (masqué)
    password, ok = QInputDialog.getText(
        None,
        "Mot de passe reMarkable",
        f"Entrez le mot de passe pour {remarkable_ip}:",
        QLineEdit.EchoMode.Password  # ✅ Syntaxe correcte
    )
    if not ok or not password:
        sys.exit(0)  # on quitte si pas de mot de passe

    window = MainWindow(remarkable_ip, password)
    window.show()

    sys.exit(app.exec())
