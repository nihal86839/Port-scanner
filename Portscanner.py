import socket
import threading
import sys
from datetime import datetime

# Configuration
TARGET = ""
PORT_RANGE_START = 0
PORT_RANGE_END = 9999
THREADS = 100  # Number of threads running simultaneously

print_lock = threading.Lock()

def scan_port(target_ip, port):
    """
    Attempts to connect to a specific port on the target IP.
    Prints the port if it is open.
    """
    try:
        # Create a TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) # Timeout to prevent hanging
        
        # Connect_ex returns 0 if connection is successful
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            with print_lock:
                print(f"[+] Open Port: {port}")
        
        s.close()
        
    except socket.error:
        # Handles cases where socket fails immediately
        pass
    except Exception as e:
        pass

def threader(target_ip, ports):
    """
    Worker function that processes ports from the list.
    """
    while True:
        try:
            # Get a port from the list
            port = ports.pop(0)
            scan_port(target_ip, port)
        except IndexError:
            # List is empty, exit thread
            break

def main():
    global TARGET, PORT_RANGE_START, PORT_RANGE_END, THREADS
    
    print("-" * 40)
    print("      PYTHON THREADED PORT SCANNER")
    print("-" * 40)
    
    # 1. Input: Link or IP
    target_input = input("Enter Target (IP or Domain): ")
    
    try:
        # Resolve domain to IP
        target_ip = socket.gethostbyname(target_input)
        TARGET = target_ip
    except socket.gaierror:
        print("[-] Error: Could not resolve hostname.")
        sys.exit()

    # 2. Input: Port Range
    try:
        p_range = input("Enter Port Range (ex 0-9999): ").split('-')
        PORT_RANGE_START = int(p_range[0])
        PORT_RANGE_END = int(p_range[1])
    except (ValueError, IndexError):
        print("[-] Error: Invalid port range format. Using default 0-9999.")
        PORT_RANGE_START = 0
        PORT_RANGE_END = 9999

    # Optional: Ask for threads
    try:
        t_input = input("Enter Number of Threads (default 100): ")
        if t_input.strip() != "":
            THREADS = int(t_input)
    except ValueError:
        print("[-] Invalid thread number. Using default.")

    print(f"\n[!] Scanning Target: {target_ip}")
    print(f"[!] Port Range: {PORT_RANGE_START} - {PORT_RANGE_END}")
    print(f"[!] Threads: {THREADS}")
    print(f"[!] Started at: {datetime.now()}")
    print("-" * 40)

    # Create a list of ports to scan
    ports_to_scan = list(range(PORT_RANGE_START, PORT_RANGE_END + 1))
    
    # 3. Threading Logic
    thread_list = []
    
    # Create and start threads
    for _ in range(THREADS):
        t = threading.Thread(target=threader, args=(target_ip, ports_to_scan))
        t.start()
        thread_list.append(t)
    
    # Wait for all threads to finish
    for t in thread_list:
        t.join()

    print("-" * 40)
    print(f"[!] Scan Completed at: {datetime.now()}")

if __name__ == "__main__":
    main()
