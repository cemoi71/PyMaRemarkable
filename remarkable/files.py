import os
from paramiko import SFTPClient

class RemarkableFiles:
    def __init__(self, ssh_client):
        self.ssh_client = ssh_client

    def list_files(self, remote_dir="/home/root/"):
        sftp = self.ssh_client.open_sftp()
        files = sftp.listdir(remote_dir)
        sftp.close()
        return files

    def download_file(self, remote_path, local_path):
        sftp = self.ssh_client.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()

    def upload_file(self, local_path, remote_path):
        sftp = self.ssh_client.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()
