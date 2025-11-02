import paramiko

class RemarkableConnection:
    def __init__(self, host, username="root", password=None):
        self.host = host
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.host, username=self.username, password=self.password)
            return True
        except Exception as e:
            print("Erreur de connexion:", e)
            return False

    def is_connected(self):
        return self.client is not None

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None
