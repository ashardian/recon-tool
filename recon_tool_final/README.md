# Recon Tool (Modular & Colorful CLI)

## 🔍 Features
- Passive Recon:
  - WHOIS Lookup
  - DNS Records (A, MX, TXT, NS)
  - Subdomain Enumeration (crt.sh)
- Active Recon:
  - Port Scanning (multithreaded)
  - Banner Grabbing
  - Technology Detection (via WhatWeb)
- Reporting:
  - HTML Summary with timestamps and all data
  - Colorful CLI Output

## 🚀 Usage
```bash
python3 main.py example.com --whois --dns --subdomains --scan --banner --tech --verbose
```

## 📦 Requirements
```bash
pip install -r requirements.txt
sudo apt install whatweb
```
