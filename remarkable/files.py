# remarkable/files.py
class RemarkableFiles:
    def __init__(self, ssh_client):
        self.ssh_client = ssh_client

    def list_files(self, remote_dir="/home/root"):
        """Liste les fichiers du dossier distant."""
        sftp = self.ssh_client.open_sftp()
        files = sftp.listdir(remote_dir)
        sftp.close()
        return files

    def upload_file(self, local_path, remote_path="/home/root/"):
        """Envoie un fichier local vers la tablette."""
        sftp = self.ssh_client.open_sftp()
        filename = local_path.split("/")[-1]
        sftp.put(local_path, remote_path + filename)
        sftp.close()
        return filename

    def download_file(self, remote_path, local_path):
        """Télécharge un fichier depuis la tablette."""
        sftp = self.ssh_client.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()
