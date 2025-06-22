import requests

def enumerate(domain):
    subdomains = set()

    # Try crt.sh
    try:
        print("[*] Trying crt.sh...")
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for entry in data:
                name = entry['name_value']
                for sub in name.split('\n'):
                    if domain in sub:
                        subdomains.add(sub.strip())
        if subdomains:
            return sorted(subdomains)
    except Exception as e:
        print(f"[!] crt.sh failed: {e}")

    # Fallback: AlienVault OTX
    try:
        print("[*] Trying AlienVault OTX...")
        otx_url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
        resp = requests.get(otx_url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for record in data.get("passive_dns", []):
                hostname = record.get("hostname")
                if hostname and domain in hostname:
                    subdomains.add(hostname.strip())
    except Exception as e:
        print(f"[!] OTX fallback failed: {e}")

    return sorted(subdomains)

