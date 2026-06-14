
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
  <img src="https://img.shields.io/badge/AI-Grok%20%7C%20OpenAI-brightgreen?style=flat&logo=openai" alt="AI">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat" alt="Status">
</p>

---

## MỤC LỤC

- [Giới Thiệu](#-giới-thiệu)
- [Tính Năng Chính](#-tính-năng-chính)
- [Công Nghệ Sử Dụng](#-công-nghệ-sử-dụng)
- [Cấu Trúc Dự Án](#-cấu-trúc-dự-án)
- [Hướng Dẫn Cài Đặt Nhanh](#-hướng-dẫn-cài-đặt-nhanh)
- [Hướng Dẫn Cài Đặt Chi Tiết](#-hướng-dẫn-cài-đặt-chi-tiết)
- [Hướng Dẫn Sử Dụng](#-hướng-dẫn-sử-dụng)
- [Cấu Trúc Firebase Database](#-cấu-trúc-firebase-database)
- [Hệ Thống AI Mentor](#-hệ-thống-ai-mentor)
- [Kiến Trúc Hệ Thống](#-kiến-trúc-hệ-thống)
- [Xử Lý Sự Cố](#-xử-lý-sự-cố-thường-gặp)
- [Lộ Trình Phát Triển](#-lộ-trình-phát-triển)
- [Đóng Góp](#-đóng-góp)
- [Giấy Phép](#-giấy-phép)

---

## Giới Thiệu

**NEO Online Judge** là một nền tảng học lập trình tương tác toàn diện được thiết kế dành riêng cho người dùng Việt Nam. Dự án kết hợp:

- **Chấm bài tự động** — Biên dịch & chạy test cases, cho điểm tức thì
- **AI Mentor thông minh** — Phân tích code, gợi ý sửa lỗi mà không đưa đáp án
- **Môi trường thi đấu** — Phòng thi trực tuyến có bấm giờ
- **Giao diện Cyberpunk** — UI hiện đại, bắt mắt với hiệu ứng neon

Dự án phù hợp cho:
- **Trường học** — Làm công cụ dạy và học lập trình
- **Câu lạc bộ** — Tổ chức thi đấu, luyện tập
- **Cá nhân** — Tự học và rèn luyện kỹ năng coding

---

## Tính Năng Chính

### Cho Học Sinh

| Tính năng | Mô tả |
|-----------|-------|
| Kho bài tập | Hàng trăm bài toán phân loại theo 3 cấp độ: Dễ - Trung bình - Khó |
| Code Editor | Soạn thảo code trực tuyến với đa ngôn ngữ (Python, C++, Java, Pascal) |
| Chấm điểm tức thì | Nộp bài và nhận kết quả ngay lập tức |
| AI Mentor | Gợi ý sửa lỗi thông minh từ AI (Grok/OpenAI) |
| Dashboard cá nhân | Theo dõi điểm số, tiến độ học tập qua biểu đồ |
| Bảng xếp hạng | So tài với các lập trình viên khác |
| Tài liệu & Video | Thư viện tài liệu PDF, video bài giảng YouTube |
| Chat chung | Kênh thảo luận toàn hệ thống |
| Random bài | Tính năng chọn bài ngẫu nhiên để thử thách |

### Cho Giáo Viên / Quản Trị Viên

| Tính năng | Mô tả |
|-----------|-------|
| Thêm bài tập | Tạo bài toán mới kèm test cases qua giao diện (cần quyền teacher) |
| Tổ chức thi | Tạo phòng thi, quản lý thời gian, theo dõi kết quả |
| Quản lý nội dung | Upload tài liệu, video bài giảng |
| Giám sát học sinh | Theo dõi tiến độ, lịch sử nộp bài |

### Đặc Điểm Nổi Bật

- **UI Cyberpunk** — Giao diện tối giản, neon, hiện đại
- **Hỗ trợ tiếng Việt** — Toàn bộ nội dung được bản địa hóa
- **Real-time** — Cập nhật kết quả chấm điểm tức thời
- **Responsive** — Hoạt động tốt trên desktop, tablet, mobile
- **Bảo mật** — Firebase Authentication & phân quyền

---

## Công Nghệ Sử Dụng

### Frontend

| Công nghệ | Mục đích |
|-----------|----------|
| **HTML5 / CSS3** | Cấu trúc & giao diện (Neo Design System) |
| **JavaScript (Vanilla)** | Tương tác & cập nhật real-time |
| **Firebase JS SDK v8** | Kết nối Realtime Database & Auth |
| **Chart.js** | Biểu đồ thống kê |
| **Font Awesome 6** | Icon |

### Backend

| Công nghệ | Mục đích | Phiên bản |
|-----------|----------|-----------|
| **Python** | Backend Judge Server | 3.9+ |
| **Flask** | HTTP API Server | 3.x |
| **Firebase Admin SDK** | Quản lý dữ liệu từ backend | Latest |
| **Grok API / OpenAI API** | AI Mentor | Grok 3 / GPT-4o-mini |
| **g++ / gcc / javac** | Trình biên dịch C++, C, Java | Theo hệ thống |

### Infrastructure

| Thành phần | Chi tiết |
|-----------|----------|
| **Database** | Firebase Realtime Database |
| **Authentication** | Firebase Auth (Email, Google, GitHub) |
| **Hosting** | Firebase Hosting (hoặc local server) |

---

## Cấu Trúc Dự Án

```
NEO-ONLINE-JUDGE/
│
├── setup/                            # Cong cu cai dat
│   ├── setup_system.py               # Script kiem tra he thong
│   ├── Dockerfile                    # Docker build
│   ├── docker-compose.yml            # Docker compose
│   └── scripts/                      # Cac script phu tro
├── .env                              # Bien moi truong
├── service-account.json              # Firebase Admin key (can tu tao)
├── requirements.txt                  # Python dependencies
├── VAN_HANH.md                       # Tai lieu van hanh
│
├── backend/                          # Backend Python
│   ├── app.py                        # Ung dung chinh (JudgeApplication)
│   ├── judge.py                      # ENTRY POINT - Khoi dong backend
│   ├── config/
│   │   ├── settings.py               # Settings tu .env
│   │   └── logging.py                # Logging system
│   ├── core/                         # Core engine
│   │   ├── compiler.py               # Bien dich da ngon ngu
│   │   └── judge.py                  # Engine cham diem
│   ├── models/
│   │   └── submission.py             # Data model
│   ├── services/
│   │   ├── firebase_service.py       # Firebase operations
│   │   └── ai_service.py             # AI Mentor (Grok/OpenAI)
│   └── routes/
│       └── auth_routes.py            # API Auth
│
├── frontend/                         # Frontend (Web) cho AI Agent va Nguoi dung
│   ├── index.html                    # Trang chu
│   ├── login.html                    # Dang nhap / Dang ky
│   ├── problems.html                 # Kho bai tap
│   ├── solve.html                    # Soan thao code
│   ├── contest.html                  # Danh sach phong thi
│   ├── contest_room.html             # Phong thi
│   ├── history.html                  # Lich su nop bai
│   ├── rank.html                     # Bang xep hang
│   ├── documents.html                # Tai lieu hoc tap
│   ├── videos.html                   # Video bai giang
│   ├── about.html                    # Gioi thieu
│   └── guide.html                    # Huong dan
│   ├── css/
│   │   └── neo-design.css            # Neo Design System
│   └── js/
│       ├── firebase-config.js        # Firebase config CHUNG
│       └── firebase-auth-check.js    # Auth check tu dong
│
├── logs/                             # Log files
└── KEY/                              # Tai nguyen phu (optional)
```

---

## Huong Dan Cai Dat Nhanh

```bash
# 1. Clone du an
git clone https://github.com/II-Max/NEO-ONLINE-JUDGE.git
cd NEO-ONLINE-JUDGE

# 2. Cai Python dependencies
pip install -r requirements.txt

# 3. Tao file .env tu mau (xem chi tiet ben duoi)

# 4. Dat file service-account.json vao thu muc goc

# 5. Chay backend judge
python backend/judge.py

# 6. Mo frontend (trinh duyet)
# MacOS:
open frontend/index.html
# Windows:
start frontend/index.html
# Hoac dung Python HTTP server:
python -m http.server 8000
# Truy cap: http://localhost:8000/frontend/
```

---

## Huong Dan Cai Dat Chi Tiet

### 1. Clone & Cai Dependencies

```bash
git clone https://github.com/II-Max/NEO-ONLINE-JUDGE.git
cd NEO-ONLINE-JUDGE
pip install -r requirements.txt
```

**Noi dung requirements.txt:**
```
firebase-admin>=6.0.0
python-dotenv>=1.0.0
requests>=2.31.0
flask>=3.0.0
flask-cors>=4.0.0
python-json-logger>=2.0.0
```

### 2. Cau Hinh Firebase

#### Buoc A: Lay Firebase Config cho Frontend

1. Vao [Firebase Console](https://console.firebase.google.com)
2. Chon du an `gtsv2-a93c5` (hoac tao moi)
3. Vao **Project settings** > **General** > **Your apps** > **Web app**
4. Copy `firebaseConfig` object
5. Cap nhat vao file `frontend/js/firebase-config.js`:

```javascript
// frontend/js/firebase-config.js
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "your-project.firebaseapp.com",
  databaseURL: "https://your-project-default-rtdb.firebaseio.com",
  projectId: "your-project",
  storageBucket: "your-project.firebasestorage.app",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.database();
```

#### Buoc B: Lay Service Account cho Backend

1. Vao **Project settings** > **Service accounts**
2. Chon **Firebase Admin SDK** > **Generate new private key**
3. Luu file `service-account.json` vao thu muc goc du an

#### Buoc C: Bat Authentication

1. Vao **Authentication** > **Sign-in method**
2. Bat cac provider: **Email/Password**, **Google**, **GitHub**
3. Them domain cua ban vao **Authorized domains** (VD: `localhost`, `gtsv2-a93c5.web.app`)

#### Buoc D: Cau hinh Realtime Database Rules

Vao **Realtime Database** > **Rules** > Dan rules:

```json
{
  "rules": {
    ".read": true,
    ".write": true,
    "users": {
      ".read": true,
      "$uid": {
        ".write": "$uid === auth.uid || root.child('users/'+$uid+'/role').val() === 'teacher'"
      }
    }
  }
}
```

### 3. Cau Hinh AI (Grok/OpenAI)

Tao file `.env` trong thu muc goc:

```env
# === Firebase ===
CRED_PATH=service-account.json
DB_URL=https://gtsv2-a93c5-default-rtdb.firebaseio.com

# === AI (Grok API - khuyen dung) ===
# Dang ky tai: https://console.x.ai
GROK_API_KEY=grok-xxx...

# === AI (OpenAI API - thay the) ===
# OPENAI_API_KEY=sk-xxx...
# AI_MODEL=gpt-4o-mini

# === Judge Engine ===
JUDGE_TIMEOUT=3
POLL_INTERVAL=1.5

# === Server ===
HOST=0.0.0.0
PORT=5000

# === Logging ===
LOG_LEVEL=INFO
```

### 4. Chay Judge Server

```bash
python backend/judge.py
```

**Output thanh cong:**
```
╔══════════════════════════════════════════════════╗
║              NEO ONLINE JUDGE v2.0               ║
║          Online Code Judge + AI Mentor           ║
╠══════════════════════════════════════════════════╣
║  Mode:          Independent Scoring              ║
║  AI Model:      grok-3-mini                      ║
║  API Server:    0.0.0.0:5000                     ║
║  Poll Interval: 1.5s                             ║
║  Judge Timeout: 3s                               ║
╚══════════════════════════════════════════════════╝
```

### 5. Mo Frontend

```bash
# Cach 1: Mo file truc tiep
# MacOS:
open frontend/index.html
# Windows:
start frontend/index.html

# Cach 2: Dung Python HTTP server (khuyen dung)
python -m http.server 8000
# Truy cap: http://localhost:8000/frontend/

# Cach 3: Deploy len Firebase Hosting
npm install -g firebase-tools
firebase login
firebase init hosting
# Chon frontend/ lam thu muc
firebase deploy --only hosting
```

---

## Huong Dan Su Dung

### Cho Hoc Sinh

#### Giai Bai Tap

1. **Dang nhap** > Vao `login.html` bang Email, Google hoac GitHub
2. **Vao Kho bai tap** > `problems.html` > Chon bai toan
3. **Viet code** > Trong `solve.html`, chon ngon ngu, viet code
4. **Nop bai** > Nhan **"Cham bai"** > Nhan ket qua tuc thi:
   - **100/100** > Hoan thanh xuat sac!
   - **> 0** > Dung mot phan
   - **0/100** > Sai hoac loi bien dich

#### Su Dung AI Mentor

1. Viet code cua ban
2. Nhan **"AI Goi Y"** (khong hoat dong trong phong thi)
3. AI se phan tich code va dua ra:
   - **Diem tot** > Khen ngoi nhung gi ban lam dung
   - **Van de** > Chi ra loi sai
   - **Goi y** > Huong dan cach sua (KHONG dua dap an)
   - **Hoc them** > Goi y kien thuc can on tap

#### Theo Doi Tien Do

- **Dashboard** > Xem tong diem, hang, bieu do tien do
- **Lich su** > Xem lai toan bo lan nop bai va code da viet
- **Bang xep hang** > So sanh diem so voi moi nguoi

#### Tham Gia Thi Dau

1. Vao **"Phong thi"** > Chon cuoc thi dang mo
2. Click **"THAM GIA"** > Bat dau lam bai trong thoi gian quy dinh
3. AI Mentor se bi vo hieu hoa trong phong thi
4. Ket thuc thi > Xem ket qua tren bang xep hang

### Cho Giao Vien / Quan Tri Vien

#### Them Bai Tap Moi

**Cach 1: Qua giao dien web (de dang)**

1. Dang nhap voi tai khoan da duoc cap quyen **giao vien**
2. Vao **Kho bai tap** > Click **"Them bai"**
3. Dien day du thong tin: ma bai, ten, mo ta, do kho, test cases
4. Nhan **"Luu bai tap"**

**Cach 2: Qua Firebase Console (nhanh)**

```json
{
  "problems": {
    "bai01": {
      "title": "Tinh tong hai so",
      "description": "Nhap vao hai so nguyen a va b. In ra tong cua chung.",
      "level": "Easy",
      "example_input": "3 5",
      "example_output": "8",
      "tutorial_vid": "dQw4w9WgXcQ",
      "testcases": [
        {"input": "3 5", "output": "8"},
        {"input": "0 0", "output": "0"},
        {"input": "-1 1", "output": "0"},
        {"input": "100 200", "output": "300"}
      ]
    }
  }
}
```

#### Tao Phong Thi

Them node `contests/{id}`:

```json
{
  "contests": {
    "contest01": {
      "title": "Thi thu giua ky",
      "description": "Bai kiem tra 45 phut",
      "created_by": "teacher@gmail.com",
      "duration_minutes": 45,
      "start_time": 1705000000000,
      "is_active": true,
      "problems": {
        "bai01": true,
        "bai02": true,
        "bai03": true
      }
    }
  }
}
```

#### Cap Quyen Giao Vien

De nang quyen giao vien cho mot tai khoan:

```javascript
// Trong Firebase Console > Database
users / {uid cua giao vien} / role: "teacher"
```

Hoac chay script Python:

```python
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("service-account.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://gtsv2-a93c5-default-rtdb.firebaseio.com'
})

USER_UID = "uid cua tai khoan can nang quyen"
db.reference(f'users/{USER_UID}').update({"role": "teacher"})
print("Da cap quyen giao vien!")
```

---

## Cau Truc Firebase Database

```
gtsv2-a93c5-default-rtdb/
│
├── users/{uid}                      # Nguoi dung
│   ├── email: "user@gmail.com"
│   ├── display_name: "Nguyen Van A"
│   ├── role: "student" | "teacher"
│   ├── avatar: "https://..."
│   └── ...
│
├── problems/{id}                    # Bai tap
│   ├── title: "Tinh tong hai so"
│   ├── description: "..."
│   ├── level: "Easy" | "Medium" | "Hard"
│   ├── testcases: [{input, output}, ...]
│   └── tutorial_vid: "youtube_id"
│
├── submissions/{id}                 # Bai nop (luyen tap)
│   ├── uid, problem_id, code, language
│   ├── status: "pending" | "completed"
│   ├── score: 100
│   └── message: "Passed 3/3 test cases."
│
├── contest_submissions/{id}         # Bai nop (phong thi)
│   ├── ... (tuong tu submissions + contest_id)
│
├── contests/{id}                    # Phong thi
│   ├── title, description, duration_minutes
│   ├── is_active, problems: {...}
│   └── participants: {...}
│
├── ai_requests/{id}                 # Yeu cau AI
│   ├── uid, code, problem_desc
│   └── status: "pending" | "completed"
│
├── documents/{id}                   # Tai lieu
├── videos/{id}                      # Video
└── global_chat/{id}                 # Chat chung
```

---

## He Thong AI Mentor

AI Mentor la tinh nang dac biet giup hoc sinh hoc lap trinh hieu qua hon.

### Cach hoat dong

1. Hoc sinh viet code va nhan **"AI Goi Y"**
2. Frontend ghi request vao Firebase (`ai_requests/{id}`)
3. Judge Server phat hien va xu ly
4. Goi **Grok API** (xAI) hoac **OpenAI API**
5. AI phan tich code dua tren system prompt:
   - Khen ngoi diem tot
   - Chi ra loi sai
   - Goi y cach sua (KHONG dua dap an)
   - Goi y kien thuc
6. Ket qua duoc ghi lai vao Firebase
7. Frontend hien thi trong modal AI

### Cau hinh AI

File `backend/services/ai_service.py`:

```python
# Ho tro ca Grok API va OpenAI API
# Grok API (khuyen dung - co goi free)
API_URL = "https://api.x.ai/v1/chat/completions"
# Hoac OpenAI
# API_URL = "https://api.openai.com/v1/chat/completions"

# Model mac dinh
AI_MODEL = "grok-3-mini"  # Hoac "gpt-4o-mini"
```

---

## Kien Truc He Thong

```
+-------------+    +--------------+    +------------------+
|   Browser   |<-->|   Firebase   |<-->|   Judge Server   |
|  (Frontend) |    |  Realtime DB |    |   (Python)       |
|             |    |              |    |                  |
| index.html  |    |  problems/   |    |  +------------+  |
| problems    |    |  submissions/|    |  | Compiler   |  |
| solve.html  |    |  ai_requests/|    |  | (g++/javac)|  |
| contest     |    |  users/      |    |  +------------+  |
| rank.html   |    |  contests/   |    |  +------------+  |
| ...         |    |  ...         |    |  | AI Service |  |
+-------------+    +--------------+    |  | (Grok/Open |  |
                                       |  |   AI)      |  |
                                       |  +------------+  |
                                       |  +------------+  |
                                       |  | Flask API  |  |
                                       |  | (Auth Sync)|  |
                                       |  +------------+  |
                                       +------------------+
```

---

## Xu Ly Su Co Thuong Gap

### 1. "This domain is not authorized" khi dang nhap

> Vao Firebase Console > Authentication > Settings
> Them domain cua ban vao "Authorized domains"
> VD: localhost, gtsv2-a93c5.web.app

### 2. AI Mentor khong phan hoi

> Kiem tra .env co OPENAI_API_KEY hoac GROK_API_KEY chua
> Kiem tra backend da chay chua: python backend/judge.py
> Kiem tra billing dashboard cua OpenAI/Grok
> Xem log: tail -f logs/judge_*.log

### 3. Cham bai khong ra ket qua

> Kiem tra judge server da chay chua: python backend/judge.py
> Kiem tra compiler da cai chua:
>   - Python: built-in
>   - C++: which g++
>   - Java: which javac
> Kiem tra test cases co trong Firebase khong

### 4. Avatar khong hien thi

> He thong tu dong fallback ve ui-avatars.com neu khong co avatar.
> Kiem tra ket noi mang hoac thu dang xuat dang nhap lai.

### 5. Khong tim thay bai tap

> Vao Firebase Console > Realtime Database > problems/
> Neu chua co du lieu, them bai tap moi (xem huong dan o tren)

---

## Lo Trinh Phat Trien

### Da hoan thanh

- [x] Kien truc backend modular (Flask + Services)
- [x] He thong cham diem da ngon ngu (Python, C++, Java, Pascal)
- [x] AI Mentor tich hop Grok/OpenAI
- [x] Giao dien Cyberpunk UI hoan chinh
- [x] Dang nhap Email / Google / GitHub
- [x] Kho bai tap voi phan loai do kho
- [x] Phong thi co bam gio
- [x] Bang xep hang toan he thong
- [x] Lich su nop bai + xem lai code
- [x] Tai lieu hoc tap & Video bai giang
- [x] Chat chung realtime
- [x] Dashboard ca nhan voi bieu do
- [x] Firebase config tap trung (firebase-config.js)
- [x] Auth check tu dong (firebase-auth-check.js)

### Ke hoach toi

- [ ] Ho tro them ngon ngu: C, JavaScript, Go, Rust
- [ ] Redis Queue cho xu ly bat dong bo
- [ ] Docker hoa toan bo he thong
- [ ] Phat hien dao van (Plagiarism Check)
- [ ] Goi y bai tap thong minh dua trinh do
- [ ] Mobile App (React Native)
- [ ] Code editor voi syntax highlighting (Monaco Editor)
- [ ] Che do toi/sang
- [ ] Multiple file submissions
- [ ] Analytics dashboard cho giao vien

---

## Dong Gop

Chung toi rat hoan nghenh moi dong gop tu cong dong!

### Cach dong gop

1. **Fork** repository
2. Tao branch moi: `git checkout -b feature/ten-tinh-nang`
3. Commit changes: `git commit -m 'Them tinh nang X'`
4. Push: `git push origin feature/ten-tinh-nang`
5. Tao **Pull Request**

### Tieu chuan code

- Tuan theo PEP 8 (Python)
- Su dung ten bien co y nghia
- Them comment cho logic phuc tap
- Kiem tra truoc khi PR

---

## Giay Phep

Duoc phan phoi duoi giay phep **MIT License**.

```
MIT License

Copyright (c) 2025 NEO Judge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## Lien He & Ho Tro

- **Email:** phamvanchung2k7@gmail.com
- **Bao loi:** [GitHub Issues](https://github.com/II-Max/NEO-ONLINE-JUDGE/issues)
- **Thao luan:** [GitHub Discussions](https://github.com/II-Max/NEO-ONLINE-JUDGE/discussions)
- **Website:** [gtsv2-a93c5.web.app](https://gtsv2-a93c5.web.app)

---

## Cam On

- **Firebase** > Backend as a Service tuyet voi
- **xAI (Grok)** > AI Mentor mien phi, chat luong cao
- **OpenAI** > AI Engine manh me
- **Cong dong** > Feedback & Contributions

---

<p align="center">
  <strong>Made with love by NEO Judge Team</strong>
</p>

<p align="center">
  <sub>Phien ban 2.0 | Cap nhat 01/2025</sub>
</p>
