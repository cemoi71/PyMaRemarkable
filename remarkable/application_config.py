# application_config.py
import json
import os

CONFIG_FILE = "config.json"
DEFAULT_IP = "192.168.178.60"  # ton IP connue par défaut
DEVICE_IP = "192.168.178.60"

def load_config():
    """Charge la configuration depuis config.json ou crée une par défaut."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass  # si corrompu, on recrée un nouveau fichier
    return {"remarkable_ip": DEFAULT_IP}

def save_config(cfg):
    """Sauvegarde la configuration."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)
