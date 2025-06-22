import socket
import ssl

def grab(host, port):
    try:
        # Create socket connection
        with socket.create_connection((host, port), timeout=3) as sock:
            sock.settimeout(3)
            if port in [443, 8443, 9443]:
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    return get_http_headers(ssock, host)
            else:
                return get_http_headers(sock, host, secure=False)
    except Exception as e:
        return f"Error: {e}"

def get_http_headers(sock, host, secure=True):
    try:
        request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        sock.sendall(request.encode())
        response = sock.recv(4096).decode(errors='ignore')
        headers = response.split('\r\n')
        parsed = [h for h in headers if ':' in h or h.startswith('HTTP')]
        return '\n'.join(parsed)
    except Exception as e:
        return f"Error reading headers: {e}"
