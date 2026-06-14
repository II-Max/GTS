"""
NEO Online Judge - Import Problems Script
Doc file problems_data.json va day toan bo bai tap len Firebase Realtime Database.
"""

# Fix encoding UTF-8 cho Windows (tranh loi cp1252 khi xu ly tieng Viet)
import os
os.environ['PYTHONUTF8'] = '1'

import json
import sys

# Them thu muc goc vao PATH de import duoc config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
import firebase_admin
from firebase_admin import credentials, db


def main():
    """Main import function."""
    print("=" * 60)
    print("  NEO ONLINE JUDGE - Import Problems Tool")
    print("=" * 60)

    # === Kiem tra file service-account.json ===
    cred_path = settings.CRED_PATH
    if not os.path.exists(cred_path):
        print(f"\n[LOI] Khong tim thay file: {cred_path}")
        print("       Vui long dat file service-account.json vao thu muc goc.")
        print("       Hoac cau hinh CRED_PATH trong .env")
        sys.exit(1)

    # === Kiem tra DB_URL ===
    if not settings.DB_URL:
        print("\n[LOI] Thieu DB_URL trong .env")
        print("       Them dong: DB_URL=https://gtsv2-a93c5-default-rtdb.firebaseio.com")
        sys.exit(1)

    # === Ket noi Firebase ===
    print(f"\n[*] Dang ket noi Firebase...")
    print(f"    Project: {settings.DB_URL}")

    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {"databaseURL": settings.DB_URL})
        print("    [OK] Da ket noi thanh cong!\n")
    except Exception as e:
        print(f"    [LOI] Khong the ket noi Firebase: {e}")
        sys.exit(1)

    # === Doc file problems_data.json ===
    json_path = os.path.join(os.path.dirname(__file__), "problems_data.json")
    if not os.path.exists(json_path):
        print(f"[LOI] Khong tim thay file: {json_path}")
        sys.exit(1)

    print(f"[*] Dang doc file: {json_path}")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            problems = json.load(f)
    except Exception as e:
        print(f"[LOI] Doc file JSON that bai: {e}")
        sys.exit(1)

    print(f"    [OK] Tim thay {len(problems)} bai tap!\n")

    # === Import tung bai ===
    success = 0
    failed = 0

    for problem in problems:
        problem_id = problem.get("id", "").strip()
        title = problem.get("title", "")

        if not problem_id:
            print(f"    [SKIP] Bai tap thieu 'id', bo qua...")
            failed += 1
            continue

        # Chuan bi du lieu cho Firebase
        firebase_data = {
            "title": problem.get("title", ""),
            "description": problem.get("description", ""),
            "level": problem.get("level", "Easy"),
            "difficulty": problem.get("difficulty", problem.get("level", "Easy")),
            "example_input": problem.get("example_input", ""),
            "example_output": problem.get("example_output", ""),
            "tutorial_vid": problem.get("tutorial_vid", ""),
            "testcases": problem.get("testcases", problem.get("test_cases", [])),
        }

        # Ghi len Firebase
        try:
            ref = db.reference(f"problems/{problem_id}")
            ref.set(firebase_data)
            print(f"    [OK] Da import: {problem_id} - {title}")
            success += 1
        except Exception as e:
            print(f"    [LOI] Import {problem_id} that bai: {e}")
            failed += 1

    # === Ket qua ===
    print("\n" + "=" * 60)
    print(f"  KET QUA IMPORT:")
    print(f"  - Thanh cong: {success} bai")
    print(f"  - That bai:   {failed} bai")
    print(f"  - Tong cong:  {len(problems)} bai")
    print("=" * 60)

    if success > 0:
        print("\n  >> Truy cap Firebase Console de kiem tra:")
        print(f"     {settings.DB_URL}")
        print("\n  >> Hoac vao Kho bai tap tren web de xem!")

    return success > 0


if __name__ == "__main__":
    main()
