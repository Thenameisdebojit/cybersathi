#!/usr/bin/env python3
# scripts/universal_launcher.py
"""
Cross-platform launcher for CyberSathi local stack.
Detects OS and runs the correct start script.
Usage: python3 scripts/universal_launcher.py [start|stop|demo|migrate]
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

def run_cmd(cmd, shell=False):
    print("Running:", cmd)
    subprocess.run(cmd, shell=shell, check=True)

def start():
    if platform.system() == "Windows":
        run_cmd([str(SCRIPTS_DIR / "start_local.bat")], shell=True)
    else:
        run_cmd(["bash", str(SCRIPTS_DIR / "start_local.sh")])

def stop():
    if platform.system() == "Windows":
        run_cmd([str(SCRIPTS_DIR / "stop_services.bat")], shell=True)
    else:
        run_cmd(["bash", str(SCRIPTS_DIR / "stop_services.sh")])

def migrate():
    run_cmd([sys.executable, str(SCRIPTS_DIR / "db_migrate.py")])

def demo():
    if platform.system() == "Windows":
        run_cmd([str(SCRIPTS_DIR / "demo.bat")], shell=True)
    else:
        run_cmd(["bash", str(SCRIPTS_DIR / "demo.sh")])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: universal_launcher.py [start|stop|demo|migrate]")
        sys.exit(1)
    cmd = sys.argv[1].lower()
    if cmd == "start":
        start()
    elif cmd == "stop":
        stop()
    elif cmd == "demo":
        demo()
    elif cmd == "migrate":
        migrate()
    else:
        print("Unknown command:", cmd)
        sys.exit(2)
