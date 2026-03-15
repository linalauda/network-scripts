#!/usr/bin/env python3
"""
subnet_calculator.py
--------------------
A command-line subnet calculator for network engineers.

Accepts any IPv4 address in CIDR notation (e.g. 192.168.1.0/24)
and returns everything you need to know about that subnet:
  - Network address
  - Broadcast address
  - Subnet mask (dotted decimal)
  - Wildcard mask
  - First and last usable host
  - Total number of usable hosts
  - IP class (A / B / C)
  - Whether the address is private or public

Usage:
  python subnet_calculator.py 192.168.1.0/24
  python subnet_calculator.py 10.0.0.0/8
  python subnet_calculator.py 172.16.5.100/20

Author: Alina Kudrina
GitHub: https://github.com/linalauda
"""

import ipaddress
import argparse
import sys


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def get_ip_class(ip: ipaddress.IPv4Address) -> str:
    """
    Returns the IP class (A, B, C, D, or E) based on the first octet.
    This is classic CCNA knowledge — the original classful addressing system.

    Class A: 1–126    (large networks, e.g. 10.x.x.x)
    Class B: 128–191  (medium networks, e.g. 172.16.x.x)
    Class C: 192–223  (small networks, e.g. 192.168.x.x)
    Class D: 224–239  (multicast)
    Class E: 240–255  (reserved / experimental)
    """
    first_octet = int(str(ip).split('.')[0])

    if 1 <= first_octet <= 126:
        return "A"
    elif first_octet == 127:
        return "A (loopback — not usable)"
    elif 128 <= first_octet <= 191:
        return "B"
    elif 192 <= first_octet <= 223:
        return "C"
    elif 224 <= first_octet <= 239:
        return "D (multicast)"
    else:
        return "E (reserved)"


def get_wildcard_mask(netmask: ipaddress.IPv4Address) -> str:
    """
    Wildcard mask = inverse of the subnet mask.
    Used in Cisco ACLs and OSPF configuration.
    Example: 255.255.255.0 → wildcard is 0.0.0.255
    """
    mask_octets = str(netmask).split('.')
    wildcard_octets = [str(255 - int(octet)) for octet in mask_octets]
    return '.'.join(wildcard_octets)


def is_private(ip: ipaddress.IPv4Address) -> str:
    """
    Checks if the IP falls within RFC 1918 private address ranges:
      10.0.0.0/8
      172.16.0.0/12
      192.168.0.0/16

    Private addresses are not routable on the public internet.
    NAT translates them to public IPs at the network edge.
    """
    return "Private (RFC 1918)" if ip.is_private else "Public"


def format_output(network_input: str) -> None:
    """
    Main calculation function.
    Takes a CIDR string, parses it, and prints a formatted summary.
    """

    # ── Parse the input ──────────────────────────────────────────
    # strict=False means 192.168.1.50/24 is accepted and treated as
    # the network 192.168.1.0/24 — just like Cisco IOS does.
    try:
        network = ipaddress.IPv4Network(network_input, strict=False)
        host_ip = ipaddress.IPv4Address(network_input.split('/')[0])
    except ValueError as e:
        print(f"\n  [ERROR] Invalid input: {e}")
        print("  Use CIDR format, e.g.  192.168.1.0/24\n")
        sys.exit(1)

    # ── Extract all the values we need ──────────────────────────
    prefix_len      = network.prefixlen                   # e.g. 24
    netmask         = network.netmask                     # e.g. 255.255.255.0
    wildcard        = get_wildcard_mask(network.netmask)  # e.g. 0.0.0.255
    network_addr    = network.network_address             # first address in subnet
    broadcast_addr  = network.broadcast_address           # last address in subnet
    ip_class        = get_ip_class(network_addr)
    privacy         = is_private(host_ip)

    # Total hosts = 2^(32 - prefix) — includes network & broadcast
    # Usable hosts = total - 2 (subtract network address and broadcast)
    # Exception: /32 = single host, /31 = point-to-point link (RFC 3021)
    total_hosts = network.num_addresses

    if prefix_len == 32:
        first_host = str(network_addr)
        last_host  = str(network_addr)
        usable     = 1
    elif prefix_len == 31:
        # RFC 3021: /31 used for point-to-point, both addresses are usable
        hosts_list = list(network.hosts())
        first_host = str(hosts_list[0]) if hosts_list else str(network_addr)
        last_host  = str(hosts_list[-1]) if hosts_list else str(broadcast_addr)
        usable     = 2
    else:
        hosts_list = list(network.hosts())
        first_host = str(hosts_list[0])   # network_addr + 1
        last_host  = str(hosts_list[-1])  # broadcast_addr - 1
        usable     = len(hosts_list)

    # ── Print the result ─────────────────────────────────────────
    width = 30  # column width for alignment

    print()
    print("  ╔══════════════════════════════════════════════════╗")
    print(f"  ║   Subnet Calculator · {network_input:<27}║")
    print("  ╠══════════════════════════════════════════════════╣")
    print(f"  ║  {'Input IP Address':<{width}} {str(host_ip):<18}  ║")
    print(f"  ║  {'Network Address':<{width}} {str(network_addr):<18}  ║")
    print(f"  ║  {'Broadcast Address':<{width}} {str(broadcast_addr):<18}  ║")
    print(f"  ║  {'Subnet Mask':<{width}} {str(netmask):<18}  ║")
    print(f"  ║  {'Wildcard Mask':<{width}} {wildcard:<18}  ║")
    print(f"  ║  {'CIDR Prefix Length':<{width}} /{prefix_len:<17}  ║")
    print("  ╠══════════════════════════════════════════════════╣")
    print(f"  ║  {'First Usable Host':<{width}} {first_host:<18}  ║")
    print(f"  ║  {'Last Usable Host':<{width}} {last_host:<18}  ║")
    print(f"  ║  {'Usable Hosts':<{width}} {usable:<18,}  ║")
    print(f"  ║  {'Total Addresses (incl. net+bc)':<{width}} {total_hosts:<18,}  ║")
    print("  ╠══════════════════════════════════════════════════╣")
    print(f"  ║  {'IP Class':<{width}} {ip_class:<18}  ║")
    print(f"  ║  {'Address Type':<{width}} {privacy:<18}  ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print()


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="IPv4 Subnet Calculator — CIDR notation input",
        epilog="Examples:\n"
               "  python subnet_calculator.py 192.168.1.0/24\n"
               "  python subnet_calculator.py 10.0.0.0/8\n"
               "  python subnet_calculator.py 172.16.5.100/20",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "network",
        help="IPv4 address with CIDR prefix, e.g. 192.168.1.0/24"
    )

    # If no arguments given, print help and exit cleanly
    if len(sys.argv) == 1:
        parser.print_help()
        print("\n  Quick example:  python subnet_calculator.py 192.168.1.0/24\n")
        sys.exit(0)

    args = parser.parse_args()
    format_output(args.network)


if __name__ == "__main__":
    main()
