"""
NEO Online Judge - System Setup Script
=======================================
Chay script nay truoc khi khoi dong he thong lan dau:

    python setup_system.py

No se tu dong kiem tra va cai dat:
  1. Moi truong (Python, pip)
  2. Thu vien (pip install -r requirements.txt)
  3. Trinh bien dich (g++, gcc, java, node, fpc...)
  4. Tinh toan ven he thong
"""

import os
import sys
import subprocess
import platform
import shutil
import json
from pathlib import Path
from datetime import datetime

# Fix Unicode console output for emojis
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# ======================================================================
# Cau hinh
# ======================================================================

SYSTEM = platform.system().lower()
IS_WINDOWS = SYSTEM == "windows"
IS_LINUX = SYSTEM == "linux"
IS_MAC = SYSTEM == "darwin"

BASE_DIR = Path(__file__).resolve().parent.parent

# Them BASE_DIR vao sys.path de the import duoc cac module trong backend
sys.path.insert(0, str(BASE_DIR))
REQUIREMENTS_FILE = BASE_DIR / "requirements.txt"
ENV_FILE = BASE_DIR / ".env"
ENV_EXAMPLE_FILE = BASE_DIR / ".env.example"

# Danh sach compiler can cai dat
REQUIRED_COMPILERS = {
    "python": {
        "check_cmd": ["python3", "--version"] if not IS_WINDOWS else ["python", "--version"],
        "name": "Python 3",
        "required": True,
        "note": "Python 3.8+ la bat buoc",
    },
    "g++": {
        "check_cmd": ["g++", "--version"],
        "install_cmd": {
            "linux": "sudo apt-get install -y g++",
            "darwin": "brew install gcc",
            "windows": "winget install -e --id BrechtSanders.WinLibs.POSIX.UCRT --accept-package-agreements --accept-source-agreements",
        },
        "name": "C++ (GCC/G++)",
        "required": False,
        "note": "Can de cham bai C++",
    },
    "gcc": {
        "check_cmd": ["gcc", "--version"],
        "install_cmd": {
            "linux": "sudo apt-get install -y gcc",
            "darwin": "brew install gcc",
            "windows": "winget install -e --id BrechtSanders.WinLibs.POSIX.UCRT --accept-package-agreements --accept-source-agreements",
        },
        "name": "C (GCC)",
        "required": False,
        "note": "Can de cham bai C",
    },
    "java": {
        "check_cmd": ["java", "-version"],
        "install_cmd": {
            "linux": "sudo apt-get install -y default-jdk",
            "darwin": "brew install openjdk",
            "windows": "winget install -e --id EclipseAdoptium.Temurin.21.JDK --accept-package-agreements --accept-source-agreements",
        },
        "name": "Java (JDK)",
        "required": False,
        "note": "Can de cham bai Java",
    },
    "javac": {
        "check_cmd": ["javac", "-version"],
        "install_cmd": {
            "linux": "sudo apt-get install -y default-jdk",
            "darwin": "brew install openjdk",
            "windows": "winget install -e --id EclipseAdoptium.Temurin.21.JDK --accept-package-agreements --accept-source-agreements",
        },
        "name": "Java Compiler (javac)",
        "required": False,
        "note": "Can de cham bai Java",
    },
    "node": {
        "check_cmd": ["node", "--version"],
        "install_cmd": {
            "linux": "sudo apt-get install -y nodejs npm",
            "darwin": "brew install node",
            "windows": "winget install -e --id OpenJS.NodeJS --accept-package-agreements --accept-source-agreements",
        },
        "name": "Node.js (JavaScript)",
        "required": False,
        "note": "Can de cham bai JavaScript",
    },
    "fpc": {
        "check_cmd": ["fpc", "--version"] if not IS_WINDOWS else ["fpc", "-v"],
        "install_cmd": {
            "linux": "sudo apt-get install -y fp-compiler",
            "darwin": "brew install fpc",
            "windows": None,  # Windows can use fpc from https://www.freepascal.org/
        },
        "name": "Free Pascal (FPC)",
        "required": False,
        "note": "Can de cham bai Pascal",
    },
}

# ======================================================================
# Mau file .env
# ======================================================================

ENV_TEMPLATE = r"""# ==============================================================================
# NEO ONLINE JUDGE v2.0 - Cau hinh moi truong
# ==============================================================================
# Chep file nay thanh .env va dien cac thong tin can thiet
# ==============================================================================

# === Firebase (Bat buoc) ===
CRED_PATH=service-account.json
DB_URL=https://gtsv2-a93c5-default-rtdb.firebaseio.com

# === AI (DeepSeek - khuyen dung, re nhat) ===
# Dang ky key mien phi tai: https://platform.deepseek.com/
DEEPSEEK_API_KEY=sk-your-deepseek-api-key
DEEPSEEK_MODEL=deepseek-chat
AI_MODEL=deepseek-chat
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=1000
AI_TIMEOUT=20

# === AI (OpenAI - fallback) ===
# OPENAI_API_KEY=sk-your-openai-api-key

# === Judge Engine ===
JUDGE_TIMEOUT=3
POLL_INTERVAL=1.5

# === Server ===
HOST=0.0.0.0
PORT=5000

# === Logging ===
LOG_LEVEL=INFO
"""


# ======================================================================
# 1. ENV SETUP - Kiem tra moi truong Python
# ======================================================================

def print_header(title: str):
    """In tieu de phan."""
    print(f"\n--- {title} {'-' * (50 - len(title))}")

def print_status(ok: bool, msg: str):
    """In trang thai."""
    icon = "[OK]" if ok else "[FAIL]"
    print(f"  {icon} {msg}")


def check_python_version() -> bool:
    """Kiem tra Python >= 3.8."""
    v = sys.version_info
    ok = v.major >= 3 and v.minor >= 8
    print_status(ok, f"Python {v.major}.{v.minor}.{v.micro} (can >= 3.8)")
    return ok


def check_pip() -> bool:
    """Kiem tra pip da duoc cai chua."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True, text=True, timeout=10
        )
        ok = result.returncode == 0
        version = result.stdout.strip().split("\n")[0] if ok else ""
        print_status(ok, f"pip: {version}" if version else "pip: khong tim thay")
        return ok
    except Exception:
        print_status(False, "pip: khong the kiem tra")
        return False


def install_pip() -> bool:
    """Tu dong cai dat pip neu chua co."""
    print("  > Dang cai dat pip...")
    try:
        # Tai get-pip.py
        import urllib.request
        url = "https://bootstrap.pypa.io/get-pip.py"
        urllib.request.urlretrieve(url, "get-pip.py")
        
        result = subprocess.run(
            [sys.executable, "get-pip.py"],
            capture_output=True, text=True, timeout=60
        )
        os.remove("get-pip.py") if os.path.exists("get-pip.py") else None
        return result.returncode == 0
    except Exception as e:
        print(f"     LOI: {e}")
        return False


def setup_env() -> bool:
    """Kiem tra va cai dat moi truong Python."""
    print_header("1. MOI TRUONG (ENVIRONMENT)")
    
    all_ok = True
    
    # Kiem tra Python
    if not check_python_version():
        print("  > Vui long cai dat Python 3.8+ tu: https://www.python.org/downloads/")
        return False
    
    # Kiem tra pip
    if not check_pip():
        print("  > pip chua duoc cai dat. Dang cai tu dong...")
        if not install_pip():
            print("  > LOI: Khong the cai dat pip. Hay cai bang tay: python -m ensurepip")
            all_ok = False
    
    # Kiem tra file .env
    if not ENV_FILE.exists():
        print("  > File .env chua ton tai. Dang tao tu .env.example...")
        if ENV_EXAMPLE_FILE.exists():
            import shutil
            shutil.copy(ENV_EXAMPLE_FILE, ENV_FILE)
            print("  > Da tao .env tu .env.example. Vui long dien thong tin!")
        else:
            with open(ENV_FILE, "w", encoding="utf-8") as f:
                f.write(ENV_TEMPLATE)
            print("  > Da tao file .env mac dinh. Vui long dien thong tin Firebase + AI key!")
        all_ok = False
    else:
        print_status(True, "File .env da ton tai")
    
    # Kiem tra service-account.json (neu co CRED_PATH)
    if ENV_FILE.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(ENV_FILE)
            cred_path = os.getenv("CRED_PATH", "service-account.json")
            if cred_path and not os.path.exists(cred_path):
                print_status(False, f"File {cred_path} khong tim thay! Can file service key cua Firebase.")
                print("     Xem huong dan tai: https://firebase.google.com/docs/admin/setup")
                all_ok = False
            else:
                print_status(True, f"File {cred_path} da tim thay")
        except ImportError:
            print("  > (bo qua kiem tra Firebase - can cai thu vien truoc)")
    
    return all_ok


# ======================================================================
# 2. DEPENDENCIES SETUP - Cai dat thu vien Python
# ======================================================================

def setup_dependencies() -> bool:
    """Cai dat cac thu vien Python tu requirements.txt."""
    print_header("2. THU VIEN (DEPENDENCIES)")
    
    if not REQUIREMENTS_FILE.exists():
        print_status(False, f"Khong tim thay {REQUIREMENTS_FILE}")
        return False
    
    try:
        print(f"  > Dang cai dat thu vien tu {REQUIREMENTS_FILE.name}...")
        print(f"     (co the mat 1-3 phut tuy toc do mang)")
        
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
            capture_output=True, text=True, timeout=300
        )
        
        if result.returncode == 0:
            print_status(True, "Da cai dat tat ca thu vien thanh cong!")
            
            # Dem so luong packages da cai
            lines = [l for l in result.stdout.split("\n") 
                     if l.strip() and "already satisfied" not in l and
                     "Requirement already" not in l]
            print(f"     Packages da cai: {len([l for l in lines if 'Successfully' in l or 'Installed' in l or l.strip().startswith('-')])}")
            return True
        else:
            print_status(False, f"Loi khi cai dat thu vien:")
            # In ra loi (toi da 10 dong)
            errors = [l for l in result.stderr.split("\n") if l.strip()][:10]
            for e in errors:
                print(f"     {e}")
            
            # Thu cai tung goi rieng le
            print("\n  > Thu cai tung goi rieng le...")
            return install_dependencies_individually()
    
    except subprocess.TimeoutExpired:
        print_status(False, "Timeout khi cai dat thu vien (qua 5 phut)")
        return False
    except Exception as e:
        print_status(False, f"Loi: {e}")
        return False


def install_dependencies_individually() -> bool:
    """Cai tung goi mot neu cai hang loat bi loi."""
    all_ok = True
    
    with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as f:
        packages = [l.strip() for l in f 
                    if l.strip() and not l.startswith("#") and not l.startswith("-")]
    
    for pkg in packages:
        # Bo qua dong huong dan
        if pkg.startswith("git+") or "://" in pkg:
            continue
        
        # Lay ten package (bo qua version)
        pkg_name = pkg.split(">=")[0].split("==")[0].strip()
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", pkg],
                capture_output=True, text=True, timeout=120
            )
            ok = result.returncode == 0
            print_status(ok, f"{pkg_name}")
            if not ok:
                all_ok = False
        except Exception:
            print_status(False, f"{pkg_name} (loi)")
            all_ok = False
    
    return all_ok


# ======================================================================
# 3. COMPILER SETUP - Kiem tra va cai dat trinh bien dich
# ======================================================================

def check_compiler(name: str, config: dict) -> dict:
    """Kiem tra mot compiler da duoc cai dat chua."""
    result = {"name": name, "installed": False, "version": "", "config": config}
    
    try:
        check = subprocess.run(
            config["check_cmd"],
            capture_output=True, text=True, timeout=10,
        )
        if check.returncode == 0:
            result["installed"] = True
            result["version"] = check.stdout.strip().split("\n")[0] or \
                                check.stderr.strip().split("\n")[0]
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        result["installed"] = False
    
    return result


def install_compiler(name: str, config: dict) -> bool:
    """Cai dat mot compiler."""
    install_cmd = config.get("install_cmd", {}).get(SYSTEM)
    
    if not install_cmd:
        print(f"     (khong co huong dan cai dat cho {SYSTEM})")
        return False
    
    print(f"  > Chay: {install_cmd}")
    
    # Cho phep in output truc tiep ra man hinh de nguoi dung thay tien trinh
    try:
        result = subprocess.run(
            install_cmd,
            shell=True,
            timeout=600
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("     LOI: Qua thoi gian cai dat (10 phut)")
        return False
    except Exception as e:
        print(f"     LOI: {e}")
        return False


def setup_compilers() -> bool:
    """Kiem tra va cai dat cac trinh bien dich."""
    print_header("3. TRINH BIEN DICH (COMPILERS)")
    
    results = []
    
    for name, config in REQUIRED_COMPILERS.items():
        info = check_compiler(name, config)
        results.append(info)
        
        if info["installed"]:
            version = info["version"][:60] if info["version"] else "(da cai)"
            print_status(True, f"{config['name']}: {version}")
        else:
            print_status(False, f"{config['name']}: chua cai dat")
            
            if config["required"]:
                print(f"     > {config['name']} LA BAT BUOC!")
            
            if config.get("install_cmd", {}).get(SYSTEM):
                # Tu dong cai dat (khong hoi)
                print(f"     > Dang cai dat tu dong...")
                ok = install_compiler(name, config)
                if ok:
                    print_status(True, f"{config['name']}: da cai dat")
                else:
                    print(f"     > Bo qua. Co the cai bang tay sau.")
            else:
                extra = config.get("note", "")
                if extra:
                    print(f"     > {extra}")
    
    # Tong ket
    installed = sum(1 for r in results if r["installed"])
    total = len(results)
    print()
    print(f"  Trang thai: {installed}/{total} compiler da duoc cai dat")
    
    return installed >= 1  # Chi can it nhat Python la duoc


# ======================================================================
# 4. INTEGRITY CHECK - Kiem tra tinh toan ven he thong
# ======================================================================

def check_firebase_connection() -> bool:
    """Kiem tra ket noi Firebase."""
    try:
        from backend.config.settings import settings
        if not settings.DB_URL:
            print_status(False, "Thieu DB_URL trong .env")
            return False
        
        import firebase_admin
        from firebase_admin import credentials, db
        
        cred_path = settings.CRED_PATH
        if not os.path.exists(cred_path):
            print_status(False, f"Khong tim thay {cred_path}")
            return False
        
        # Thu ket noi
        cred = credentials.Certificate(cred_path)
        try:
            app = firebase_admin.get_app()
        except ValueError:
            app = firebase_admin.initialize_app(cred, {"databaseURL": settings.DB_URL})
        
        # Thu doc du lieu
        ref = db.reference("/")
        ref.get()  # Chi can khong loi la duoc
        print_status(True, "Ket noi Firebase thanh cong!")
        
        # Kiem tra problems
        prob_ref = db.reference("problems")
        prob_data = prob_ref.get()
        if prob_data:
            count = len(prob_data)
            print(f"     So bai tap: {count}")
        else:
            print("     (Chua co bai tap nao, chay import_problems.py de them)")
        
        return True
    except Exception as e:
        print_status(False, f"Firebase: {e}")
        return False


def check_judge_engine() -> bool:
    """Kiem tra judge engine co the chay duoc khong."""
    try:
        from backend.core.compiler import Compiler
        
        # Kiem tra Python
        cmd, err = Compiler.compile("python", "test_judge", 'print("hello")')
        if err:
            print_status(False, f"Judge Engine: {err}")
            return False
        
        # Chay thu
        from backend.core.judge import JudgeEngine
        result = JudgeEngine.grade_all(
            cmd,
            [{"input": "", "output": "hello"}, {"input": "", "output": "hello"}],
            timeout=3
        )
        
        ok = result["passed"] == 2
        print_status(ok, f"Judge Engine: {result['passed']}/{result['total']} test passed")
        
        # Don dep
        Compiler.cleanup("test_judge")
        
        return ok
    except Exception as e:
        print_status(False, f"Judge Engine: {e}")
        return False


def check_module_imports() -> bool:
    """Kiem tra cac module co the import duoc khong."""
    modules = [
        ("firebase_admin", "firebase-admin"),
        ("requests", "requests"),
        ("flask", "flask"),
        ("flask_cors", "flask-cors"),
        ("jwt", "pyjwt"),
        ("dotenv", "python-dotenv"),
    ]
    
    all_ok = True
    for mod_name, pkg_name in modules:
        try:
            __import__(mod_name)
            print_status(True, f"{pkg_name}")
        except ImportError:
            print_status(False, f"{pkg_name} (chua cai)")
            all_ok = False
    
    return all_ok


def integrity_check() -> bool:
    """Chay kiem tra tinh toan ven he thong."""
    print_header("4. KIEM TRA TINH TOAN VEN (INTEGRITY)")
    
    checks = []
    
    # Kiem tra cau truc thu muc
    required_dirs = ["backend", "backend/core", "backend/services", "backend/config", "frontend"]
    for d in required_dirs:
        ok = os.path.isdir(BASE_DIR / d)
        print_status(ok, f"Thu muc {d}/")
        checks.append(ok)
    
    # Kiem tra cac file quan trong
    required_files = [
        "backend/judge.py", "requirements.txt", ".env",
        "backend/config/settings.py", "backend/config/logging.py",
        "backend/app.py",
        "backend/core/compiler.py", "backend/core/judge.py",
        "backend/services/firebase_service.py",
        "backend/services/ai_service.py",
    ]
    for f in required_files:
        ok = (BASE_DIR / f).exists()
        print_status(ok, f"File {f}")
        checks.append(ok)
    
    # Kiem tra imports
    print()
    print("  Kiem tra thu vien Python:")
    mod_ok = check_module_imports()
    checks.append(mod_ok)
    
    # Kiem tra judge engine
    print()
    print("  Kiem tra Judge Engine:")
    judge_ok = check_judge_engine()
    checks.append(judge_ok)
    
    # Kiem tra Firebase
    print()
    print("  Kiem tra Firebase:")
    fb_ok = check_firebase_connection()
    checks.append(fb_ok)
    
    all_ok = all(checks)
    
    print()
    if all_ok:
        print("  [+] TAT CA CAC KIEM TRA DEU DAT!")
        print(f"     {sum(checks)}/{len(checks)} thanh cong")
    else:
        print(f"  [!] {sum(checks)}/{len(checks)} thanh cong")
        print("     Kiem tra phan loi ben tren de biet chi tiet")
    
    return all_ok


# ======================================================================
# MAIN - Chay setup
# ======================================================================

def print_banner():
    """In banner khi chay script."""
    print("""
    ============================================
      NEO ONLINE JUDGE v2.0 - HE THONG SETUP
    ============================================
      Trinh tu:
        1. Moi truong (Python, pip, .env)
        2. Thu vien (pip install)
        3. Trinh bien dich (g++, java, node...)
        4. Kiem tra tinh toan ven
    ============================================
    """)


def write_report(results: dict):
    """Ghi bao cao ra file log."""
    report_path = BASE_DIR / "logs" / f"setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    os.makedirs(report_path.parent, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("NEO ONLINE JUDGE - Setup Report\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"System: {platform.system()} {platform.release()}\n")
        f.write(f"Python: {sys.version}\n")
        f.write("=" * 50 + "\n\n")
        
        for section, data in results.items():
            f.write(f"\n## {section.upper()}\n")
            ok_str = "OK" if data['ok'] else "FAILED"
            f.write(f"   Status: {ok_str}\n")
            if 'details' in data:
                for d in data['details']:
                    f.write(f"   - {d}\n")
        
        total_ok = sum(1 for v in results.values() if v['ok'])
        f.write(f"\n{'=' * 50}\n")
        f.write(f"Tong ket: {total_ok}/{len(results)} phan thanh cong\n")
    
    return report_path


def main():
    """Main function - chay toan bo qua trinh setup."""
    print_banner()
    
    print(f"  He dieu hanh: {platform.system()} {platform.release()}")
    print(f"  Python:       {sys.version.split()[0]}")
    print(f"  Thu muc:      {BASE_DIR}")
    print()
    
    results = {}
    all_ok = True
    
    # Buoc 1: Moi truong
    env_ok = setup_env()
    results["env"] = {"ok": env_ok, "details": []}
    if not env_ok:
        all_ok = False
    
    # Buoc 2: Thu vien
    deps_ok = setup_dependencies()
    results["dependencies"] = {"ok": deps_ok, "details": []}
    if not deps_ok:
        all_ok = False
    
    # Buoc 3: Trinh bien dich
    compilers_ok = setup_compilers()
    results["compilers"] = {"ok": compilers_ok, "details": []}
    if not compilers_ok:
        all_ok = False
    
    # Buoc 4: Kiem tra tinh toan ven
    integrity_ok = integrity_check()
    results["integrity"] = {"ok": integrity_ok, "details": []}
    if not integrity_ok:
        all_ok = False
    
    # Tong ket
    print()
    print("=" * 60)
    if all_ok:
        print("  [OK] HE THONG DA SAN SANG!")
        print()
        print("  Chay:  python backend/judge.py")
        print("  Web:   https://gtsv2-a93c5.web.app")
        print("  API:   http://localhost:5000/api/health")
    else:
        print("  [WARN] CAN XU LY MOT SO VAN DE TREN")
        print()
        print("  Vui long kiem tra cac muc FAILED va chay lai:")
        print("  python setup/setup_system.py")
    
    print("=" * 60)
    
    # Ghi bao cao
    report = write_report(results)
    print(f"\n  Bao cao chi tiet: {report}")
    
    return all_ok


if __name__ == "__main__":
    main()
