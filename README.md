# network-scripts
# 🌐 network-scripts

> Python automation tools for network engineers — focused on Cisco IOS environments, infrastructure monitoring, and network diagnostics.

Built by a network engineer with 5+ years of NOC and IT infrastructure experience across telecom and enterprise environments.  
Currently pursuing CCNA certification and B.Sc. Computer Science (IU Germany).

---

## 📋 What's in this repo

| Script | Description | Status |
|--------|-------------|--------|
| `ping_sweep.py` | ICMP ping sweep across a subnet — live host discovery | ✅ Ready |
| `port_scanner.py` | TCP port scanner with service detection and CSV export | ✅ Ready |
| `subnet_calculator.py` | CIDR subnet calculator — network/broadcast/host range | ✅ Ready |
| `cisco_backup.py` | Automates `show running-config` backup from Cisco IOS via SSH (Netmiko) | ✅ Ready |
| `interface_checker.py` | Polls Cisco device interfaces — detects down/err-disabled states | ✅ Ready |
| `dns_lookup.py` | Bulk DNS resolver — forward/reverse lookup with export | ✅ Ready |
| `arp_monitor.py` | ARP table watcher — detects IP/MAC changes and potential spoofing | 🔧 In progress |
| `vlan_report.py` | Pulls VLAN info from Cisco switches via SSH and generates a summary | 🔧 In progress |

---

## 🧠 Why these scripts

In my years working in a Network Operations Center at beeline (VimpelCom), the most time-consuming tasks were:
- Manually checking device states during incidents
- Backing up configs before and after change windows
- Hunting for IP conflicts and ARP anomalies in large subnets

These scripts are the tools I wish I had then — and the ones I'm building now.

---

## 🛠️ Tech stack

- **Python 3.10+**
- **Netmiko** — SSH connections to Cisco IOS / IOS-XE devices
- **Paramiko** — low-level SSH where needed
- **ipaddress** — built-in Python subnet math
- **socket / scapy** — raw network operations
- **csv / json** — structured output for reporting

---

## 🚀 Getting started

```bash
# Clone the repo
git clone https://github.com/linalauda/network-scripts.git
cd network-scripts

# Install dependencies
pip install -r requirements.txt

# Run subnet calculator (no device needed)
python subnet_calculator.py 192.168.1.0/24

# Run ping sweep
python ping_sweep.py --subnet 10.0.0.0/24

# Backup Cisco device config (requires SSH access to device)
python cisco_backup.py --host 192.168.1.1 --user admin
```

---

## 📁 Project structure

```
network-scripts/
│
├── cisco/
│   ├── cisco_backup.py        # IOS config backup via SSH
│   ├── interface_checker.py   # Interface state monitor
│   └── vlan_report.py         # VLAN summary report
│
├── diagnostics/
│   ├── ping_sweep.py          # Subnet host discovery
│   ├── port_scanner.py        # TCP port scanner
│   └── arp_monitor.py         # ARP spoof detection
│
├── utils/
│   ├── subnet_calculator.py   # CIDR calculator
│   └── dns_lookup.py          # Bulk DNS resolver
│
├── requirements.txt
└── README.md
```

---

## 🔐 Security note

These tools are built for **authorized network management only**.  
Never run scanning or SSH scripts against networks you do not own or have explicit permission to test.  
All examples use RFC 1918 private address space.

---

## 📚 Background & learning context

This repo is part of my active preparation for the **Cisco CCNA certification** and the **Cisco Incubator Learning Programme (2026)**.

The scripts are grounded in real-world experience:
- 3+ years as a **NOC Engineer** at beeline Russia — monitoring production telecom and IPTV networks
- 2+ years as **IT Engineering Trainee** at comNET Solutions Group — deploying Cisco switches, firewalls, and WLAN infrastructure on client sites
- Active **Cisco NetAcad** learner: Ethical Hacking, AI Tech, English for IT

The goal: combine CLI and hardware knowledge with Python automation — the way modern network engineers actually work.

---

## 🗺️ Roadmap

- [ ] Add Cisco IOS-XE RESTCONF/YANG examples (DevNet path)
- [ ] Build a simple network topology mapper using LLDP/CDP data
- [ ] Add CheckMK integration scripts (used in professional context at comNET)
- [ ] CCNA lab topology configs (GNS3 / Packet Tracer)

---

## 📬 Contact

**Alina Kudrina**  
🔗 [linkedin.com/in/alinakudrina](https://linkedin.com/in/alinakudrina)  
✉ linakudrina@gmail.com

---

*"The best network scripts are the ones you write because you were tired of doing it by hand."*
