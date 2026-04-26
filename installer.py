#!/usr/bin/env python3
"""
1-Click installer for rio-phisher
"""
import os, sys, subprocess

print("🔧 rio-phisher installer...")

# Platform fixes
if os.name == 'nt':  # Windows
    subprocess.run("python -m pip install --upgrade pip", shell=True, capture_output=True)
elif 'ANDROID_ROOT' in os.environ:
    subprocess.run("pkg update && pkg upgrade -y", shell=True, capture_output=True)

print("✅ Ready! Run: python run.py")
