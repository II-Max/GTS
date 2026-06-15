# 📘 VẬN HÀNH HỆ THỐNG NEO ONLINE JUDGE

> Tài liệu hướng dẫn toàn diện về cấu trúc, vận hành và quản trị hệ thống NEO Online Judge.
> **Phiên bản:** 3.0 | **Cập nhật:** 06/2026 | **Trạng thái:** Production — Security Hardened

---

## 📋 MỤC LỤC

- [1. Tổng Quan Hệ Thống](#1-tổng-quan-hệ-thống)
- [2. Cấu Trúc Dự Án](#2-cấu-trúc-dự-án)
- [3. Luồng Hoạt Động](#3-luồng-hoạt-động)
- [4. Cách Vận Hành](#4-cách-vận-hành)
- [5. Quản Trị Dữ Liệu](#5-quản-trị-dữ-liệu)
- [6. Cấu Trúc Firebase Database](#6-cấu-trúc-firebase-database)
- [7. Bảo Mật Hệ Thống](#7-bảo-mật-hệ-thống)
- [8. Xử Lý Sự Cố Thường Gặp](#8-xử-lý-sự-cố-thường-gặp)
- [9. Bảo Trì & Nâng Cấp](#9-bảo-trì--nâng-cấp)

---

## 1. TỔNG QUAN HỆ THỐNG

### 1.1. Kiến trúc tổng thể

```
┌───────────────────────────────────────────────────────────────────┐
│                    TRÌNH DUYỆT NGƯỜI DÙNG                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐ ┌────────┐  │
│  │Problem   │ │Solve     │ │Contest   │ │Rank       │ │...     │  │
│  │List      │ │Editor    │ │Room      │ │Leaderboard│ │        │  │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬──────┘ └───┬────┘  │
│       └────────────┴────────────┴────────────┴────────────┘       │
│                      Firebase SDK (JS)                            │
└───────────────────────┬───────────────────────────────────────────┘
                        │
           ┌────────────▼────────────┐
           │   FIREBASE REALTIME     │
           │      DATABASE           │
           │   (Google Cloud)        │
           │   Security Rules v3.0   │
           └────────────┬────────────┘
                        │
           ┌────────────▼────────────┐
           │   JUDGE SERVER          │
           │   (Python Backend)      │
           │  ┌──────────────────┐   │
           │  │ Flask API Server │   │
           │  │ /api/stats       │   │
           │  │ /api/auth/*      │   │
           │  └────────┬─────────┘   │
           │  ┌────────▼─────────┐   │
           │  │ Judge Engine     │   │
           │  │ (Compiler + Test)│   │
           │  └────────┬─────────┘   │
           │  ┌────────▼─────────┐   │
           │  │ AI Mentor Service│   │
           │  │ (DeepSeek/Grok)  │   │
           │  └──────────────────┘   │
           └─────────────────────────┘
```

### 1.2. Công nghệ sử dụng

| Thành phần | Công nghệ |
|-----------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) |
| **UI Framework** | Thiết kế riêng (Neo Design System) |
| **Database** | Firebase Realtime Database |
| **Authentication** | Firebase Auth (Email, Google, GitHub) |
| **Backend Judge** | Python 3.9+ (Flask) |
| **AI Mentor** | DeepSeek API / Grok API — tương thích OpenAI format |
| **Compiler** | g++ (C++), gcc (C), javac (Java), Node.js (JS), Python |
| **Security** | Firebase Security Rules v3.0, JWT Auth, CORS hạn chế |

### 1.3. Tính năng chính

- ✅ **Kho bài tập** — Duyệt, tìm kiếm, lọc bài tập theo độ khó
- ✅ **Code Editor** — Soạn thảo code, chọn ngôn ngữ, nộp bài
- ✅ **Chấm điểm tự động** — Biên dịch, chạy test case, tính điểm
- ✅ **AI Mentor** — Gợi ý sửa lỗi thông minh từ DeepSeek/Grok
- ✅ **Phòng thi** — Thi đấu trực tuyến, bảng xếp hạng theo thời gian thực
- ✅ **Lịch sử** — Xem lại các lần nộp bài, code đã nộp
- ✅ **Bảng xếp hạng** — Hall of Fame toàn hệ thống (public_leaderboard)
- ✅ **Tài liệu học tập** — Thư viện PDF, tài liệu online
- ✅ **Video bài giảng** — Kho video YouTube tích hợp
- ✅ **Chat chung** — Kênh thảo luận toàn hệ thống
- ✅ **Phân quyền** — Giáo viên (teacher) / Học sinh (student)
- ✅ **Thống kê** — API `/api/stats` trả số lượng bài/user/lượt nộp

---

## 2. CẤU TRÚC DỰ ÁN

```
NEO-ONLINE-JUDGE/
│
├── .env                              # ⚙️ Biến môi trường (KHÔNG commit lên git)
├── .env.example                      # Mẫu cấu hình
├── service-account.json              # Firebase Admin key (KHÔNG commit lên git)
├── database.rules.json               # Firebase Security Rules v3.0
├── firebase.json                     # Firebase CLI config (hosting + database)
├── requirements.txt                  # Python dependencies
│
├── backend/                          # 🧠 Backend Python
│   ├── app.py                        # Ứng dụng chính (JudgeApplication + Flask API)
│   ├── judge.py                      # Entry point — khởi động backend
│   ├── config/
│   │   ├── settings.py               # Settings từ .env (JWT, CORS, AI)
│   │   └── logging.py                # Logging system
│   ├── core/
│   │   ├── compiler.py               # Biên dịch đa ngôn ngữ
│   │   └── judge.py                  # Engine chấm điểm
│   ├── models/
│   │   └── submission.py             # Submission model
│   ├── services/
│   │   ├── firebase_service.py       # Firebase operations + public_leaderboard
│   │   ├── auth_service.py           # Auth, JWT, phân quyền
│   │   └── ai_service.py             # AI Mentor (DeepSeek/Grok API)
│   └── routes/
│       └── auth_routes.py            # Auth API + Stats endpoint
│
├── frontend/                         # 🌐 Frontend (Static Web)
│   ├── index.html                    # Trang chủ (stats từ /api/stats)
│   ├── login.html                    # Đăng nhập / Đăng ký
│   ├── problems.html                 # Kho bài tập
│   ├── solve.html                    # Code editor + nộp bài (rate-limited)
│   ├── contest.html                  # Danh sách phòng thi
│   ├── contest_room.html             # Phòng thi
│   ├── history.html                  # Lịch sử nộp bài (chỉ của mình)
│   ├── rank.html                     # Bảng xếp hạng (từ public_leaderboard)
│   ├── documents.html                # Thư viện tài liệu
│   ├── videos.html                   # Video bài giảng
│   ├── about.html                    # Giới thiệu
│   ├── guide.html                    # Hướng dẫn
│   ├── css/
│   │   └── neo-design.css            # Neo Design System
│   └── js/
│       ├── firebase-config.js        # Cấu hình Firebase CHUNG
│       └── firebase-auth-check.js    # Kiểm tra đăng nhập tự động
│
└── logs/                             # 📝 Log files
```

---

## 3. LUỒNG HOẠT ĐỘNG

### 3.1. Luồng nộp bài (có bảo mật)

```
1. NGƯỜI DÙNG đăng nhập → Có currentUser
   │
   ▼
2. SOLVE.HTML
   ├── Kiểm tra currentUser != null
   ├── Rate-limit: >= 5 giây giữa các lần nộp
   ├── Ghi submissions/{id} { uid, code, status: "pending" }
   │   └── Firebase Rules validate: uid === auth.uid, status === "pending"
   │
   ▼
3. JUDGE SERVER (polling mỗi 1.5s)
   ├── Admin SDK: bypass rules để đọc pending submissions
   ├── Biên dịch + chấm điểm
   ├── Ghi kết quả vào submissions/{id}
   └── Cập nhật public_leaderboard/{uid} { display_name, score, problems_solved }
```

### 3.2. Luồng Bảng Xếp Hạng (an toàn)

```
RANK.HTML đọc từ db.ref('public_leaderboard')
   │
   ├── Node này .read: true — ai cũng đọc được
   ├── Chỉ chứa: display_name, avatar, score, problems_solved
   ├── KHÔNG có email, KHÔNG có code bài nộp
   └── Được Backend tự động cập nhật sau mỗi lần chấm
```

### 3.3. Luồng AI Mentor (có bảo vệ)

```
1. NGƯỜI DÙNG nhấn "AI Gợi Ý"
   │
   ├── Kiểm tra currentUser != null (nếu không → redirect login)
   ├── Kiểm tra không phải contest mode
   ├── Ghi ai_requests/{id} { uid: currentUser.uid, status: "pending" }
   │   └── Firebase Rules validate: uid === auth.uid
   │
   ▼
2. JUDGE SERVER xử lý AI request
   └── Ghi kết quả vào ai_requests/{id}
```

---

## 4. CÁCH VẬN HÀNH

### 4.1. Yêu cầu hệ thống

- **Python** 3.9+
- **Node.js** 18+ (cho firebase CLI)
- **g++** (cho C++)
- **JDK** 11+ (cho Java, tùy chọn)

### 4.2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4.3. Cấu hình .env

```bash
# Tạo file .env từ template
cp .env.example .env
```

| Biến | Mô tả | Bắt buộc |
|------|-------|---------|
| `CRED_PATH` | Đường dẫn file service-account.json | ✅ |
| `DB_URL` | URL Firebase Realtime Database | ✅ |
| `JWT_SECRET_KEY` | Secret key cho JWT token (≥ 32 ký tự ngẫu nhiên) | ✅ |
| `DEEPSEEK_API_KEY` | API key DeepSeek (hoặc Grok) | ✅ (cho AI) |
| `AI_MODEL` | Model AI (mặc định: deepseek-chat) | ❌ |
| `JUDGE_TIMEOUT` | Timeout chấm bài (giây, mặc định: 3) | ❌ |
| `POLL_INTERVAL` | Tần suất polling (giây, mặc định: 1.5) | ❌ |
| `ALLOWED_ORIGINS` | Danh sách domain CORS (mặc định: production + localhost) | ❌ |

> ⚠️ **QUAN TRỌNG:** File `.env` và `service-account.json` PHẢI được thêm vào `.gitignore`. KHÔNG bao giờ commit lên git.

### 4.4. Tạo JWT_SECRET_KEY

```bash
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
# Dán kết quả vào .env
```

### 4.5. Khởi động hệ thống

#### Bước 1: Chuẩn bị Firebase

1. Vào [Firebase Console](https://console.firebase.google.com)
2. Chọn dự án `gtsv2-a93c5`
3. Vào **Project settings** → **Service accounts** → Generate key → lưu `service-account.json`
4. Vào **Authentication** → **Sign-in method** → Bật Email, Google, GitHub
5. Thêm domain vào **Authorized domains**: `localhost`, `gtsv2-a93c5.web.app`

#### Bước 2: Deploy Security Rules

```bash
firebase deploy --only database
```

#### Bước 3: Chạy Judge Server

```bash
python backend/judge.py
```

#### Bước 4: Deploy Frontend

```bash
firebase deploy --only hosting
# Hosting URL: https://gtsv2-a93c5.web.app
```

---

## 5. QUẢN TRỊ DỮ LIỆU

### 5.1. Thêm bài tập mới

**Qua giao diện web (dành cho giáo viên):**
1. Đăng nhập với tài khoản **giáo viên** (teacher)
2. Vào **Kho bài tập** → nhấn **"Thêm bài"**

**Qua Firebase Console:**
```json
{
  "problems": {
    "bai01": {
      "title": "Tính tổng hai số",
      "description": "Nhập vào hai số nguyên a và b. In ra tổng của chúng.",
      "level": "Easy",
      "difficulty": "Dễ",
      "example_input": "3 5",
      "example_output": "8",
      "author": "teacher@gmail.com",
      "testcases": [
        {"input": "3 5", "output": "8"},
        {"input": "0 0", "output": "0"}
      ]
    }
  }
}
```

### 5.2. Cấp quyền giáo viên

> ⚠️ **Bắt buộc** phải thực hiện qua Backend Python hoặc Firebase Console. Học sinh KHÔNG thể tự nâng quyền.

```python
# Script cấp quyền giáo viên
from firebase_admin import db
db.reference(f'users/{USER_UID}').update({"role": "teacher"})
print("Đã cấp quyền giáo viên!")
```

### 5.3. Khởi tạo public_leaderboard

Lần đầu tiên backend chạy, `public_leaderboard` sẽ được tự động cập nhật sau mỗi lần chấm bài. Để khởi tạo dữ liệu có sẵn từ `users`:

```python
from backend.services.firebase_service import FirebaseService
fb = FirebaseService()
fb.initialize()
users = fb.get_data("users") or {}
for uid, u in users.items():
    if isinstance(u, dict) and u.get("score", 0) > 0:
        fb.update_public_leaderboard(
            uid=uid,
            display_name=u.get("display_name", "Unknown"),
            score=u.get("score", 0),
            problems_solved=u.get("problems_solved", 0),
            avatar=u.get("avatar", "")
        )
print("Đã khởi tạo public_leaderboard!")
```

---

## 6. CẤU TRÚC FIREBASE DATABASE

Xem chi tiết tại [`CSDL.md`](CSDL.md).

Node quan trọng nhất:
- `users/{uid}` — Thông tin người dùng (chỉ đọc chính mình)
- `public_leaderboard/{uid}` — Điểm xếp hạng (công khai, an toàn)
- `problems/{id}` — Bài tập (công khai)
- `submissions/{id}` — Bài nộp (chỉ đọc bài của mình)
- `global_chat/{id}` — Chat (validate danh tính)

---

## 7. BẢO MẬT HỆ THỐNG

### 7.1. Các lớp bảo mật đã triển khai

| Lớp | Biện pháp | Trạng thái |
|-----|-----------|-----------|
| **Firebase Rules** | Phân quyền chi tiết theo từng node và từng UID | ✅ v3.0 |
| **Chống lộ source code** | Submission chỉ đọc bởi chính mình hoặc teacher | ✅ |
| **Chống giả mạo chat** | Validate name/role khớp DB khi gửi tin nhắn | ✅ |
| **Chống leo thang quyền** | Học sinh không thể tự sửa role/score | ✅ |
| **JWT Secret** | Key ngẫu nhiên 32 bytes, bắt buộc set trong .env | ✅ |
| **CORS hạn chế** | Chỉ cho phép domain production + localhost | ✅ |
| **Rate Limit** | Client-side: không nộp bài quá 1 lần/5 giây | ✅ |
| **AI Guard** | Bắt buộc đăng nhập để dùng AI Mentor | ✅ |
| **Leaderboard an toàn** | public_leaderboard chỉ chứa tên + điểm | ✅ |
| **Stats API** | Backend tính toán, không lộ data thô | ✅ |

### 7.2. Những gì KHÔNG được làm

- ❌ **KHÔNG** commit `.env` hoặc `service-account.json` lên git
- ❌ **KHÔNG** đặt Firebase Rules về `".read": true, ".write": true`
- ❌ **KHÔNG** để `JWT_SECRET_KEY` là chuỗi đơn giản hoặc để trống
- ❌ **KHÔNG** set `ALLOWED_ORIGINS = ["*"]` trong production

### 7.3. Kiểm tra bảo mật định kỳ

```bash
# Kiểm tra rules hiện tại trên Firebase
firebase database:rules:get --project gtsv2-a93c5

# Re-deploy rules sau khi thay đổi
firebase deploy --only database
```

---

## 8. XỬ LÝ SỰ CỐ THƯỜNG GẶP

### 8.1. "Permission denied" khi đọc dữ liệu

```
Nguyên nhân: Firebase Rules đã được thắt chặt.
Kiểm tra:
1. Người dùng có đăng nhập chưa?
2. Trang đang đọc đúng node chưa? (VD: rank.html phải đọc public_leaderboard)
3. Xem log console trình duyệt để biết node nào bị denied
```

### 8.2. Bảng xếp hạng trống

```
Nguyên nhân: Chưa có dữ liệu trong public_leaderboard.
Cách khắc phục:
1. Chạy script khởi tạo public_leaderboard (xem mục 5.3)
2. Hoặc nộp bài và để Backend tự động cập nhật
```

### 8.3. AI Mentor không phản hồi

```
Nguyên nhân 1: Backend chưa chạy
  → Chạy: python backend/judge.py

Nguyên nhân 2: Thiếu API key
  → Kiểm tra .env có DEEPSEEK_API_KEY hoặc GROK_API_KEY

Nguyên nhân 3: Hết quota API
  → Kiểm tra billing trên dashboard của DeepSeek/Grok
```

### 8.4. Chấm bài không ra kết quả

```
1. Judge server chưa chạy → python backend/judge.py
2. Thiếu compiler:
   - C++: cài g++
   - Java: cài JDK
3. Xem logs: tail -f logs/judge_*.log
```

### 8.5. Lỗi JWT token hết hạn

```
Nguyên nhân: Server restart tạo JWT_SECRET_KEY mới.
Cách khắc phục: Set JWT_SECRET_KEY cố định trong .env
```

### 8.6. Xem Logs

```bash
tail -f logs/judge_*.log   # Log realtime
grep -i error logs/judge_*.log | tail -20  # Chỉ xem lỗi
```

---

## 9. BẢO TRÌ & NÂNG CẤP

### 9.1. Cập nhật frontend

```bash
firebase deploy --only hosting
```

### 9.2. Cập nhật security rules

```bash
# Sau khi sửa database.rules.json
firebase deploy --only database
```

### 9.3. Sao lưu dữ liệu Firebase

```bash
firebase database:export --project gtsv2-a93c5 backup_$(date +%Y%m%d).json
```

### 9.4. Xóa dữ liệu test

Để tránh đầy database, xóa định kỳ:
- `ai_requests` cũ hơn 30 ngày
- `submissions` test của tài khoản thử nghiệm

### 9.5. Tối ưu hóa hiệu suất

- Nếu nhiều người dùng cùng lúc → tăng `POLL_INTERVAL` lên 2-3s
- Nếu cần realtime hơn → thiết lập Redis queue (`USE_QUEUE=true`)
- Nếu chấm C++/Java nhiều → đảm bảo server có đủ RAM (≥ 2GB)

---

## 📌 TÓM TẮT NHANH

```bash
# 1. Chạy backend (luôn cần để chấm bài + AI)
python backend/judge.py

# 2. Deploy hosting
firebase deploy --only hosting

# 3. Deploy database rules (sau khi thay đổi)
firebase deploy --only database

# 4. Xem logs
tail -f logs/judge_*.log

# 5. Sao lưu dữ liệu
firebase database:export --project gtsv2-a93c5 backup.json

# 6. Tạo JWT secret mới
python -c "import secrets; print(secrets.token_hex(32))"
```

---

> **Phiên bản:** 3.0 | **Cập nhật:** 06/2026 | **Hỗ trợ:** phamvanchung2k7@gmail.com
