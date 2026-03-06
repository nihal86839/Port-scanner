import socket
import threading
import sys
from datetime import datetime

# Lock for printing to console safely
print_lock = threading.Lock()

def get_banner(sock):
    """Try to grab a banner from the service"""
    try:
        sock.settimeout(1)
        return sock.recv(1024).decode().strip()
    except:
        return None

def scan_port(target_ip, port, results_list):
    """
    Scans a single port. If open, adds to the results list.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            # Port is open
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "unknown"
            
            # Add to shared list
            results_list.append((port, service))
            
        s.close()
        
    except Exception:
        pass

def main():
    print("-" * 50)
    print("       UPGRADED PYTHON PORT SCANNER")
    print("-" * 50)

    # 1. Input Target
    target_input = input("Enter Target IP or Domain: ")
    try:
        target_ip = socket.gethostbyname(target_input)
    except socket.gaierror:
        print("[-] Error: Hostname could not be resolved.")
        sys.exit()

    # 2. Input Port Range
    try:
        port_range = input("Enter Port Range (ex 0-9999): ").split('-')
        start_port = int(port_range[0])
        end_port = int(port_range[1])
    except (ValueError, IndexError):
        print("[-] Invalid range. Using default 0-1024.")
        start_port = 0
        end_port = 1024

    # 3. Input Threads
    try:
        thread_count = int(input("Enter Threads (ex 100): "))
    except ValueError:
        print("[-] Invalid number. Using default 50.")
        thread_count = 50

    print(f"\n[!] Scanning {target_ip} from port {start_port} to {end_port}...")
    print(f"[!] Started at: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 50)

    # List to hold results
    open_ports = []
    threads = []
    
    start_time = datetime.now()

    # Create and start threads
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target_ip, port, open_ports))
        threads.append(t)
        t.start()
        
        # Limit active threads to the user defined number
        # This prevents the computer from crashing if scanning 0-9999
        while threading.active_count() > thread_count:
            pass

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # 4. Print results 1 by 1 (Sorted)
    # Sort the list by port number (item[0])
    open_ports.sort(key=lambda x: x[0])

    print(f"\n[+] Scan Complete. Found {len(open_ports)} open ports:")
    print("-" * 50)
    
    if open_ports:
        for port, service in open_ports:
            print(f"    [OPEN] Port {port} ({service})")
    else:
        print("    No open ports found.")

    end_time = datetime.now()
    print("-" * 50)
    print(f"[!] Duration: {end_time - start_time}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[-] Scan stopped by user.")
        sys.exit()
