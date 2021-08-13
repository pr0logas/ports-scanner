#!/usr/bin/env python3
##: Author: Tomas Andriekus
##: Date: 2021-08-12
##: Description: This script tries to check if it's possible to make a connection with the specific endpoint port. 
##: This is very useful to ensure secure infrastructure and consistency with the firewall rules.

import socket
import sys
import threading
import time


TARGETS_FILE = 'ALL_final.txt'
PORT_SCAN_START = 1
PORT_SCAN_END = 9999
CUSTOM_PORTS = [27017, 27018, 27019]
PORTS_NOT_TO_SCAN = [53]
targets = []
ports = []
results = []
process_status_success = [True]


def read_hosts_from_text_file():
    with open(TARGETS_FILE, 'r') as file:
        result = file.readlines()

        for host in result:
            targets.append(host.split()[1])

    # Remove checker host
    targets.remove('some-specific-host')


def populate_which_ports_to_scan():
    for port in range(PORT_SCAN_START,PORT_SCAN_END):
        ports.append(port)

    ports.extend(CUSTOM_PORTS)

    for port in PORTS_NOT_TO_SCAN:
        ports.remove(port)


def check_port(s, target, port):
    try:
        result = s.connect_ex((target, port))

        if result == 0:
            info = f"Port is open - {target}:{port}"
            print("")
            print(info)
            print("")
            results.append(info)
            process_status_success[0] = False
        s.close()

    except KeyboardInterrupt:
        print("\n Exitting Program !!!!")
        sys.exit(1)
    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        print(f"{target}:{port}")
        sys.exit(0)
    except socket.error:
        print("\n Server not responding !!!!")
        print(f"{target}:{port}")
        sys.exit(1)
    except:
        sys.exit(1)


populate_which_ports_to_scan()
read_hosts_from_text_file()


print(f"How many hosts: {len(targets)}")
print(f"Scanning ports from: {PORT_SCAN_START} to {PORT_SCAN_END} + custom ports - {CUSTOM_PORTS}")
print(f"Exception for ports: {PORTS_NOT_TO_SCAN}")


for host in targets:
    print(f"Scanning host: {host}")

    for port in ports:
        socket.setdefaulttimeout(0.500)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread(target=check_port, args=(s, host, port)).start()
        time.sleep(0.001)


if not process_status_success[0]:
    print(results)
    print(f"Infrastructure is insecure! Attention is needed!")
    sys.exit(1)
else:
    print(f"ALL ports are closed. DappRadar infrastructure is secure")
