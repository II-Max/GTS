# ?? NEO ONLINE JUDGE

**NEO ONLINE JUDGE** là m?t n?n t?ng h?c l?p tr?nh týõng tác ðý?c t?i ýu cho ngý?i dùng Vi?t Nam, k?t h?p tính nãng ch?m bài t? ð?ng, hý?ng d?n AI, và môi trý?ng thi ð?u l?p tr?nh tr?c tuy?n.

---

## ?? M?c L?c
- [? Tính Nãng](#-tính-nãng)
- [??? Công Ngh? S? D?ng](#?-công-ngh?-s?-d?ng)
- [?? C?u Trúc D? Án](#-c?u-trúc-d?-án)
- [?? Cài Ð?t & Ch?y](#-cài-ð?t--ch?y)
- [?? Hý?ng D?n S? D?ng](#-hý?ng-d?n-s?-d?ng)
- [?? C?u H?nh Firebase](#-c?u-h?nh-firebase)
- [?? G?i ? Nâng C?p](#-g?i-?-nâng-c?p)
- [?? Ðóng Góp](#-ðóng-góp)
- [?? Gi?y Phép](#-gi?y-phép)

---

## ? Tính Nãng

### ?? Cho H?c Sinh
- ? **Luy?n T?p**: Gi?i các bài toán l?p tr?nh và nh?n ði?m t?c th?
- ?? **AI Mentor**: Nh?n nh?n xét, g?i ? t? AI (GPT-4o-mini) mà không c?n ðáp án ð?y ð?
- ?? **Theo D?i Ti?n Ð?**: Xem l?ch s? submissions và ði?m s?
- ?? **B?ng X?p H?ng**: So sánh k?t qu? v?i nh?ng ngý?i dùng khác
- ?? **Ch? Ð? Thi Ð?u**: Tham gia các cu?c thi l?p tr?nh tr?c tuy?n

### ????? Cho Giáo Viên/Admin
- ?? **Qu?n L? Ð? Bài**: T?o, ch?nh s?a bài toán v?i các test case
- ?? **Ch?m Ði?m T? Ð?ng**: H? th?ng t? ð?ng ch?m bài 24/7
- ?? **Giám Sát Thi Ð?u**: Qu?n l? các cu?c thi và k?t qu? sinh viên
- ?? **Thý Vi?n Bài T?p**: Lýu tr? hàng trãm bài toán phân lo?i theo c?p ð?

### ?? Ð?c Ði?m N?i B?t
- **?? UI Cyberpunk**: Giao di?n hi?n ð?i, b?t m?t v?i hi?u ?ng neon
- **???? H? Tr? Ti?ng Vi?t**: Toàn b? n?i dung ðý?c b?n ð?a hóa
- **? Real-time**: C?p nh?t k?t qu? ch?m ði?m t?c th?
- **?? Responsive**: Ho?t ð?ng t?t trên desktop, tablet, mobile
- **?? B?o M?t**: Firebase Authentication & Database Rules

---

## ??? Công Ngh? S? D?ng

### Backend
| Công Ngh? | M?c Ðích | Phiên B?n |
|-----------|---------|----------|
| **Python** | Backend Judge, x? l? biên d?ch & ch?m ði?m | 3.8+ |
| **Firebase Realtime DB** | Lýu tr? d? li?u submissions, problems, users | Latest |
| **Firebase Admin SDK** | Qu?n l? d? li?u t? backend | Latest |
| **OpenAI API** | AI Mentor - nh?n xét code | GPT-4o-mini |

### Frontend
| Công Ngh? | M?c Ðích |
|-----------|---------|
| **HTML5** | Markup c?u trúc |
| **CSS3** | Styling & Animation (Cyberpunk UI) |
| **JavaScript (Vanilla)** | Interactivity & Real-time Updates |
| **Firebase SDK** | K?t n?i Realtime Database |

### H? Tr? Ngôn Ng? L?p Tr?nh
- ? **Python** - Ch?y tr?c ti?p
- ? **C++** - Biên d?ch v?i g++
- ?? **C**, **Java**, **JavaScript** - C?n thêm h? tr?

---

## ?? C?u Trúc D? Án

```
NEO-ONLINE-JUDGE/
??? judge.py                      # ?? Backend Judge Server (Core)
??? public/
?   ??? index.html               # ?? Trang ch? (Cyberpunk Gateway)
?   ??? problems.html            # ?? Danh sách bài toán
?   ??? solve.html               # ?? So?n th?o & submit code
?   ??? contest.html             # ?? Danh sách cu?c thi
?   ??? contest_room.html        # ?? Ph?ng thi ð?u
?   ??? rank.html                # ?? B?ng x?p h?ng
?   ??? history.html             # ?? L?ch s? submissions
?   ??? guide.html               # ?? Hý?ng d?n s? d?ng
?   ??? videos.html              # ?? Video hý?ng d?n
?   ??? documents.html           # ?? Tài li?u
?   ??? about.html               # ?? V? d? án
??? KEY/
?   ??? resources.json           # ?? D? li?u tài nguyên (API keys, config)
??? .git/                        # Version control

```

---

## ?? Cài Ð?t & Ch?y

### Yêu C?u H? Th?ng
- **Python 3.8+**
- **g++ compiler** (cho C++ support)
- **Internet connection** (k?t n?i Firebase & OpenAI)

### 1?? Clone Repo
```bash
git clone https://github.com/II-Max/NEO-ONLINE-JUDGE.git
cd NEO-ONLINE-JUDGE
```

### 2?? Cài Ð?t Dependencies
```bash
pip install -r requirements.txt
```

*(N?u chýa có `requirements.txt`, ch?y:)*
```bash
pip install firebase-admin requests
```

### 3?? C?u H?nh Firebase
- T?o file `service-account.json` t? Firebase Console
- Ð?t file vào thý m?c g?c c?a d? án
- C?p nh?t `DB_URL` trong `judge.py` n?u c?n

### 4?? C?u H?nh OpenAI API
- L?y API key t? [platform.openai.com](https://platform.openai.com)
- C?p nh?t `OPENAI_API_KEY` trong `judge.py`

### 5?? Kh?i Ð?ng Judge Server
```bash
python judge.py
```

**Output mong ð?i:**
```
>> [SYSTEM] Ðang kh?i ð?ng NEO JUDGE CORE...
   -> [OK] K?t n?i Firebase thành công.

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

## ?? Hý?ng D?n S? D?ng

### ????? Cho H?c Sinh

#### ?? Gi?i Bài T?p
1. Ði ð?n **"LUY?N T?P"** ? Ch?n bài toán
2. So?n code trong tr?nh so?n th?o
3. Click **"SUBMIT"** ð? n?p bài
4. Xem k?t qu? ch?m ði?m t?c th? (Ðúng/Sai test cases)

#### ?? S? D?ng AI Mentor
1. Sau khi submit bài, click **"YÊU C?U AI"**
2. AI s? phân tích code c?a b?n
3. Nh?n ðý?c g?i ?, không ph?i ðáp án ð?y ð?
4. C?i thi?n k? nãng l?p tr?nh

#### ?? Xem Ti?n Ð?
- **L?CH S?**: Xem t?t c? submissions
- **X?P H?NG**: So sánh ði?m v?i ngý?i khác

#### ?? Tham Gia Thi Ð?u
1. Vào **"THI Ð?U"** ? Ch?n cu?c thi
2. Click **"THAM GIA"**
3. Gi?i các bài trong khung th?i gian quy ð?nh
4. Xem b?ng x?p h?ng cu?c thi

### ????? Cho Qu?n Tr? Viên

#### ? Thêm Bài T?p
1. Vào Firebase Console
2. T?o document trong collection `problems`
3. C?u trúc:
   ```json
   {
     "id": "problem_001",
     "title": "Tính T?ng Hai S?",
     "description": "Nh?p hai s? a và b, tính t?ng",
     "level": "d?",
     "language_support": ["python", "cpp"],
     "testcases": [
       {"input": "5 3", "output": "8"},
       {"input": "10 20", "output": "30"}
     ]
   }
   ```

#### ?? T?o Cu?c Thi
1. Vào Firebase Console
2. T?o document trong collection `contests`
3. Thêm thông tin: `title`, `start_time`, `end_time`, `problems`

---

## ?? C?u H?nh Firebase

### Quy C?u Trúc Database
```
neo-online-judge-default-rtdb/
??? users/                        # Thông tin ngý?i dùng
?   ??? {uid}/
?       ??? name
?       ??? email
?       ??? score
?       ??? join_date
??? problems/                     # Thý vi?n bài t?p
?   ??? {problem_id}/
?       ??? title
?       ??? description
?       ??? testcases[]
?       ??? level
??? submissions/                  # N?p bài luy?n t?p
?   ??? {submission_id}/
?       ??? user_id
?       ??? problem_id
?       ??? code
?       ??? language
?       ??? status: "pending" | "completed"
?       ??? score
?       ??? message
??? contest_submissions/          # N?p bài thi ð?u
?   ??? {submission_id}/
?       ??? [týõng t? submissions]
??? contests/                     # Danh sách cu?c thi
?   ??? {contest_id}/
?       ??? title
?       ??? start_time
?       ??? end_time
?       ??? problems[]
??? ai_requests/                  # Yêu c?u AI Mentor
    ??? {request_id}/
        ??? user_id
        ??? code
        ??? problem_desc
        ??? status: "pending" | "completed"
        ??? response
```

---

## ?? G?i ? Nâng C?p

### ?? **Tier 1: B?o M?t & ?n Ð?nh (C?p Ð?: Cao)**

1. **?? B?o V? API Key**
   ```python
   # ? HI?N T?I (Không an toàn): API key hardcode
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

2. **??? Xác Th?c & Phân Quy?n**
   - Thêm Firebase Authentication
   - Ki?m tra user permissions trý?c khi ch?m bài
   - Ngãn ch?n cheating (gi?i h?n submission/phút)

3. **?? X? L? L?i T?t Hõn**
   ```python
   # ? Logging chi ti?t
   import logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   # Thay v?: print(f"L?i: {e}")
   # Dùng: logger.error(f"L?i Firebase: {e}", exc_info=True)
   ```

---

### ?? **Tier 2: M? R?ng Ch?c Nãng (C?p Ð?: Cao)**

4. **?? H? Tr? Thêm Ngôn Ng?**
   ```python
   def compile_code(lang, filename, code):
       # Thêm: Java, JavaScript, Go, Rust...

       if lang == 'java':
           with open(f"{filename}.java", "w") as f: f.write(code)
           res = subprocess.run(["javac", f"{filename}.java"], ...)
           return [f"java", "-cp", ".", filename], None

       elif lang == 'javascript':
           with open(f"{filename}.js", "w") as f: f.write(code)
           return ["node", f"{filename}.js"], None
   ```

5. **?? H? Tr? Multiple File Submissions**
   - Cho phép n?p multiple files (header files, class files)
   - H? tr? project-based problems

6. **?? H? Th?ng Tutorial & Streaming**
   - Tích h?p YouTube tutorials
   - Support livestream coding sessions

---

### ?? **Tier 3: Hi?u Nãng & DevOps (C?p Ð?: Trung-Cao)**

7. **? T?i Ýu Performance**
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
   - Tích h?p Sentry cho error tracking
   - CloudWatch logs
   - Prometheus metrics

---

### ?? **Tier 4: C?i Thi?n UX/UI (C?p Ð?: Trung)**

10. **?? Frontend Modernization**
    - Migrate sang React/Vue.js
    - Code editor tích h?p (Monaco Editor)
    - Real-time collaboration (code pairing)

11. **?? Mobile App**
    - React Native ho?c Flutter app
    - Push notifications

12. **?? Dark/Light Mode**
    - Toggle theme
    - User preference persistence

---

### ?? **Tier 5: AI & Machine Learning (C?p Ð?: Cao)**

13. **?? Advanced AI Features**
    ```python
    # Tích h?p multiple AI models
    MODELS = {
        'gpt-4': 'Chi ti?t, logic ph?c t?p',
        'gpt-4-turbo': 'Cân b?ng t?c ð?/ch?t lý?ng',
        'claude-3': 'Phân tích chuyên sâu',
        'llama-2': 'Open source alternative'
    }
    ```

14. **?? Phân Tích & Recommendations**
    - D? ðoán ði?m d?a vào l?ch s?
    - G?i ? bài t?p phù h?p level
    - Analytics dashboard

15. **?? Plagiarism Detection**
    - So sánh code similarity
    - Detect copy-paste

---

## ?? Checklist Nâng C?p Ýu Tiên

| Ýu Tiên | Tính Nãng | Th?i Gian | Khó Ð? |
|---------|----------|----------|---------|
| ?? Cao | B?o v? API keys | 30 phút | D? |
| ?? Cao | Logging & Error Handling | 1 gi? | D? |
| ?? Cao | Authentication | 2 gi? | Trung |
| ?? Cao | C/Java/JS Support | 3 gi? | Trung |
| ?? Trung | Redis Queue | 2 gi? | Trung |
| ?? Trung | Docker & CI/CD | 3 gi? | Cao |
| ?? Trung | React Frontend | 8-10 gi? | Cao |
| ?? Th?p | AI Models | 2-4 gi? | Cao |

---

## ?? B?t Ð?u V?i Tier 1

### Bý?c 1: T?o `.env` file
```bash
touch .env
```

### Bý?c 2: C?p nh?t `judge.py`
```python
import os
from dotenv import load_dotenv

load_dotenv()

CRED_PATH = os.getenv('CRED_PATH', 'service-account.json')
DB_URL = os.getenv('DB_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CURRENT_MODEL = os.getenv('MODEL', 'gpt-4o-mini')
```

### Bý?c 3: Cài Ð?t Dependencies
```bash
pip install python-dotenv
```

---

## ?? Ðóng Góp

Chúng tôi hoan nghênh các ðóng góp t? c?ng ð?ng!

### Cách Ðóng Góp
1. Fork repository
2. T?o feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Code Style
- Tuân theo PEP 8 (Python)
- S? d?ng meaningful variable names
- Thêm comments cho logic ph?c t?p
- Test trý?c khi PR

---

## ?? Gi?y Phép

D? án này ðý?c c?p phép dý?i MIT License - xem file [LICENSE](LICENSE) ð? bi?t chi ti?t.

---

## ?? Liên H? & H? Tr?

- ?? Email: support@neo-judge.io
- ?? Issues: [GitHub Issues](https://github.com/II-Max/NEO-ONLINE-JUDGE/issues)
- ?? Discussions: [GitHub Discussions](https://github.com/II-Max/NEO-ONLINE-JUDGE/discussions)
- ?? Website: [neo-judge.io](https://neo-judge.io)

---

## ?? C?m Õn

- **Firebase** - Backend as a Service
- **OpenAI** - AI Mentor Engine
- **Community** - Feedback & Contributions

---

**Made with ?? by NEO Judge Team**

Last Updated: 2024 | Version: 1.0
