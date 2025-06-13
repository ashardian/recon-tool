# Recon Tool

A modular CLI-based reconnaissance tool developed in Python to automate passive and active recon during red team engagements.

## 🔍 Features

- WHOIS Lookup
- DNS Enumeration (A, MX, TXT, NS)
- Subdomain Enumeration via crt.sh
- Port Scanning (multithreaded)
- Banner Grabbing
- Technology Detection (via WhatWeb)
- Report Generation (HTML)

## 🛠 Requirements

- Python 3.x
- Dependencies: see `requirements.txt`
- External: `whatweb` (must be installed separately)

## 🚀 Usage

```bash
python recon_tool.py example.com --whois --dns --subdomains --scan --banner --tech --verbose
```

## ⚙ Command-line Flags

- `--whois`: Perform WHOIS lookup
- `--dns`: DNS enumeration
- `--subdomains`: Find subdomains using crt.sh
- `--scan`: Port scan (1–1024)
- `--banner`: Banner grabbing
- `--tech`: Detect technologies (via WhatWeb)
- `--report`: Specify output file (default: `report.html`)
- `--verbose`: Enable debug logs

## 📄 Sample Report

See `/docs/sample_report.html` after running on any domain.

## 🐳 Bonus (Optional)

To Dockerize, a Dockerfile can be added (not included here).

## 📚 License

MIT
