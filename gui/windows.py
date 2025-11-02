from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QListWidget, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self, remarkable):
        super().__init__()
        self.remarkable = remarkable
        self.setWindowTitle("reMarkable Sync")

        # Layout principal
        layout = QVBoxLayout()

        # Boutons
        self.btn_settings = QPushButton("Parameters")
        self.btn_search = QPushButton("Search devices")
        self.btn_upload = QPushButton("Load file")
        self.btn_download = QPushButton("Download file")

        layout.addWidget(self.btn_settings)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.btn_upload)
        layout.addWidget(self.btn_download)

        # Explorateur de fichiers
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connecter boutons à fonctions (à implémenter)
        self.btn_search.clicked.connect(self.search_tablet)
        self.btn_upload.clicked.connect(self.upload_file)
        self.btn_download.clicked.connect(self.download_file)

    def search_tablet(self):
        # TODO : chercher les tablettes en ligne
        pass

    def upload_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select file to upload")
        if file_name:
            # TODO : appeler remarkable.files.upload_file
            pass

    def download_file(self):
        selected_items = self.file_list.selectedItems()
        for item in selected_items:
            # TODO : appeler remarkable.files.download_file
            pass
