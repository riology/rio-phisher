#!/bin/bash
echo "🚀 Auto-installing PhishingKit..."

# Detect platform
if [[ "$OSTYPE" == "linux-android"* ]]; then
    echo "📱 Termux detected"
    pkg update -y && pkg install python ngrok -y
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Linux detected"
    sudo apt update && sudo apt install python3 python3-pip ngrok -y 2>/dev/null || sudo yum install python3 python3-pip -y
else
    echo "💻 Downloading ngrok..."
    curl -s https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz | tar zxvf - ngrok && sudo mv ngrok /usr/local/bin/
fi

pip3 install -r requirements.txt
chmod +x run.sh
echo "✅ Ready! Run: ./run.sh  or  python3 server.py"