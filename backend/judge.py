#!/usr/bin/env python3
# ==============================================================================
# NEO ONLINE JUDGE v2.0
# Entry point - khoi dong ung dung cham bai + API server + Auth
# ==============================================================================
#
# Usage:  python judge.py
#         python -m backend.app
#
# Tinh nang: Cham bai tu dong, AI Mentor, Auth (Email/Google/GitHub/Facebook)
# ==============================================================================

import sys
import os

# Add project root to sys.path so that absolute imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Fix Unicode console output
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from backend.app import main

if __name__ == "__main__":
    main()
