# 🔍 Recon Tool by Ashar Dian

A lightweight, modular, and color-enhanced reconnaissance CLI tool designed for red team and penetration testing scenarios.

---

## 📌 Features

### 🕵️ Passive Recon Modules
| Module          | Description                                              |
|-----------------|----------------------------------------------------------|
| WHOIS Lookup    | Gathers domain registration details                      |
| DNS Enumeration | Retrieves A, MX, TXT, NS records from public resolvers   |
| Subdomain Enum  | Uses `crt.sh` to find subdomains of the target           |

### 🚀 Active Recon Modules
| Module          | Description                                              |
|-----------------|----------------------------------------------------------|
| Port Scanning   | Multithreaded TCP scan on common ports (1–1024)          |
| Banner Grabbing | Extracts HTTP/HTTPS headers for basic fingerprinting     |
| Tech Detection  | Uses `whatweb` to detect server technologies             |

---

## 🎨 CLI Output
- Color-coded terminal output for clarity
- Structured JSON-like presentation
- Verbose logging with `--verbose` flag

---

## 📝 Report Generation
- Output: HTML report with all gathered data
- Includes timestamp and target info
- Structured and styled for readability

---

## 🚀 How to Use

## 🧰 Setting Up a Virtual Environment (Recommended)

To avoid dependency conflicts, it is recommended to create and use a Python virtual environment.

```bash
# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # For Linux/macOS

```


### 🔧 Installation

```bash
git clone https://github.com/ashardian/recon-tool
cd recon-tool
pip install -r requirements.txt
sudo apt install whatweb whois
cd recon_tool_final
```

### 🧪 Run Example

```bash
python3 main.py example.com --whois --dns --subdomains --scan --banner --tech --verbose
```

---

## 🔧 CLI Options

| Flag            | Description                             |
|-----------------|-----------------------------------------|
| `--whois`       | Perform WHOIS lookup                    |
| `--dns`         | Perform DNS enumeration                 |
| `--subdomains`  | Discover subdomains                     |
| `--scan`        | Scan common ports (1–1024)              |
| `--banner`      | Grab HTTP/HTTPS banners from open ports |
| `--tech`        | Detect technologies via WhatWeb         |
| `--report`      | Output report filename (HTML)           |
| `--verbose`     | Enable debug logging                    |

---

## 🗂 Directory Structure

```
recon_tool_final/
├── main.py
├── active/
│   ├── banner_grab.py
│   ├── port_scan.py
│   └── tech_detect.py
├── passive/
│   ├── whois_lookup.py
│   ├── dns_enum.py
│   └── subdomain_enum.py
├── utils/
│   └── report_generator.py
├── docs/
├── requirements.txt
└── README.md
```

---

## 👨‍💻 Author
**Ashar Dian**  
Tool developed for summer offensive security internship task.

(c) 2025 — All rights reserved.

---
