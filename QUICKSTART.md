# ?? QUICK START - NEO ONLINE JUDGE

Hý?ng d?n kh?i ð?ng nhanh trong 5 phút! ?

---

## ?? M?c Tiêu: Kh?i Ð?ng Judge Server

### 1?? **Chu?n B?** (2 phút)

```bash
# Clone/Navigate to project
cd NEO-ONLINE-JUDGE

# T?o virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2?? **Cài Ð?t Dependencies** (1 phút)

```bash
pip install -r requirements.txt
```

### 3?? **C?u H?nh Firebase** (1 phút)

1. T?o `.env` file:
```bash
cp .env.example .env
```

2. Edit `.env` và thêm credentials:
```env
OPENAI_API_KEY=sk-your-key-here
DB_URL=https://your-db.firebaseio.com
CRED_PATH=./service-account.json
```

3. Download `service-account.json` t? Firebase Console

### 4?? **Ch?y Server** (1 phút)

```bash
python judge.py
```

**Output mong ð?i:**
```
>> [SYSTEM] Ðang kh?i ð?ng NEO JUDGE CORE...
   -> [OK] K?t n?i Firebase thành công.
?? SERVER START (Mode: Independent Scoring)
```

---

## ?? Ch?y Frontend

### Option 1: Tr?c ti?p
```bash
# M? file trong tr?nh duy?t
open public/index.html
```

### Option 2: Web Server
```bash
python -m http.server 8000
# Truy c?p: http://localhost:8000/public
```

---

## ?? C?u H?nh Nhanh

### T?p Quan Tr?ng

| T?p | M?c Ðích |
|-----|---------|
| `.env` | Environment variables |
| `judge.py` | Backend judge server |
| `public/index.html` | Frontend gateway |
| `requirements.txt` | Python dependencies |

### Folder Structure

```
?? NEO-ONLINE-JUDGE
??? ?? judge.py                 # Backend
??? ?? requirements.txt         # Dependencies
??? ?? .env                     # Config (t?o t? .env.example)
??? ?? service-account.json     # Firebase creds
??? ?? public/                  # Frontend
?   ??? ?? index.html          # Trang ch?
?   ??? ?? solve.html          # So?n code
?   ??? ?? problems.html       # Danh sách bài
?   ??? ...
??? ?? KEY/
    ??? ?? resources.json      # Tài nguyên
```

---

## ?? Troubleshooting

### ? Error: "No module named 'firebase_admin'"
**Solution:**
```bash
pip install firebase-admin
```

### ? Error: ".env file not found"
**Solution:**
```bash
cp .env.example .env
# Edit .env with your credentials
```

### ? Error: "Connection refused (Firebase)"
**Solution:**
1. Check `DB_URL` in `.env` is correct
2. Check Firebase database exists and is accessible
3. Verify `service-account.json` is valid

### ? Error: "401 OpenAI API Key invalid"
**Solution:**
1. Get new API key from https://platform.openai.com
2. Update `OPENAI_API_KEY` in `.env`
3. Ensure key has required permissions

---

## ? Verify Setup

### Test Backend
```bash
python -c "
import firebase_admin
from firebase_admin import db, credentials
import os
from dotenv import load_dotenv

load_dotenv()
cred = credentials.Certificate(os.getenv('CRED_PATH'))
app = firebase_admin.initialize_app(cred, {'databaseURL': os.getenv('DB_URL')})
print('? Firebase connected!')
"
```

### Test API
```bash
python -c "
import requests
import os
from dotenv import load_dotenv

load_dotenv()
headers = {'Authorization': f'Bearer {os.getenv(\"OPENAI_API_KEY\")}'}
response = requests.get('https://api.openai.com/v1/models', headers=headers)
print(f'Status: {response.status_code}')
print('? OpenAI API working!' if response.status_code == 200 else '? API error')
"
```

---

## ?? Next Steps

### Sau khi kh?i ð?ng thành công:

1. **T?o bài t?p ð?u tiên:**
   - Vào Firebase Console
   - T?o problem trong collection `problems`

2. **Submit bài test:**
   - M? `public/solve.html`
   - Vi?t code Python/C++
   - Click "SUBMIT"

3. **Xem k?t qu?:**
   - Server t? ð?ng ch?m bài
   - Xem ði?m trong `public/history.html`

4. **Upgrade h? th?ng:**
   - Xem `UPGRADE_GUIDE.md` ð? thêm features
   - Xem `ROADMAP.md` ð? th?y k? ho?ch

---

## ?? Tài Li?u Ð?y Ð?

- **README.md** - T?ng quan d? án
- **UPGRADE_GUIDE.md** - Hý?ng d?n nâng c?p chi ti?t
- **ROADMAP.md** - K? ho?ch phát tri?n
- **CONTRIBUTING.md** - Hý?ng d?n ðóng góp
- **.env.example** - C?u h?nh m?u
- **Dockerfile** - Containerization

---

## ?? Tips

### Ch?y ? Background (Linux/Mac)
```bash
nohup python judge.py > judge.log 2>&1 &
```

### Ch?y ? Background (Windows)
```bash
start /B python judge.py > judge.log 2>&1
```

### Debug Mode
```bash
# Thêm vào judge.py
import logging
logging.basicConfig(level=logging.DEBUG)

# Ho?c set environment variable
set LOGLEVEL=DEBUG  # Windows
export LOGLEVEL=DEBUG  # Linux/Mac
```

### Restart Server
```bash
# T?m process
ps aux | grep judge.py  # Linux/Mac
tasklist | findstr python  # Windows

# Kill process
kill <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows

# Restart
python judge.py
```

---

## ?? Need Help?

- ?? Xem README.md
- ?? Report issues trên GitHub
- ?? Tham gia discussions
- ?? Email support

---

**Happy Coding! ??**

Last Updated: December 2024
