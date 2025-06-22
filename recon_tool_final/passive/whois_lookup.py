import subprocess

def lookup(domain):
    try:
        result = subprocess.check_output(["whois", domain], stderr=subprocess.DEVNULL).decode()
        return result
    except Exception as e:
        return f"Error: {e}"
