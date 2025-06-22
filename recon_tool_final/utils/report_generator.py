import json
import datetime

def generate_report(data, filename="report.html"):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""
    <html>
    <head>
        <title>Recon Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; padding: 20px; }}
            h1 {{ color: #003366; }}
            pre {{ background: #fff; padding: 10px; border: 1px solid #ccc; overflow-x: auto; }}
            .section {{ margin-bottom: 30px; }}
            .section h2 {{ color: #004080; border-bottom: 2px solid #ccc; }}
            ul {{ list-style-type: disc; margin-left: 20px; }}
        </style>
    </head>
    <body>
        <h1>Reconnaissance Report</h1>
        <p><strong>Generated:</strong> {time}</p>
        <div class="section">
            <h2>WHOIS Info</h2>
            <pre>{data.get('whois', 'No result')}</pre>
        </div>
        <div class="section">
            <h2>DNS Records</h2>
            <pre>{json.dumps(data.get('dns', 'No result'), indent=2)}</pre>
        </div>
        <div class="section">
            <h2>Subdomains</h2>
            <pre>{json.dumps(data.get('subdomains', 'No result'), indent=2)}</pre>
        </div>
        <div class="section">
            <h2>Open Ports</h2>
            <pre>{data.get('ports', 'No result')}</pre>
        </div>
        <div class="section">
            <h2>Banners</h2>
            <ul>
    """
    banners = data.get('banners', {})
    if banners:
        for port, banner in banners.items():
            html += f"<li><strong>Port {port}:</strong><pre>{banner}</pre></li>"
    else:
        html += "<li>No result</li>"

    html += """
            </ul>
        </div>
        <div class="section">
            <h2>Technology Detection</h2>
    """
    tech_output = data.get('tech', '').strip()
    if tech_output:
        html += "<ul>"
        for line in tech_output.splitlines():
            html += f"<li><pre>{line}</pre></li>"
        html += "</ul>"
    else:
        html += "<pre>No result</pre>"

    html += """
        </div>
        <footer style="margin-top:50px;font-size:0.9em;color:#555;">
            <hr>
            <p>&copy; Recon Tool by Ashar Dian</p>
        </footer>
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

