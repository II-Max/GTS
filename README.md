
<p align="center">
  <img src="https://ui-avatars.com/api/?name=NEO+OJ&background=00f3ff&color=05070a&size=128" alt="NEO OJ Logo" width="128">
</p>

<h1 align="center">NEO ONLINE JUDGE</h1>

<p align="center">
  <strong>Nền tảng học lập trình tương tác thông minh — Chấm bài tự động + AI Mentor</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=flat&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Firebase-Realtime%20DB-orange?style=flat&logo=firebase" alt="Firebase">
  <img src="https://img.shields.io/badge/AI-DeepSeek%20%7C%20Grok-brightgreen?style=flat&logo=openai" alt="AI">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat" alt="Status">
  <img src="https://img.shields.io/badge/Security-Hardened%20v3.0-red?style=flat&logo=shield" alt="Security">
</p>

---

## MUC LUC

- [Gioi Thieu](#gioi-thieu)
- [Tinh Nang Chinh](#tinh-nang-chinh)
- [Cong Nghe Su Dung](#cong-nghe-su-dung)
- [Cau Truc Du An](#cau-truc-du-an)
- [Huong Dan Cai Dat Nhanh](#huong-dan-cai-dat-nhanh)
- [Huong Dan Cai Dat Chi Tiet](#huong-dan-cai-dat-chi-tiet)
- [Huong Dan Su Dung](#huong-dan-su-dung)
- [Cau Truc Firebase Database](#cau-truc-firebase-database)
- [Bao Mat He Thong](#bao-mat-he-thong)
- [Kien Truc He Thong](#kien-truc-he-thong)
- [Xu Ly Su Co](#xu-ly-su-co-thuong-gap)
- [Lo Trinh Phat Trien](#lo-trinh-phat-trien)
- [Dong Gop](#dong-gop)
- [Giay Phep](#giay-phep)

---

## Gioi Thieu

**NEO Online Judge** la nen tang hoc lap trinh tuong tac toan dien duoc thiet ke danh rieng cho nguoi dung Viet Nam. Du an ket hop:

- **Cham bai tu dong** — Bien dich & chay test cases, cho diem tuc thi
- **AI Mentor thong minh** — Phan tich code, goi y sua loi ma khong dua dap an
- **Moi truong thi dau** — Phong thi truc tuyen co bam gio
- **Giao dien Cyberpunk** — UI hien dai, bat mat voi hieu ung neon
- **Bao mat cao** — Firebase Security Rules v3.0, JWT, CORS han che

Du an phu hop cho:
- **Truong hoc** — Lam cong cu day va hoc lap trinh
- **Cau lac bo** — To chuc thi dau, luyen tap
- **Ca nhan** — Tu hoc va ren luyen ky nang coding

---

## Tinh Nang Chinh

### Cho Hoc Sinh

| Tinh nang | Mo ta |
|-----------|-------|
| Kho bai tap | Bai toan phan loai theo 3 cap do: De - Trung binh - Kho |
| Code Editor | Soan thao code truc tuyen voi da ngon ngu (Python, C++, Java, Pascal) |
| Cham diem tuc thi | Nop bai va nhan ket qua ngay lap tuc |
| AI Mentor | Goi y sua loi thong minh tu AI (DeepSeek/Grok) — Yeu cau dang nhap |
| Dashboard ca nhan | Theo doi diem so, tien do hoc tap |
| Bang xep hang | So tai voi cac lap trinh vien khac (tu public_leaderboard) |
| Tai lieu & Video | Thu vien tai lieu PDF, video bai giang YouTube |
| Chat chung | Kenh thao luan toan he thong (co validate danh tinh) |

### Cho Giao Vien / Quan Tri Vien

| Tinh nang | Mo ta |
|-----------|-------|
| Them bai tap | Tao bai toan moi kem test cases qua giao dien |
| To chuc thi | Tao phong thi, quan ly thoi gian |
| Quan ly noi dung | Upload tai lieu, video bai giang |
| Cap quyen giao vien | Phai thuc hien qua Backend/Firebase Console |

### Dac Diem Noi Bat

- **UI Cyberpunk** — Giao dien toi gian, neon, hien dai
- **Ho tro tieng Viet** — Toan bo noi dung duoc ban dia hoa
- **Real-time** — Cap nhat ket qua cham diem tuc thoi
- **Bao mat cao** — Security Rules v3.0 + JWT + CORS han che

---

## Cong Nghe Su Dung

### Frontend

| Cong nghe | Muc dich |
|-----------|----------|
| **HTML5 / CSS3** | Cau truc & giao dien (Neo Design System) |
| **JavaScript (Vanilla)** | Tuong tac & cap nhat real-time |
| **Firebase JS SDK v8** | Ket noi Realtime Database & Auth |
| **Font Awesome 6** | Icon |

### Backend

| Cong nghe | Muc dich | Phien ban |
|-----------|----------|-----------| 
| **Python** | Backend Judge Server | 3.9+ |
| **Flask** | HTTP API Server | 3.x |
| **Firebase Admin SDK** | Quan ly du lieu tu backend (bypass rules) | Latest |
| **DeepSeek / Grok API** | AI Mentor | deepseek-chat / grok-3 |
| **g++ / javac** | Trinh bien dich C++, Java | Theo he thong |

### Infrastructure

| Thanh phan | Chi tiet |
|-----------|----------|
| **Database** | Firebase Realtime Database |
| **Security Rules** | Firebase Security Rules v3.0 |
| **Authentication** | Firebase Auth (Email, Google, GitHub) |
| **Hosting** | Firebase Hosting |

---

## Cau Truc Du An

```
NEO-ONLINE-JUDGE/
├── .env                              # Bien moi truong (KHONG commit)
├── .env.example                      # Mau cau hinh
├── service-account.json              # Firebase Admin key (KHONG commit)
├── database.rules.json               # Firebase Security Rules v3.0
├── firebase.json                     # Firebase CLI config
├── requirements.txt                  # Python dependencies
│
├── backend/
│   ├── app.py                        # JudgeApplication + Flask API
│   ├── judge.py                      # ENTRY POINT
│   ├── config/
│   │   ├── settings.py               # Settings (JWT bắt buộc, CORS han che)
│   │   └── logging.py
│   ├── core/
│   │   ├── compiler.py               # Bien dich da ngon ngu
│   │   └── judge.py                  # Engine cham diem
│   ├── services/
│   │   ├── firebase_service.py       # Firebase ops + update_public_leaderboard()
│   │   ├── auth_service.py           # Auth + JWT
│   │   └── ai_service.py             # AI Mentor
│   └── routes/
│       └── auth_routes.py            # API (bo login bang password rong)
│
├── frontend/
│   ├── index.html                    # Trang chu (stats tu /api/stats)
│   ├── rank.html                     # Bang XH (tu public_leaderboard)
│   ├── solve.html                    # Code editor (rate-limited, AI guard)
│   ├── history.html                  # Lich su (chi cua minh)
│   ├── ...
│   ├── css/neo-design.css
│   └── js/
│       ├── firebase-config.js
│       └── firebase-auth-check.js
│
└── logs/
```

---

## Huong Dan Cai Dat Nhanh

```bash
# 1. Clone du an
git clone https://github.com/II-Max/NEO-ONLINE-JUDGE.git
cd NEO-ONLINE-JUDGE

# 2. Cai Python dependencies
pip install -r requirements.txt

# 3. Tao file .env (xem chi tiet ben duoi)
cp .env.example .env

# 4. Dat file service-account.json vao thu muc goc

# 5. Tao JWT secret key
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
# Dan vao .env

# 6. Chay backend judge
python backend/judge.py

# 7. Deploy len Firebase
firebase deploy
```

---

## Huong Dan Cai Dat Chi Tiet

### 1. Clone & Cai Dependencies

```bash
git clone https://github.com/II-Max/NEO-ONLINE-JUDGE.git
cd NEO-ONLINE-JUDGE
pip install -r requirements.txt
```

### 2. Cau Hinh Firebase

#### Buoc A: Lay Firebase Config cho Frontend

1. Vao [Firebase Console](https://console.firebase.google.com)
2. Chon du an `gtsv2-a93c5`
3. Vao **Project settings** > **Your apps** > **Web app**
4. Copy `firebaseConfig`, cap nhat vao `frontend/js/firebase-config.js`

#### Buoc B: Lay Service Account cho Backend

1. Vao **Project settings** > **Service accounts**
2. **Generate new private key** > Luu file `service-account.json` vao thu muc goc

#### Buoc C: Bat Authentication

1. Vao **Authentication** > **Sign-in method**
2. Bat: **Email/Password**, **Google**, **GitHub**
3. Them domain vao **Authorized domains**: `localhost`, `gtsv2-a93c5.web.app`

#### Buoc D: Deploy Security Rules v3.0

```bash
firebase deploy --only database
```

> Cac rules trong `database.rules.json` bao gom:
> - `public_leaderboard`: Cong khai chi doc
> - `submissions`: `.indexOn: ["uid"]` cho query nhanh
> - `global_chat`: Validate danh tinh nguoi gui

### 3. Cau Hinh .env

Tao file `.env` trong thu muc goc:

```env
# === Firebase ===
CRED_PATH=service-account.json
DB_URL=https://gtsv2-a93c5-default-rtdb.firebaseio.com

# === AI (chon 1 trong 2) ===
DEEPSEEK_API_KEY=sk-xxx...        # https://platform.deepseek.com
# GROK_API_KEY=grok-xxx...        # https://console.x.ai

AI_MODEL=deepseek-chat
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=1000
AI_TIMEOUT=20

# === Judge Engine ===
JUDGE_TIMEOUT=3
POLL_INTERVAL=1.5

# === Server ===
HOST=0.0.0.0
PORT=5000

# === Authentication (BAT BUOC — phai dat gia tri ngu nhien manh) ===
JWT_SECRET_KEY=<chay: python -c "import secrets; print(secrets.token_hex(32))">
JWT_EXPIRY_HOURS=24

# === Logging ===
LOG_LEVEL=INFO
```

> ⚠️ **QUAN TRONG:**
> - `JWT_SECRET_KEY` PHAI duoc dat. Neu de trong, server se tu tao key ngau nhien moi lan khoi dong, dan den het phien dang nhap.
> - KHONG commit `.env` len git.

### 4. Chay Judge Server

```bash
python backend/judge.py
```

---

## Cau Truc Firebase Database

Cay du lieu chinh:

```
gtsv2-a93c5-default-rtdb/
├── users/{uid}                    # Thong tin ca nhan (chi doc chinh minh)
├── public_leaderboard/{uid}       # Diem cong khai (ai cung doc duoc)
├── problems/{id}                  # Bai tap (cong khai)
├── submissions/{id}               # Bai nop (chi doc cua minh hoac teacher)
├── contest_submissions/{id}       # Bai nop thi (tuong tu)
├── contests/{id}                  # Phong thi (yeu cau dang nhap)
├── ai_requests/{id}               # Yeu cau AI (chi doc cua minh hoac teacher)
├── documents/{id}                 # Tai lieu (yeu cau dang nhap)
├── videos/{id}                    # Video (yeu cau dang nhap)
└── global_chat/{id}               # Chat (yeu cau dang nhap + validate)
```

Xem chi tiet: [CSDL.md](CSDL.md)

---

## Bao Mat He Thong

### Cac lop bao mat (v3.0)

| Lop | Bien phap | Trang thai |
|-----|-----------|-----------|
| Firebase Rules | Phan quyen chi tiet theo tung node/UID | ✅ |
| Chong lo source code | Submission chi doc boi chinh minh | ✅ |
| Chong gia mao chat | Validate name/role khi gui tin | ✅ |
| Chong leo thang quyen | Hoc sinh khong tu sua role/score | ✅ |
| JWT Secret | Key ngau nhien 32 bytes, bat buoc | ✅ |
| CORS han che | Chi domain production + localhost | ✅ |
| Rate Limit | Khong nop bai > 1 lan / 5 giay | ✅ |
| AI Guard | Bat buoc dang nhap de dung AI | ✅ |
| Leaderboard an toan | public_leaderboard chi chua ten + diem | ✅ |
| Stats API | Backend tinh toan, khong lo data tho | ✅ |

### Tuyet doi KHONG duoc:

- ❌ Commit `.env` hoac `service-account.json` len git
- ❌ Dat Firebase Rules `.read: true, .write: true`
- ❌ De `JWT_SECRET_KEY` trong hoac don gian
- ❌ Set `ALLOWED_ORIGINS = ["*"]` trong production

---

## Kien Truc He Thong

```
+-------------+    +--------------+    +------------------+
|   Browser   |<-->|   Firebase   |<-->|   Judge Server   |
|  (Frontend) |    |  Realtime DB |    |   (Python)       |
|             |    | Rules v3.0   |    |                  |
| index.html  |    |  problems/   |    |  +------------+  |
| solve.html  |    |  public_lb/  |    |  | Compiler   |  |
| rank.html   |    |  submissions/|    |  +------------+  |
| history.html|    |  ai_requests/|    |  +------------+  |
| ...         |    |  users/      |    |  | AI Service |  |
+-------------+    +--------------+    |  +------------+  |
      |                                |  +------------+  |
      |            /api/stats          |  | Flask API  |  |
      +--------- Backend API -------->|  +------------+  |
                                       +------------------+
```

---

## Xu Ly Su Co Thuong Gap

### 1. "Permission denied" khi doc du lieu

> Kiem tra nguoi dung da dang nhap chua, va trang dang doc dung node chua.
> VD: rank.html phai doc `public_leaderboard`, khong phai `users`.

### 2. Bang xep hang trong

> Chua co du lieu trong `public_leaderboard`.
> Chay script khoi tao (xem VAN_HANH.md muc 5.3) hoac nop bai de Backend tu cap nhat.

### 3. AI Mentor khong phan hoi

> Kiem tra backend da chay chua: `python backend/judge.py`
> Kiem tra `.env` co `DEEPSEEK_API_KEY` hoac `GROK_API_KEY`.

### 4. Cham bai khong ra ket qua

> Kiem tra judge server chay chua.
> Kiem tra compiler da cai chua (g++, javac).
> Xem log: `tail -f logs/judge_*.log`

### 5. JWT het han sau khi restart

> Set `JWT_SECRET_KEY` co dinh trong `.env` thay vi de trong.

---

## Lo Trinh Phat Trien

### Da hoan thanh

- [x] Kien truc backend modular (Flask + Services)
- [x] He thong cham diem da ngon ngu (Python, C++, Java, Pascal)
- [x] AI Mentor tich hop DeepSeek/Grok
- [x] Giao dien Cyberpunk UI hoan chinh
- [x] Dang nhap Email / Google / GitHub
- [x] Kho bai tap voi phan loai do kho
- [x] Phong thi co bam gio
- [x] Bang xep hang (public_leaderboard - an toan)
- [x] Lich su nop bai + xem lai code (chi cua minh)
- [x] Tai lieu hoc tap & Video bai giang
- [x] Chat chung realtime (validate danh tinh)
- [x] Dashboard ca nhan
- [x] Firebase config tap trung
- [x] **Firebase Security Rules v3.0** (security hardened)
- [x] **JWT bao mat** (bắt buoc set key)
- [x] **CORS han che** (chi production + localhost)
- [x] **Rate limit** (chong spam nop bai)
- [x] **AI Guard** (bat buoc dang nhap)
- [x] **public_leaderboard** (leaderboard an toan)
- [x] **API /api/stats** (thong ke cong khai an toan)

### Ke hoach toi

- [ ] Ho tro them ngon ngu: C, JavaScript, Go, Rust
- [ ] Redis Queue cho xu ly bat dong bo
- [ ] Docker hoa toan bo he thong
- [ ] Phat hien dao van (Plagiarism Check)
- [ ] Server-side rate limiting (Flask-Limiter)
- [ ] Mobile App (React Native)
- [ ] Monaco Editor (syntax highlighting)
- [ ] Analytics dashboard cho giao vien

---

## Dong Gop

Chung toi rat hoan nghenh moi dong gop tu cong dong!

1. **Fork** repository
2. Tao branch moi: `git checkout -b feature/ten-tinh-nang`
3. Commit changes: `git commit -m 'Them tinh nang X'`
4. Push: `git push origin feature/ten-tinh-nang`
5. Tao **Pull Request**

---

## Giay Phep

Duoc phan phoi duoi giay phep **MIT License**.

---

<p align="center">
  <strong>Made with love by NEO Judge Team</strong>
</p>

<p align="center">
  <sub>Phien ban 3.0 | Cap nhat 06/2026 | Security Hardened</sub>
</p>
