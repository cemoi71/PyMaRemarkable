# fichier : scan_ping.py
# Usage: python3 scan_ping.py

import ipaddress
import subprocess
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def make_cidr(ip):
    return str(ipaddress.ip_network(ip + "/24", strict=False))

def ping(ip):
    # ping une fois, timeout court
    # -c 1 : 1 paquet, -W 1 : timeout 1s (sur Linux)
    cmd = ["ping", "-c", "1", "-W", "1", ip]
    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except Exception:
        return False

def scan_network(network, workers=100):
    ips = [str(ip) for ip in ipaddress.ip_network(network).hosts()]
    alive = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(ping, ip): ip for ip in ips}
        for fut in as_completed(futures):
            ip = futures[fut]
            if fut.result():
                try:
                    host = socket.gethostbyaddr(ip)[0]
                except Exception:
                    host = ""
                alive.append({"ip": ip, "hostname": host})
    return alive

def print_devices(devices):
    if not devices:
        print("No devices found.")
        return
    print(f"{'IP':16} {'Hostname'}")
    print("-"*40)
    for d in sorted(devices, key=lambda x: x['ip']):
        print(f"{d['ip']:16} {d['hostname']}")

if __name__ == "__main__":
    local_ip = get_local_ip()
    cidr = make_cidr(local_ip)
    print(f"Local IP detected : {local_ip} -> scan on {cidr}")
    devices = scan_network(cidr)
    print_devices(devices)
