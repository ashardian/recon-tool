import argparse
import logging
from colorama import Fore, Style, init
from passive import whois_lookup, dns_enum, subdomain_enum
from active import port_scan, banner_grab, tech_detect
from utils.report_generator import generate_report

init(autoreset=True)

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def print_result(title, content):
    print(Fore.CYAN + f"\n=== {title} ===")
    if isinstance(content, dict) or isinstance(content, list):
        import json
        print(Fore.GREEN + json.dumps(content, indent=2))
    else:
        print(Fore.GREEN + str(content))

def main():
    parser = argparse.ArgumentParser(description="Modular Recon Tool with Color Output")
    parser.add_argument("target", help="Target domain or IP")
    parser.add_argument("--whois", action="store_true", help="WHOIS lookup")
    parser.add_argument("--dns", action="store_true", help="DNS enumeration")
    parser.add_argument("--subdomains", action="store_true", help="Subdomain enumeration")
    parser.add_argument("--scan", action="store_true", help="Port scan")
    parser.add_argument("--banner", action="store_true", help="Banner grabbing")
    parser.add_argument("--tech", action="store_true", help="Technology detection")
    parser.add_argument("--report", default="report.html", help="Report output file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    data = {}
    if args.whois:
        data['whois'] = whois_lookup.lookup(args.target)
        print_result("WHOIS Lookup", data['whois'])
    if args.dns:
        data['dns'] = dns_enum.enumerate(args.target)
        print_result("DNS Records", data['dns'])
    if args.subdomains:
        data['subdomains'] = subdomain_enum.enumerate(args.target)
        print_result("Subdomains", data['subdomains'])
    if args.scan:
        ports = list(range(1, 1025))
        data['ports'] = port_scan.scan(args.target, ports)
        print_result("Open Ports", data['ports'])
    if args.banner and 'ports' in data:
        data['banners'] = {p: banner_grab.grab(args.target, p) for p in data['ports']}
        print_result("Banners", data['banners'])
    if args.tech:
        data['tech'] = tech_detect.detect(args.target)
        print_result("Technology Detection", data['tech'])

    if any([args.whois, args.dns, args.subdomains, args.scan, args.banner, args.tech]):
        generate_report(data, args.report)
        print(Fore.YELLOW + f"\n[+] Report saved to {args.report}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
