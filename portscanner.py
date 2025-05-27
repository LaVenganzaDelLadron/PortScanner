import socket
import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

ADB_PORT_RANGE = range(0, 99999)

def timestamp():
    return datetime.now().strftime("[%H:%M:%S]")

def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            return sock.connect_ex((ip, port)) == 0
    except:
        return False

def try_adb_connect(ip, port):
    try:
        output = subprocess.check_output(["adb", "connect", f"{ip}:{port}"], stderr=subprocess.STDOUT)
        result = output.decode().strip()
        if "connected" in result.lower() or "already connected" in result.lower():
            return True, result
        return False, result
    except subprocess.CalledProcessError as e:
        return False, e.output.decode().strip()
    except Exception as e:
        return False, str(e)

def scan_port(ip, port):
    if is_port_open(ip, port):
        success, response = try_adb_connect(ip, port)
        if success:
            return (port, "✓", f"ADB CONNECTED ({response})")
        else:
            return (port, "✗", f"Port OPEN, ADB FAILED: {response}")
    return None

def scan_ip(ip):
    results = []
    print(f"\n{timestamp()} Scanning ports 0–99999 on {ip}...")
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in ADB_PORT_RANGE}
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
                port, status, message = result
                print(f" ├─ [{status}] {str(port).ljust(6)} → {message}")
    return results

def main():
    target_range = input("Enter public IP or range (e.g., 192.168.1.0/24 or 192.168.1.5): ")

    try:
        network = ipaddress.IPv4Network(target_range, strict=False)
        targets = [str(ip) for ip in network.hosts()]
    except ValueError:
        targets = [target_range]

    print(f"\n{timestamp()} Starting brute-force ADB scan on {target_range}...\n")

    found_devices = []
    for ip in targets:
        results = scan_ip(ip)
        found_devices.extend([(ip, port) for port, status, _ in results if status == "✓"])

    print(f"\n{timestamp()} Scan complete.\n")

    if found_devices:
        print("[+] ADB Devices Found:")
        for ip, port in found_devices:
            print(f" └─ {ip}:{port}")
    else:
        print("[!] No open ADB ports found.")

if __name__ == "__main__":
    main()
