import argparse
import subprocess
import socket
import requests
import json
import pythonwhois
import dns.resolver
import datetime
import logging
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Setup Logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# WHOIS Lookup
def whois_lookup(domain):
    logger.info("Performing WHOIS lookup...")
    try:
        info = pythonwhois.get_whois(domain)
        return json.dumps(info, indent=2)
    except Exception as e:
        logger.error(f"WHOIS lookup failed: {e}")
        return "WHOIS lookup failed"

# DNS Enumeration
def dns_enum(domain):
    logger.info("Performing DNS enumeration...")
    records = {}
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8', '1.1.1.1']  # Use Google and Cloudflare DNS
    try:
        for rtype in ['A', 'MX', 'TXT', 'NS']:
            try:
                answers = resolver.resolve(domain, rtype, raise_on_no_answer=False)
                records[rtype] = [r.to_text() for r in answers]
            except Exception as e:
                records[rtype] = f"Error: {e}"
    except Exception as e:
        logger.error(f"DNS enumeration failed: {e}")
    return records

# Subdomain Enumeration
def subdomain_enum(domain):
    logger.info("Enumerating subdomains using crt.sh...")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subdomains = set()
    try:
        resp = requests.get(url, timeout=10)
        for entry in resp.json():
            name = entry['name_value']
            for sub in name.split('\n'):
                if domain in sub:
                    subdomains.add(sub.strip())
    except Exception as e:
        logger.error(f"Subdomain enumeration failed: {e}")
    return list(subdomains)

# Fast Port Scanning with Threads
def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((host, port)) == 0:
                return port
    except:
        pass
    return None

def port_scan(host, ports):
    logger.info("Scanning ports with threads...")
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, host, port) for port in ports]
        for f in futures:
            result = f.result()
            if result:
                open_ports.append(result)
    return open_ports

# Banner Grabbing
def banner_grab(target, port):
    try:
        with socket.socket() as s:
            s.settimeout(2)
            s.connect((target, port))
            banner = s.recv(1024).decode(errors='ignore').strip()
            return banner
    except:
        return "No banner found"

# Technology Detection using whatweb CLI (assumes installed)
def tech_detect(domain):
    logger.info("Detecting technologies...")
    try:
        output = subprocess.check_output(["whatweb", domain], stderr=subprocess.DEVNULL).decode()
        return output
    except Exception as e:
        logger.error(f"Technology detection failed: {e}")
        return "Technology detection failed"

# Generate Report
def generate_report(data, filename="report.html"):
    logger.info(f"Generating report {filename}...")
    time = datetime.datetime.now().isoformat()
    html = f"""
    <html><head><title>Recon Report</title></head><body>
    <h1>Reconnaissance Report</h1>
    <p><strong>Generated:</strong> {time}</p>
    <h2>WHOIS Info</h2><pre>{data.get('whois')}</pre>
    <h2>DNS Records</h2><pre>{json.dumps(data.get('dns'), indent=2)}</pre>
    <h2>Subdomains</h2><pre>{json.dumps(data.get('subdomains'), indent=2)}</pre>
    <h2>Open Ports</h2><pre>{data.get('ports')}</pre>
    <h2>Banners</h2><pre>{json.dumps(data.get('banners'), indent=2)}</pre>
    <h2>Technology Detection</h2><pre>{data.get('tech')}</pre>
    </body></html>
    """
    with open(filename, "w") as f:
        f.write(html)

# Main CLI Parser
def main():
    parser = argparse.ArgumentParser(description="Advanced Recon Tool")
    parser.add_argument("target", help="Target domain or IP (e.g., example.com)")
    parser.add_argument("--whois", action="store_true", help="Perform WHOIS lookup")
    parser.add_argument("--dns", action="store_true", help="Perform DNS enumeration")
    parser.add_argument("--subdomains", action="store_true", help="Find subdomains using crt.sh")
    parser.add_argument("--scan", action="store_true", help="Scan common ports (1–1024)")
    parser.add_argument("--banner", action="store_true", help="Grab banners from open ports")
    parser.add_argument("--tech", action="store_true", help="Detect technologies via WhatWeb")
    parser.add_argument("--report", default="report.html", help="Output report filename (default: report.html)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose/debug logging")
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    data = {}
    if args.whois:
        data['whois'] = whois_lookup(args.target)
    if args.dns:
        data['dns'] = dns_enum(args.target)
    if args.subdomains:
        data['subdomains'] = subdomain_enum(args.target)
    if args.scan:
        ports = list(range(1, 1025))
        data['ports'] = port_scan(args.target, ports)
    if args.banner and 'ports' in data:
        data['banners'] = {p: banner_grab(args.target, p) for p in data['ports']}
    if args.tech:
        data['tech'] = tech_detect(args.target)

    if any([args.whois, args.dns, args.subdomains, args.scan, args.banner, args.tech]):
        generate_report(data, args.report)
        logger.info("Recon complete. Report saved as " + args.report)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
