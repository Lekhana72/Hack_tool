import socket
import ipaddress
import subprocess
import platform
import re

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None

def get_mac_address(ip):
    """Get MAC address by sending ARP request (works on Windows/Linux)"""
    if platform.system().lower() == "windows":
        # Windows ARP command
        output = subprocess.check_output(f"arp -a {ip}", shell=True, text=True)
        match = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", output)
    else:
        # Linux/Mac ARP command
        output = subprocess.check_output(f"arp {ip}", shell=True, text=True)
        match = re.search(r"([0-9a-f]{2}:){5}[0-9a-f]{2}", output)

    return match.group(0) if match else None

def scan_network(network, method="tcp", port=80):
    active_hosts = []
    for ip in ipaddress.IPv4Network(network, strict=False):
        ip_str = str(ip)
        try:
            if method == "tcp":
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                if sock.connect_ex((ip_str, port)) == 0:
                    hostname = get_hostname(ip_str)
                    mac = get_mac_address(ip_str)
                    active_hosts.append((ip_str, hostname, mac))
                sock.close()

            elif method == "ping":
                param = "-n" if platform.system().lower() == "windows" else "-c"
                command = ["ping", param, "1", ip_str]
                if subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                    hostname = get_hostname(ip_str)
                    mac = get_mac_address(ip_str)
                    active_hosts.append((ip_str, hostname, mac))

        except Exception:
            pass
    return active_hosts

if __name__ == "__main__":
    network = input("Enter network (e.g. 192.168.1.0/24): ")
    method = input("Method ('tcp' or 'ping') [tcp]: ") or "tcp"
    port = 80
    if method == "tcp":
        port = int(input("TCP port to test (default 80): ") or 80)

    results = scan_network(network, method, port)

    print("\nResponsive hosts:")
    for ip, hostname, mac in results:
        print(f" - {ip} | Hostname: {hostname or 'N/A'} | MAC: {mac or 'N/A'}")

