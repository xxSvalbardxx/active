#!/usr/bin/python3

import sys
import argparse
import socket
import time
import select
import struct


def parse_arguments():
    parser = argparse.ArgumentParser(description="Tiny Scanner: A simple port scanner.")
    parser.add_argument("-u", "--udp", type=str, help="UDP scan")
    parser.add_argument("-t", "--tcp", type=str, help="TCP scan")
    parser.add_argument(
        "-p", "--port", required=True, help="Port to scan (1 to 65535) (e.g. 22 or 22-80)"
    )
    args = parser.parse_args()
    return args

def scan_tcp_port(host, port):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    tcp_socket.settimeout(5) # setting timeout means that the connection will be closed after 5 seconds
    is_open = tcp_socket.connect_ex((host, port)) == 0
    tcp_socket.close()
    return is_open

def create_udp_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

def create_icmp_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

def scan_udp_port(host, port, timeout=5):
    udp_sock = create_udp_socket()
    icmp_sock = create_icmp_socket()
    icmp_sock.setblocking(0)  # Non-blocking mode
    icmp_sock.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
    icmp_sock.bind(("", port))
    try:
        # Envoi d'un paquet UDP vers le port cible
        udp_sock.sendto(b"", (host, port))  # Paquet UDP vide
        
        start_time = time.time()
        while True:
            current_time = time.time()
            if current_time - start_time > timeout:
                print(f"Port {port} UDP might be open/filtered (no ICMP response received)")
                return True
            
            ready = select.select([icmp_sock], [], [], timeout)
            if ready[0]:
                data, _ = icmp_sock.recvfrom(1024)
                # Extraction du type ICMP et du code à partir du paquet (en supposant un en-tête IP de 20 octets)
                icmp_type, icmp_code = struct.unpack_from("bb", data, 20)
                if icmp_type == 3 and icmp_code == 3:
                    #print(f"Port {port} UDP is closed (ICMP port unreachable received)")
                    return False
            else:
                # Timeout sans réponse ICMP
                print(f"Port {port} UDP might be open/filtered (no ICMP response received)")
                return True
    finally:
        udp_sock.close()
        icmp_sock.close()

def scan_port(host, port, is_udp=False):
    if is_udp:
        return scan_udp_port(host, port)
    return scan_tcp_port(host, port)

def handle_port_range(port_range):
    if "-" in port_range:
        start_port, end_port = map(int, port_range.split("-"))
        if not 1 <= start_port <= 65535 or not 1 <= end_port <= 65535:
            print("Invalid port range. Please specify a port between 1 and 65535.")
            sys.exit(1)
        return range(start_port, end_port + 1)
    return [int(port_range)]


def main():
    args = parse_arguments()
    ports_to_scan = handle_port_range(args.port)

    if not args.tcp and not args.udp:
        print("Please specify either TCP or UDP scan.")
        sys.exit(1)
    if args.tcp:
        print("Scanning TCP ports...")
        host = args.tcp
        is_udp = False
    if args.udp:
        print("Scanning UDP ports...")
        host = args.udp
        is_udp = True

    for port in ports_to_scan:
        is_open = scan_port(host, port, is_udp)
        status = "open" if is_open else "closed"
        if is_open:
            print(f"Port {port} is {status}")


if __name__ == "__main__":
    main()
