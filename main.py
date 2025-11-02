import sys
from PySide6.QtWidgets import QApplication
from gui.windows import MainWindow
from remarkable.connection import RemarkableConnection
from remarkable.files import RemarkableFiles

def main():
    app = QApplication(sys.argv)

    # Connexion à la reMarkable (host à remplir ou détecter automatiquement)
    host = "192.168.x.x"
    r_conn = RemarkableConnection(host, username="root")
    r_conn.connect()
    r_files = RemarkableFiles(r_conn.client)

    window = MainWindow(r_files)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
