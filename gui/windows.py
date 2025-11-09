# gui/windows.py
from PySide6.QtWidgets import (
    QMainWindow, QPushButton, QListWidget, QVBoxLayout,
    QWidget, QLabel, QMessageBox, QFileDialog, QInputDialog
)
from remarkable.application_config import load_config, save_config
from remarkable.connection import RemarkableConnection
from remarkable.files import RemarkableFiles
from PySide6.QtCore import QTimer
from remarkable.scan_ping import is_device_online
from remarkable.application_config import DEVICE_IP

class MainWindow(QMainWindow):
    def __init__(self, remarkable_ip, password):
        super().__init__()

        self.setWindowTitle("Remarkable Sync Utility")
        self.remarkable_ip = remarkable_ip  # <- CORRECTION ICI
        self.password = password
        self.connection = None  # ✅ Correction ici
        self.device_ip = DEVICE_IP
        self.file_manager = None

        # === Layout principal ===
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # === Zone de statut ===
        self.status_label = QLabel("Statut : Inconnu")
        layout.addWidget(self.status_label)

        # === Liste des statuts (historique) ===
        self.status_list = QListWidget()
        layout.addWidget(self.status_list)

        # === Boutons ===
        button_layout = QVBoxLayout()
        self.refresh_button = QPushButton("Update connection")
        self.settings_button = QPushButton("Parameters")
        self.load_button = QPushButton("Load Files")
        self.download_button = QPushButton("Download Files")

        layout.addWidget(self.status_label)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.download_button)

        # Connexions boutons
        self.refresh_button.clicked.connect(lambda: self.check_connection(show_alert=True))
        self.settings_button.clicked.connect(self.open_settings)
        self.load_button.clicked.connect(self.upload_file)
        self.download_button.clicked.connect(self.download_file)

        # === Layout principal ===
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer pour mise à jour automatique
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.check_connection(show_alert=False))
        self.timer.start(5000)

        self.check_connection()

    # --- Fonctions principales ---
    def log(self, text):
        self.status_list.addItem(text)
        self.status_list.scrollToBottom()

    def connect_remarkable(self, show_alert=False):
        """Établit la connexion SSH et initialise RemarkableFiles."""
        if self.connection and self.connection.client:
            return True  # déjà connecté

        self.connection = RemarkableConnection(self.remarkable_ip, password=self.password)
        if not self.connection.connect():
            self.log(f"❌ Could not connect to {self.remarkable_ip}")
            if show_alert:
                QMessageBox.critical(self, "Connection failed", f"Cannot connect to {self.remarkable_ip}")
            return False

        self.file_manager = RemarkableFiles(self.connection.client)
        self.log("✅ Connection established")
        return True

    def check_connection(self, show_alert=False):
        if not self.connect_remarkable(show_alert=show_alert):
            self.status_label.setText(f"❌ Hors ligne ({self.remarkable_ip})")
            return
        self.status_label.setText(f"✅ Connecté ({self.remarkable_ip})")
        try:
            files = self.file_manager.list_files()
            self.log(f"{len(files)} fichiers trouvés sur {self.remarkable_ip}")
        except Exception as e:
            self.log(f"Erreur lors de la liste des fichiers : {e}")

    def show_ip(self):
        self.status_list.clear()
        self.status_list.addItem(f"reMarkable IP: {self.remarkable_ip}")

    def open_settings(self):
        new_ip, ok = QInputDialog.getText(self, "Change reMarkable IP", "Enter new IP:", text=self.remarkable_ip)
        if ok and new_ip:
            self.remarkable_ip = new_ip
            cfg = load_config()
            cfg["remarkable_ip"] = new_ip
            save_config(cfg)
            QMessageBox.information(self, "Updated", f"New IP saved: {new_ip}")
            self.log(f"💾 IP updated to {new_ip}")

    def upload_file(self):
        if not self.connect_remarkable():
            return
        file_name, _ = QFileDialog.getOpenFileName(self, "Select file to upload")
        if not file_name:
            return
        try:
            uploaded = self.file_manager.upload_file(file_name)
            self.log(f"✅ Uploaded {uploaded} to /home/root/")
        except Exception as e:
            self.log(f"❌ Upload failed: {e}")

    def download_file(self):
        if not self.connect_remarkable():
            return
        remote_file, ok = QInputDialog.getText(self, "Download file", "Remote file path (e.g. /home/root/test.txt):")
        if not ok or not remote_file:
            return
        local_path, _ = QFileDialog.getSaveFileName(self, "Save file as")
        if not local_path:
            return
        try:
            self.file_manager.download_file(remote_file, local_path)
            self.log(f"✅ Downloaded {remote_file} → {local_path}")
        except Exception as e:
            self.log(f"❌ Download failed: {e}")
