#import subprocess
import socket

"""
def ping_ip(ip):
    #Retourne True si l’IP répond au ping, False sinon
    cmd = ["ping", "-c", "1", "-W", "1", ip]
    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except Exception:
        return False
"""
# scan_ping.py

import subprocess

def is_device_online(ip_address: str) -> bool:
    """
    Retourne True si le périphérique répond au ping, False sinon.
    Compatible Linux / macOS / Windows.
    """
    try:
        # Commande adaptée selon le système
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip_address],  # Linux/macOS
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Erreur dans is_device_online(): {e}")
        return False

def ping_ip(ip, port=22, timeout=1):
    """
    Vérifie si la Remarkable répond sur le port SSH.
    Retourne True si la connexion réussit, False sinon.
    """
    try:
        sock = socket.create_connection((ip, port), timeout=timeout)
        sock.close()
        return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False