#!/usr/bin/env python3
# scripts/db_migrate.py
"""
scripts/db_migrate.py
Initializes DB schema for CyberSathi.
This script imports the db_service.init_db function from backend.app.services.
Run from repo root: python3 scripts/db_migrate.py
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

try:
    from backend.app.services.db_service import init_db
except Exception as e:
    print("❌ Failed to import init_db from backend.app.services.db_service:", e)
    print("Make sure you're running this from the repo root and Pythonpath is correct.")
    raise

def main():
    print("🔧 Initializing database (creating tables)...")
    init_db()
    print("✅ Database init complete.")

if __name__ == "__main__":
    main()
