
import socket
import time
import ipaddress
from datetime import datetime

print("Welcome to my Python Port Scanner!")

target = input("Enter the target IP address: ")

try:
    ip = ipaddress.ip_address(target)

    if not isinstance(ip, ipaddress.IPv4Address):
        raise ValueError("IPv4 addresses only")

except ValueError:
    print("Invalid IP address. Please enter a valid IPv4 address.")
    exit()


try:
    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))

except ValueError:
    print("Invalid input. Please enter numbers only.")
    exit()


if (start_port < 1 or start_port > 65535 or
    end_port < 1 or end_port > 65535):

    print("Invalid port number. Please enter ports between 1 and 65535.")
    exit()

if start_port > end_port:
    print("Invalid port range. Starting port cannot be greater than ending port.")
    exit()


print("\nScanning target:", target)
print("-----------------------------")

scan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

scan_results = []
start_time = time.time()

open_ports = 0
closed_ports = 0
timed_out_ports = 0
error_ports = 0

for port in range(start_port, end_port + 1):

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.settimeout(5)

    try:
        my_socket.connect((target, port))
        print("Port", port, "is OPEN")
        open_ports += 1
        scan_results.append(f"Port {port} is OPEN")

    except ConnectionRefusedError:
        print("Port", port, "is CLOSED")
        closed_ports += 1
        scan_results.append(f"Port {port} is CLOSED")

    except socket.timeout:
        print("Port", port, "timed out")
        timed_out_ports += 1
        scan_results.append(f"Port {port} timed out")

    except OSError as error:
        print("Port", port, "Error:", error)
        error_ports += 1
        scan_results.append(f"Port {port} Error: {error}")

    finally:
        my_socket.close()


print("-----------------------------")
print("Scan completed!")

end_time = time.time()
scan_duration = end_time - start_time

print("\nScan Summary")
print("-----------------------------")
print("Open ports:", open_ports)
print("Closed ports:", closed_ports)
print("Timed-out ports:", timed_out_ports)
print("Error ports:", error_ports)
print("Total scanned:", open_ports + closed_ports + timed_out_ports + error_ports)
print("Scan duration:", round(scan_duration, 2), "seconds")


with open("scan_results.txt", "a") as file:
    file.write("\n========== PORT SCAN REPORT ==========\n")
    file.write(f"Target IP: {target}\n")
    file.write(f"Scan date: {scan_date}\n")
    file.write(f"Ports scanned: {start_port}-{end_port}\n")

    file.write("\nScan Results:\n")

    for result in scan_results:
        file.write(result + "\n")

    file.write("\nScan Summary:\n")
    file.write(f"Open ports: {open_ports}\n")
    file.write(f"Closed ports: {closed_ports}\n")
    file.write(f"Timed-out ports: {timed_out_ports}\n")
    file.write(f"Error ports: {error_ports}\n")
    file.write(f"Total scanned: {open_ports + closed_ports + timed_out_ports + error_ports}\n")
    file.write(f"Scan duration: {round(scan_duration, 2)} seconds\n")
    file.write("======================================\n")

print("\nScan report saved to scan_results.txt")
