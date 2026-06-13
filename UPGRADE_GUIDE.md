# ?? UPGRADE GUIDE - NEO ONLINE JUDGE

Hý?ng d?n chi ti?t ð? nâng c?p NEO ONLINE JUDGE theo các giai ðo?n.

---

## ?? M?c L?c

1. [Tier 1: B?o V? API Keys](#tier-1-b?o-v?-api-keys)
2. [Tier 2: Logging & Error Handling](#tier-2-logging--error-handling)
3. [Tier 3: Authentication](#tier-3-authentication)
4. [Tier 4: Multi-Language Support](#tier-4-multi-language-support)
5. [Tier 5: Docker & Containerization](#tier-5-docker--containerization)
6. [Tier 6: Frontend Modernization](#tier-6-frontend-modernization)

---

## Tier 1: B?o V? API Keys

### ?? Th?i Gian: 30-45 phút
### ?? Ð? Khó: ? (D?)

### Bý?c 1: Cài Ð?t python-dotenv

```bash
pip install python-dotenv
pip freeze > requirements.txt
```

### Bý?c 2: T?o File .env

T?o file `.env` ? thý m?c g?c:

```env
CRED_PATH=./service-account.json
DB_URL=https://neo-online-judge-default-rtdb.firebaseio.com
OPENAI_API_KEY=sk-your-actual-key-here
MODEL=gpt-4o-mini
JUDGE_TIMEOUT=3
```

### Bý?c 3: C?p Nh?t judge.py

```python
# Thêm vào ð?u file
import os
from dotenv import load_dotenv

load_dotenv()

# Thay th? hardcoded values
CRED_PATH = os.getenv('CRED_PATH', 'service-account.json')
DB_URL = os.getenv('DB_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CURRENT_MODEL = os.getenv('MODEL', 'gpt-4o-mini')
JUDGE_TIMEOUT = int(os.getenv('JUDGE_TIMEOUT', '3'))
```

### Bý?c 4: C?p Nh?t .gitignore

```
.env
.env.local
service-account.json
__pycache__/
*.pyc
```

### ? Verification

```bash
# Test configuration loading
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('OPENAI_API_KEY')[:10])"
```

---

## Tier 2: Logging & Error Handling

### ?? Th?i Gian: 1-1.5 gi?
### ?? Ð? Khó: ?? (Trung B?nh)

### Bý?c 1: Cài Ð?t Logging

```bash
pip install python-json-logger
```

### Bý?c 2: T?o File config/logging_config.py

```python
# config/logging_config.py
import logging
import logging.config
import os
from datetime import datetime

# T?o thý m?c logs n?u chýa có
os.makedirs('logs', exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'json',
            'filename': f'logs/judge_{datetime.now().strftime("%Y%m%d")}.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'standard',
            'filename': f'logs/errors_{datetime.now().strftime("%Y%m%d")}.log',
            'maxBytes': 10485760,
            'backupCount': 5
        }
    },
    'loggers': {
        'judge': {
            'level': 'DEBUG',
            'handlers': ['console', 'file', 'error_file'],
            'propagate': False
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger('judge')
```

### Bý?c 3: C?p Nh?t judge.py

```python
# Thêm vào ð?u file sau imports
from config.logging_config import setup_logging

logger = setup_logging()

# Thay th? print b?ng logger
# Thay v?: print(">> [SYSTEM] Ðang kh?i ð?ng...")
# Dùng: logger.info("Ðang kh?i ð?ng NEO JUDGE CORE")

# Enhanced error handling
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(CRED_PATH)
        firebase_admin.initialize_app(cred, {'databaseURL': DB_URL})
    logger.info("K?t n?i Firebase thành công.")
except FileNotFoundError as e:
    logger.error(f"File {CRED_PATH} không t?m th?y", exc_info=True)
    sys.exit(1)
except Exception as e:
    logger.error(f"L?i kh?i t?o Firebase: {e}", exc_info=True)
    sys.exit(1)
```

### Bý?c 4: C?p Nh?t Các Hàm Khác

```python
def execute_and_grade(run_cmd, input_data, expected_output):
    """Ch?y code và so sánh k?t qu?"""
    try:
        if input_data is None: 
            input_data = ""

        logger.debug(f"Ch?y l?nh: {' '.join(run_cmd)}")

        process = subprocess.run(
            run_cmd,
            input=str(input_data),
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=JUDGE_TIMEOUT
        )

        actual = process.stdout.strip()
        expected = str(expected_output).strip()

        if process.stderr:
            logger.warning(f"Runtime error: {process.stderr}")
            return 0, f"Runtime Error: {process.stderr}"

        if actual == expected:
            logger.debug("Test passed")
            return 100, "Chính xác tuy?t ð?i!"
        else:
            logger.debug(f"Test failed. Expected: {expected}, Got: {actual}")
            return 0, f"Sai k?t qu?.\nOutput: {actual}\nÐáp án: {expected}"

    except subprocess.TimeoutExpired:
        logger.warning("Code execution timeout")
        return 0, "Time Limit Exceeded"
    except Exception as e:
        logger.error(f"Error during grading: {e}", exc_info=True)
        return 0, f"L?i h? th?ng: {str(e)}"
```

### ? Verification

```bash
# Ch?y judge và ki?m tra logs
python judge.py

# Xem log files
ls -la logs/
cat logs/judge_*.log
```

---

## Tier 3: Authentication

### ?? Th?i Gian: 1.5-2 gi?
### ?? Ð? Khó: ??? (Trung B?nh-Khó)

### Bý?c 1: C?p Nh?t Firebase Rules

```json
{
  "rules": {
    "users": {
      "$uid": {
        ".read": "$uid === auth.uid",
        ".write": "$uid === auth.uid"
      }
    },
    "submissions": {
      "$submission_id": {
        ".read": "auth != null",
        ".write": "auth != null && root.child('users').child(auth.uid).exists()"
      }
    },
    "problems": {
      ".read": "auth != null",
      "$problem_id": {
        ".write": "root.child('users').child(auth.uid).child('role').val() === 'admin'"
      }
    },
    "ai_requests": {
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}
```

### Bý?c 2: T?o auth_manager.py

```python
# auth_manager.py
import firebase_admin
from firebase_admin import auth
import logging

logger = logging.getLogger(__name__)

class AuthManager:
    """Qu?n l? xác th?c ngý?i dùng"""

    @staticmethod
    def verify_token(token):
        """Xác minh token t? client"""
        try:
            decoded = auth.verify_id_token(token)
            return decoded
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return None

    @staticmethod
    def get_user_role(uid):
        """L?y vai tr? c?a ngý?i dùng"""
        try:
            user_record = auth.get_user(uid)
            # L?y claims (roles)
            return user_record.custom_claims or {}
        except Exception as e:
            logger.error(f"Error getting user role: {e}")
            return None

    @staticmethod
    def is_admin(uid):
        """Ki?m tra xem ngý?i dùng có ph?i admin không"""
        try:
            user_record = auth.get_user(uid)
            return user_record.custom_claims.get('admin', False) if user_record.custom_claims else False
        except Exception as e:
            logger.error(f"Error checking admin status: {e}")
            return False
```

### Bý?c 3: Tích H?p vào judge.py

```python
from auth_manager import AuthManager

def process_submission_queue(table_name):
    """Process submissions with authentication"""
    data_dict = db.reference(table_name).get()

    if not data_dict:
        return

    for key, val in data_dict.items():
        if isinstance(val, dict) and val.get('status') == 'pending':
            # Verify user exists
            user_id = val.get('user_id')
            if not user_id:
                logger.warning(f"Submission {key} missing user_id")
                continue

            try:
                user_record = auth.get_user(user_id)
                logger.info(f"Processing submission for {user_record.email}")
            except Exception as e:
                logger.error(f"Invalid user_id {user_id}: {e}")
                continue

            # Process submission...
            lang = val.get('language')
            code = val.get('code')
            prob_id = val.get('problem_id')

            # ... rest of processing
```

### ? Verification

```bash
# Test authentication
python -c "
from firebase_admin import auth, initialize_app, credentials
import os
from dotenv import load_dotenv

load_dotenv()
cred = credentials.Certificate(os.getenv('CRED_PATH'))
app = initialize_app(cred)

# Create test user
try:
    user = auth.create_user(
        email='test@example.com',
        password='Test123456'
    )
    print(f'Created user: {user.uid}')
    auth.delete_user(user.uid)
    print('Test passed!')
except Exception as e:
    print(f'Error: {e}')
"
```

---

## Tier 4: Multi-Language Support

### ?? Th?i Gian: 2-3 gi?
### ?? Ð? Khó: ???? (Khó)

### Bý?c 1: T?o compiler_manager.py

```python
# compiler_manager.py
import subprocess
import os
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class CompilerManager:
    """Qu?n l? biên d?ch cho các ngôn ng? khác nhau"""

    TIMEOUT = 10

    @staticmethod
    def compile_python(filename: str, code: str) -> Tuple[Optional[list], Optional[str]]:
        """Python: ch?y tr?c ti?p"""
        try:
            with open(f"{filename}.py", "w", encoding="utf-8") as f:
                f.write(code)
            return [os.sys.executable, f"{filename}.py"], None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def compile_cpp(filename: str, code: str) -> Tuple[Optional[list], Optional[str]]:
        """C++: biên d?ch v?i g++"""
        try:
            with open(f"{filename}.cpp", "w", encoding="utf-8") as f:
                f.write(code)

            result = subprocess.run(
                ["g++", f"{filename}.cpp", "-o", f"{filename}.exe", "-std=c++17"],
                capture_output=True,
                text=True,
                timeout=CompilerManager.TIMEOUT
            )

            if result.returncode != 0:
                return None, result.stderr
            return [f"{filename}.exe"], None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def compile_c(filename: str, code: str) -> Tuple[Optional[list], Optional[str]]:
        """C: biên d?ch v?i gcc"""
        try:
            with open(f"{filename}.c", "w", encoding="utf-8") as f:
                f.write(code)

            result = subprocess.run(
                ["gcc", f"{filename}.c", "-o", f"{filename}.exe", "-std=c11"],
                capture_output=True,
                text=True,
                timeout=CompilerManager.TIMEOUT
            )

            if result.returncode != 0:
                return None, result.stderr
            return [f"{filename}.exe"], None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def compile_java(filename: str, code: str) -> Tuple[Optional[list], Optional[str]]:
        """Java: biên d?ch v?i javac"""
        try:
            # Extract class name from code
            import re
            match = re.search(r'public\s+class\s+(\w+)', code)
            class_name = match.group(1) if match else filename

            with open(f"{class_name}.java", "w", encoding="utf-8") as f:
                f.write(code)

            result = subprocess.run(
                ["javac", f"{class_name}.java"],
                capture_output=True,
                text=True,
                timeout=CompilerManager.TIMEOUT
            )

            if result.returncode != 0:
                return None, result.stderr
            return ["java", "-cp", ".", class_name], None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def compile_javascript(filename: str, code: str) -> Tuple[Optional[list], Optional[str]]:
        """JavaScript: ch?y v?i Node.js"""
        try:
            with open(f"{filename}.js", "w", encoding="utf-8") as f:
                f.write(code)
            return ["node", f"{filename}.js"], None
        except Exception as e:
            return None, str(e)

    @classmethod
    def compile(cls, lang: str, filename: str, code: str) -> Tuple[Optional[list], Optional[str]]:
        """Compile code based on language"""
        compilers = {
            'python': cls.compile_python,
            'cpp': cls.compile_cpp,
            'c': cls.compile_c,
            'java': cls.compile_java,
            'javascript': cls.compile_javascript,
        }

        if lang not in compilers:
            return None, f"Ngôn ng? '{lang}' chýa ðý?c h? tr?"

        return compilers[lang](filename, code)
```

### Bý?c 2: C?p Nh?t judge.py

```python
from compiler_manager import CompilerManager

def compile_code(lang, filename, code):
    """Wrapper function using new CompilerManager"""
    return CompilerManager.compile(lang, filename, code)
```

### ? Verification

```bash
# Test multi-language compilation
python -c "
from compiler_manager import CompilerManager

# Test Python
cmd, err = CompilerManager.compile('python', 'test', 'print(5)')
print(f'Python: {\"OK\" if not err else err}')

# Test C++
cpp_code = '#include <iostream>\nint main() { std::cout << 5; return 0; }'
cmd, err = CompilerManager.compile('cpp', 'test', cpp_code)
print(f'C++: {\"OK\" if not err else err}')
"
```

---

## Tier 5: Docker & Containerization

### ?? Th?i Gian: 1.5-2 gi?
### ?? Ð? Khó: ??? (Trung B?nh-Khó)

### Bý?c 1: Ð? Có S?n Dockerfile

File `Dockerfile` ð? ðý?c t?o. Ð? build:

```bash
docker build -t neo-judge:latest .
```

### Bý?c 2: Setup Docker Compose

File `docker-compose.yml` ð? ðý?c t?o. Ð? ch?y:

```bash
# Copy .env.example thành .env
cp .env.example .env

# C?p nh?t .env v?i credentials th?c t?
nano .env

# Ch?y services
docker-compose up -d

# Xem logs
docker-compose logs -f judge

# D?ng services
docker-compose down
```

### Bý?c 3: GitHub Actions CI/CD

T?o `.github/workflows/ci.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

    - name: Run tests
      run: |
        pip install pytest pytest-cov
        pytest tests/ --cov=. --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Build Docker image
      run: docker build -t neo-judge:latest .

    - name: Push to registry
      # C?n setup Docker credentials
      run: |
        # echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        # docker push neo-judge:latest
        echo "Docker push would happen here"
```

### ? Verification

```bash
# Test Docker build
docker build -t neo-judge:test .

# Test container
docker run --rm neo-judge:test python -c "import sys; print(sys.version)"

# Test with docker-compose
docker-compose up --abort-on-container-exit
```

---

## Tier 6: Frontend Modernization

### ?? Th?i Gian: 8-10 gi?
### ?? Ð? Khó: ????? (R?t Khó)

### Bý?c 1: Cài Ð?t React

```bash
# Cài Node.js trý?c (https://nodejs.org)

# T?o React app
npm create vite@latest neo-judge-frontend -- --template react
cd neo-judge-frontend

# Cài dependencies
npm install
npm install firebase monaco-editor axios zustand
```

### Bý?c 2: T?o Structure

```
neo-judge-frontend/
??? src/
?   ??? components/
?   ?   ??? Editor.jsx          # Code editor
?   ?   ??? ProblemList.jsx     # Problems list
?   ?   ??? ResultPanel.jsx     # Results display
?   ?   ??? Navbar.jsx          # Navigation
?   ??? pages/
?   ?   ??? Home.jsx
?   ?   ??? Problems.jsx
?   ?   ??? Contests.jsx
?   ?   ??? Dashboard.jsx
?   ??? services/
?   ?   ??? firebase.js         # Firebase config
?   ?   ??? api.js              # API calls
?   ??? store/
?   ?   ??? useStore.js         # Zustand store
?   ??? App.jsx
?   ??? main.jsx
??? package.json
```

### Bý?c 3: Editor Component

```jsx
// src/components/Editor.jsx
import React from 'react';
import Editor from '@monaco-editor/react';

export default function CodeEditor({ code, setCode, language }) {
  return (
    <Editor
      height="400px"
      language={language}
      value={code}
      onChange={setCode}
      theme="vs-dark"
      options={{
        minimap: { enabled: false },
        fontSize: 14,
        fontFamily: '"Fira Code", monospace',
        automaticLayout: true
      }}
    />
  );
}
```

### Bý?c 4: Build & Deploy

```bash
# Build production
npm run build

# Deploy ke Firebase Hosting
npm install -g firebase-tools
firebase login
firebase init hosting
firebase deploy
```

---

## ?? Summary: Upgrade Roadmap

| Tier | Feature | Time | Difficulty | Priority |
|------|---------|------|------------|----------|
| 1 | Protect API Keys | 45 min | ? | ?? HIGH |
| 2 | Logging System | 1.5h | ?? | ?? HIGH |
| 3 | Authentication | 2h | ??? | ?? HIGH |
| 4 | Multi-Language | 3h | ???? | ?? MEDIUM |
| 5 | Docker/CI-CD | 2h | ??? | ?? MEDIUM |
| 6 | React Frontend | 10h | ????? | ?? LOW |

---

**Total Upgrade Time:** 20-24 gi? ð? hoàn thành t?t c? Tier

**Recommend Implementation Order:**
1. Start with Tier 1-2 (Security & Logging) - 2 gi?
2. Add Tier 3 (Auth) - 2 gi? thêm
3. Then Tier 4-5 (Features & DevOps) - 5 gi? thêm
4. Finally Tier 6 (UI) - 10 gi? thêm

Good luck! ??
