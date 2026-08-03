#!/usr/bin/env python3
"""
Weekly health check - runs automatically to verify system
"""

import os
import subprocess
from datetime import datetime

def log_message(msg):
    """Write to log"""
    with open("logs/health_check.log", "a") as f:
        f.write(f"{datetime.now()}: {msg}\n")
    print(msg)

def check_system():
    """Check system health"""
    log_message("="*50)
    log_message("HEALTH CHECK START")
    
    # Check number.txt
    try:
        with open("number.txt", "r") as f:
            number = int(f.read().strip())
            log_message(f"✅ number.txt: {number}")
    except:
        log_message("❌ number.txt missing or corrupt - recreating")
        with open("number.txt", "w") as f:
            f.write("0")
    
    # Check git
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if result.stdout:
        log_message(f"⚠️ Uncommitted changes found: {result.stdout}")
        subprocess.run(["python", "update_number.py"])
    else:
        log_message("✅ Git repository clean")
    
    # Check remote
    result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
    if "origin" not in result.stdout:
        log_message("⚠️ No remote configured - adding")
        subprocess.run(["git", "remote", "add", "origin", 
                       "https://github.com/pradhanashwarya2122/daily-notes.git"])
    else:
        log_message("✅ Remote configured")
    
    # Check last commit date
    result = subprocess.run(["git", "log", "-1", "--format=%cd"], 
                           capture_output=True, text=True)
    if result.stdout:
        log_message(f"✅ Last commit: {result.stdout.strip()}")
    
    log_message("HEALTH CHECK COMPLETE")
    log_message("="*50)

if __name__ == "__main__":
    check_system()