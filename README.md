
# ?? NEO ONLINE JUDGE

**NEO ONLINE JUDGE** l� m?t n?n t?ng h?c l?p tr?nh t��ng t�c ��?c t?i �u cho ng�?i d�ng Vi?t Nam, k?t h?p t�nh n�ng ch?m b�i t? �?ng, h�?ng d?n AI, v� m�i tr�?ng thi �?u l?p tr?nh tr?c tuy?n.

---

## ?? M?c L?c
- [? T�nh N�ng](#-t�nh-n�ng)
- [??? C�ng Ngh? S? D?ng](#?-c�ng-ngh?-s?-d?ng)
- [?? C?u Tr�c D? �n](#-c?u-tr�c-d?-�n)
- [?? C�i �?t & Ch?y](#-c�i-�?t--ch?y)
- [?? H�?ng D?n S? D?ng](#-h�?ng-d?n-s?-d?ng)
- [?? C?u H?nh Firebase](#-c?u-h?nh-firebase)
- [?? G?i ? N�ng C?p](#-g?i-?-n�ng-c?p)
- [?? ��ng G�p](#-��ng-g�p)
- [?? Gi?y Ph�p](#-gi?y-ph�p)

---

## ? T�nh N�ng

### ?? Cho H?c Sinh
- ? **Luy?n T?p**: Gi?i c�c b�i to�n l?p tr?nh v� nh?n �i?m t?c th?
- ?? **AI Mentor**: Nh?n nh?n x�t, g?i ? t? AI (GPT-4o-mini) m� kh�ng c?n ��p �n �?y �?
- ?? **Theo D?i Ti?n �?**: Xem l?ch s? submissions v� �i?m s?
- ?? **B?ng X?p H?ng**: So s�nh k?t qu? v?i nh?ng ng�?i d�ng kh�c
- ?? **Ch? �? Thi �?u**: Tham gia c�c cu?c thi l?p tr?nh tr?c tuy?n

### ????? Cho Gi�o Vi�n/Admin
- ?? **Qu?n L? �? B�i**: T?o, ch?nh s?a b�i to�n v?i c�c test case
- ?? **Ch?m �i?m T? �?ng**: H? th?ng t? �?ng ch?m b�i 24/7
- ?? **Gi�m S�t Thi �?u**: Qu?n l? c�c cu?c thi v� k?t qu? sinh vi�n
- ?? **Th� Vi?n B�i T?p**: L�u tr? h�ng tr�m b�i to�n ph�n lo?i theo c?p �?

### ?? �?c �i?m N?i B?t
- **?? UI Cyberpunk**: Giao di?n hi?n �?i, b?t m?t v?i hi?u ?ng neon
- **???? H? Tr? Ti?ng Vi?t**: To�n b? n?i dung ��?c b?n �?a h�a
- **? Real-time**: C?p nh?t k?t qu? ch?m �i?m t?c th?
- **?? Responsive**: Ho?t �?ng t?t tr�n desktop, tablet, mobile
- **?? B?o M?t**: Firebase Authentication & Database Rules

---

## ??? C�ng Ngh? S? D?ng

### Backend
| C�ng Ngh? | M?c ��ch | Phi�n B?n |
|-----------|---------|----------|
| **Python** | Backend Judge, x? l? bi�n d?ch & ch?m �i?m | 3.8+ |
| **Firebase Realtime DB** | L�u tr? d? li?u submissions, problems, users | Latest |
| **Firebase Admin SDK** | Qu?n l? d? li?u t? backend | Latest |
| **OpenAI API** | AI Mentor - nh?n x�t code | GPT-4o-mini |

### Frontend
| C�ng Ngh? | M?c ��ch |
|-----------|---------|
| **HTML5** | Markup c?u tr�c |
| **CSS3** | Styling & Animation (Cyberpunk UI) |
| **JavaScript (Vanilla)** | Interactivity & Real-time Updates |
| **Firebase SDK** | K?t n?i Realtime Database |

### H? Tr? Ng�n Ng? L?p Tr?nh
- ? **Python** - Ch?y tr?c ti?p
- ? **C++** - Bi�n d?ch v?i g++
- ?? **C**, **Java**, **JavaScript** - C?n th�m h? tr?

---

## ?? C?u Tr�c D? �n

```
NEO-ONLINE-JUDGE/
??? judge.py                      # ?? Backend Judge Server (Core)
??? public/
?   ??? index.html               # ?? Trang ch? (Cyberpunk Gateway)
?   ??? problems.html            # ?? Danh s�ch b�i to�n
?   ??? solve.html               # ?? So?n th?o & submit code
?   ??? contest.html             # ?? Danh s�ch cu?c thi
?   ??? contest_room.html        # ?? Ph?ng thi �?u
?   ??? rank.html                # ?? B?ng x?p h?ng
?   ??? history.html             # ?? L?ch s? submissions
?   ??? guide.html               # ?? H�?ng d?n s? d?ng
?   ??? videos.html              # ?? Video h�?ng d?n
?   ??? documents.html           # ?? T�i li?u
?   ??? about.html               # ?? V? d? �n
??? KEY/
?   ??? resources.json           # ?? D? li?u t�i nguy�n (API keys, config)
??? .git/                        # Version control

```

---

## ?? C�i �?t & Ch?y

### Y�u C?u H? Th?ng
- **Python 3.8+**
- **g++ compiler** (cho C++ support)
- **Internet connection** (k?t n?i Firebase & OpenAI)

### 1?? Clone Repo
```bash
git clone https://github.com/II-Max/NEO-ONLINE-JUDGE.git
cd NEO-ONLINE-JUDGE
```

### 2?? C�i �?t Dependencies
```bash
pip install -r requirements.txt
```

*(N?u ch�a c� `requirements.txt`, ch?y:)*
```bash
pip install firebase-admin requests
```

### 3?? C?u H?nh Firebase
- T?o file `service-account.json` t? Firebase Console
- �?t file v�o th� m?c g?c c?a d? �n
- C?p nh?t `DB_URL` trong `judge.py` n?u c?n

### 4?? C?u H?nh OpenAI API
- L?y API key t? [platform.openai.com](https://platform.openai.com)
- C?p nh?t `OPENAI_API_KEY` trong `judge.py`

### 5?? Kh?i �?ng Judge Server
```bash
python judge.py
```

**Output mong �?i:**
```
>> [SYSTEM] �ang kh?i �?ng NEO JUDGE CORE...
   -> [OK] K?t n?i Firebase th�nh c�ng.

?? SERVER START (Mode: Independent Scoring)
?? AI Model: gpt-4o-mini
==================================================
```

### 6?? M? Frontend
M? file `public/index.html` trong tr?nh duy?t, ho?c:
```bash
python -m http.server 8000
# Truy c?p: http://localhost:8000/public/index.html
```

---


## ?? H�?ng D?n S? D?ng

### ????? Cho H?c Sinh

#### ?? Gi?i B�i T?p
1. �i �?n **"LUY?N T?P"** ? Ch?n b�i to�n
2. So?n code trong tr?nh so?n th?o
3. Click **"SUBMIT"** �? n?p b�i
4. Xem k?t qu? ch?m �i?m t?c th? (��ng/Sai test cases)

#### ?? S? D?ng AI Mentor
1. Sau khi submit b�i, click **"Y�U C?U AI"**
2. AI s? ph�n t�ch code c?a b?n
3. Nh?n ��?c g?i ?, kh�ng ph?i ��p �n �?y �?
4. C?i thi?n k? n�ng l?p tr?nh

#### ?? Xem Ti?n �?
- **L?CH S?**: Xem t?t c? submissions
- **X?P H?NG**: So s�nh �i?m v?i ng�?i kh�c

#### ?? Tham Gia Thi �?u
1. V�o **"THI �?U"** ? Ch?n cu?c thi
2. Click **"THAM GIA"**
3. Gi?i c�c b�i trong khung th?i gian quy �?nh
4. Xem b?ng x?p h?ng cu?c thi

### ????? Cho Qu?n Tr? Vi�n

#### ? Th�m B�i T?p
1. V�o Firebase Console
2. T?o document trong collection `problems`
3. C?u tr�c:
   ```json
   {
     "id": "problem_001",
     "title": "T�nh T?ng Hai S?",
     "description": "Nh?p hai s? a v� b, t�nh t?ng",
     "level": "d?",
     "language_support": ["python", "cpp"],
     "testcases": [
       {"input": "5 3", "output": "8"},
       {"input": "10 20", "output": "30"}
     ]
   }
   ```

#### ?? T?o Cu?c Thi
1. V�o Firebase Console
2. T?o document trong collection `contests`
3. Th�m th�ng tin: `title`, `start_time`, `end_time`, `problems`

---

## ?? C?u H?nh Firebase

### Quy C?u Tr�c Database
```
neo-online-judge-default-rtdb/
??? users/                        # Th�ng tin ng�?i d�ng
?   ??? {uid}/
?       ??? name
?       ??? email
?       ??? score
?       ??? join_date
??? problems/                     # Th� vi?n b�i t?p
?   ??? {problem_id}/
?       ??? title
?       ??? description
?       ??? testcases[]
?       ??? level
??? submissions/                  # N?p b�i luy?n t?p
?   ??? {submission_id}/
?       ??? user_id
?       ??? problem_id
?       ??? code
?       ??? language
?       ??? status: "pending" | "completed"
?       ??? score
?       ??? message
??? contest_submissions/          # N?p b�i thi �?u
?   ??? {submission_id}/
?       ??? [t��ng t? submissions]
??? contests/                     # Danh s�ch cu?c thi
?   ??? {contest_id}/
?       ??? title
?       ??? start_time
?       ??? end_time
?       ??? problems[]
??? ai_requests/                  # Y�u c?u AI Mentor
    ??? {request_id}/
        ??? user_id
        ??? code
        ??? problem_desc
        ??? status: "pending" | "completed"
        ??? response
```

---


## ?? G?i ? N�ng C?p

### ?? **Tier 1: B?o M?t & ?n �?nh (C?p �?: Cao)**

1. **?? B?o V? API Key**
   ```python
   # ? HI?N T?I (Kh�ng an to�n): API key hardcode
   OPENAI_API_KEY = "sk-xxx..."

   # ? C?P NH?T: S? d?ng environment variables
   import os
   from dotenv import load_dotenv
   load_dotenv()
   OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
   DB_URL = os.getenv('DB_URL')
   ```

   **T?o file `.env`:**
   ```env
   OPENAI_API_KEY=sk-xxx...
   DB_URL=https://...
   CRED_PATH=./service-account.json
   ```

2. **??? X�c Th?c & Ph�n Quy?n**
   - Th�m Firebase Authentication
   - Ki?m tra user permissions tr�?c khi ch?m b�i
   - Ng�n ch?n cheating (gi?i h?n submission/ph�t)

3. **?? X? L? L?i T?t H�n**
   ```python
   # ? Logging chi ti?t
   import logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   # Thay v?: print(f"L?i: {e}")
   # D�ng: logger.error(f"L?i Firebase: {e}", exc_info=True)
   ```

---

### ?? **Tier 2: M? R?ng Ch?c N�ng (C?p �?: Cao)**

4. **?? H? Tr? Th�m Ng�n Ng?**
   ```python
   def compile_code(lang, filename, code):
       # Th�m: Java, JavaScript, Go, Rust...

       if lang == 'java':
           with open(f"{filename}.java", "w") as f: f.write(code)
           res = subprocess.run(["javac", f"{filename}.java"], ...)
           return [f"java", "-cp", ".", filename], None

       elif lang == 'javascript':
           with open(f"{filename}.js", "w") as f: f.write(code)
           return ["node", f"{filename}.js"], None
   ```

5. **?? H? Tr? Multiple File Submissions**
   - Cho ph�p n?p multiple files (header files, class files)
   - H? tr? project-based problems

6. **?? H? Th?ng Tutorial & Streaming**
   - T�ch h?p YouTube tutorials
   - Support livestream coding sessions

---

### ?? **Tier 3: Hi?u N�ng & DevOps (C?p �?: Trung-Cao)**

7. **? T?i �u Performance**
   ```python
   # ? S? d?ng Queue (Redis) thay v? polling
   import redis
   from rq import Queue

   q = Queue(connection=redis.Redis())
   job = q.enqueue(process_submission_queue, 'submissions')
   ```

8. **?? Containerization (Docker)**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "judge.py"]
   ```

   **T?o `docker-compose.yml`:**
   ```yaml
   version: '3.8'
   services:
     judge:
       build: .
       environment:
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - DB_URL=${DB_URL}
       volumes:
         - ./service-account.json:/app/service-account.json
   ```

9. **?? Monitoring & Logging**
   - T�ch h?p Sentry cho error tracking
   - CloudWatch logs
   - Prometheus metrics

---

### ?? **Tier 4: C?i Thi?n UX/UI (C?p �?: Trung)**

10. **?? Frontend Modernization**
    - Migrate sang React/Vue.js
    - Code editor t�ch h?p (Monaco Editor)
    - Real-time collaboration (code pairing)

11. **?? Mobile App**
    - React Native ho?c Flutter app
    - Push notifications

12. **?? Dark/Light Mode**
    - Toggle theme
    - User preference persistence

---

### ?? **Tier 5: AI & Machine Learning (C?p �?: Cao)**

13. **?? Advanced AI Features**
    ```python
    # T�ch h?p multiple AI models
    MODELS = {
        'gpt-4': 'Chi ti?t, logic ph?c t?p',
        'gpt-4-turbo': 'C�n b?ng t?c �?/ch?t l�?ng',
        'claude-3': 'Ph�n t�ch chuy�n s�u',
        'llama-2': 'Open source alternative'
    }
    ```

14. **?? Ph�n T�ch & Recommendations**
    - D? �o�n �i?m d?a v�o l?ch s?
    - G?i ? b�i t?p ph� h?p level
    - Analytics dashboard

15. **?? Plagiarism Detection**
    - So s�nh code similarity
    - Detect copy-paste

---

## ?? Checklist N�ng C?p �u Ti�n

| �u Ti�n | T�nh N�ng | Th?i Gian | Kh� �? |
|---------|----------|----------|---------|
| ?? Cao | B?o v? API keys | 30 ph�t | D? |
| ?? Cao | Logging & Error Handling | 1 gi? | D? |
| ?? Cao | Authentication | 2 gi? | Trung |
| ?? Cao | C/Java/JS Support | 3 gi? | Trung |
| ?? Trung | Redis Queue | 2 gi? | Trung |
| ?? Trung | Docker & CI/CD | 3 gi? | Cao |
| ?? Trung | React Frontend | 8-10 gi? | Cao |
| ?? Th?p | AI Models | 2-4 gi? | Cao |

---

## ?? B?t �?u V?i Tier 1

### B�?c 1: T?o `.env` file
```bash
touch .env
```

### B�?c 2: C?p nh?t `judge.py`
```python
import os
from dotenv import load_dotenv

load_dotenv()

CRED_PATH = os.getenv('CRED_PATH', 'service-account.json')
DB_URL = os.getenv('DB_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CURRENT_MODEL = os.getenv('MODEL', 'gpt-4o-mini')
```

### B�?c 3: C�i �?t Dependencies
```bash
pip install python-dotenv
```

---

## ?? ��ng G�p

Ch�ng t�i hoan ngh�nh c�c ��ng g�p t? c?ng �?ng!

### C�ch ��ng G�p
1. Fork repository
2. T?o feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Code Style
- Tu�n theo PEP 8 (Python)
- S? d?ng meaningful variable names
- Th�m comments cho logic ph?c t?p
- Test tr�?c khi PR

---

## ?? Gi?y Ph�p

D? �n n�y ��?c c?p ph�p d�?i MIT License - xem file [LICENSE](LICENSE) �? bi?t chi ti?t.

---

## ?? Li�n H? & H? Tr?

- ?? Email: support@neo-judge.io
- ?? Issues: [GitHub Issues](https://github.com/II-Max/NEO-ONLINE-JUDGE/issues)
- ?? Discussions: [GitHub Discussions](https://github.com/II-Max/NEO-ONLINE-JUDGE/discussions)
- ?? Website: [neo-judge.io](https://neo-judge.io)

---

## ?? C?m �n

- **Firebase** - Backend as a Service
- **OpenAI** - AI Mentor Engine
- **Community** - Feedback & Contributions

---

**Made with ?? by NEO Judge Team**

Last Updated: 2024 | Version: 1.0

