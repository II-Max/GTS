# 📘 VẬN HÀNH HỆ THỐNG NEO ONLINE JUDGE

> Tài liệu hướng dẫn toàn diện về cấu trúc, vận hành và quản trị hệ thống NEO Online Judge.

---

## 📋 MỤC LỤC

- [1. Tổng Quan Hệ Thống](#1-tổng-quan-hệ-thống)
- [2. Cấu Trúc Dự Án](#2-cấu-trúc-dự-án)
- [3. Luồng Hoạt Động](#3-luồng-hoạt-động)
- [4. Cách Vận Hành](#4-cách-vận-hành)
- [5. Quản Trị Dữ Liệu](#5-quản-trị-dữ-liệu)
- [6. Cấu Trúc Firebase Database](#6-cấu-trúc-firebase-database)
- [7. Xử Lý Sự Cố Thường Gặp](#7-xử-lý-sự-cố-thường-gặp)
- [8. Bảo Trì & Nâng Cấp](#8-bảo-trì--nâng-cấp)

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
│       │            │            │            │            │       │
│       └────────────┴────────────┴────────────┴────────────┘       │
│                      Firebase SDK (JS)                            │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                   ┌────────────▼────────────┐
                   │                         │
                   │   FIREBASE REALTIME     │
                   │      DATABASE           │
                   │   (Google Cloud)        │
                   │                         │
                   └────────────┬────────────┘
                                │
                   ┌────────────▼────────────┐
                   │                         │
                   │   JUDGE SERVER          │
                   │   (Python Backend)      │
                   │                         │
                   │  ┌───────────────────┐  │
                   │  │ Flask API Server  │  │
                   │  │ (Auth Sync, v.v.) │  │
                   │  └────────┬──────────┘  │
                   │           │             │
                   │  ┌────────▼──────────┐  │
                   │  │ Judge Engine      │  │
                   │  │ (Compiler +       │  │
                   │  │  Test Runner)     │  │
                   │  └────────┬──────────┘  │
                   │           │             │
                   │  ┌────────▼──────────┐  │
                   │  │ AI Mentor Service │  │
                   │  │ (Grok API /       │  │
                   │  │  OpenAI)          │  │
                   │  └───────────────────┘  │
                   │                         │
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
| **AI Mentor** | Grok API (xAI) — tương thích OpenAI format |
| **Compiler** | g++ (C++), gcc (C), javac (Java), Node.js (JS), Python |
| **Code Editor** | Textarea với syntax highlighting (Monaco sẵn sàng) |

### 1.3. Tính năng chính

- ✅ **Kho bài tập** — Duyệt, tìm kiếm, lọc bài tập theo độ khó
- ✅ **Code Editor** — Soạn thảo code, chọn ngôn ngữ, nộp bài
- ✅ **Chấm điểm tự động** — Biên dịch, chạy test case, tính điểm
- ✅ **AI Mentor** — Gợi ý sửa lỗi thông minh từ Grok/OpenAI
- ✅ **Phòng thi** — Thi đấu trực tuyến, bảng xếp hạng theo thời gian thực
- ✅ **Lịch sử** — Xem lại các lần nộp bài, code đã nộp
- ✅ **Bảng xếp hạng** — Hall of Fame toàn hệ thống
- ✅ **Tài liệu học tập** — Thư viện PDF, tài liệu online
- ✅ **Video bài giảng** — Kho video YouTube tích hợp
- ✅ **Chat chung** — Kênh thảo luận toàn hệ thống
- ✅ **Phân quyền** — Giáo viên (teacher) / Học sinh (student)

---

## 2. CẤU TRÚC DỰ ÁN

```
NEO-ONLINE-JUDGE/
│
├── setup/                        # 🛠️ Cung cu cai dat
│   ├── setup_system.py           # Script kiem tra he thong
│   ├── Dockerfile                # Docker build
│   ├── docker-compose.yml        # Docker compose
│   └── scripts/                  # Cac script phu tro
│
├── backend/                      # 🧠 Backend Python
│   ├── app.py                    # Ứng dụng chính (JudgeApplication)
│   ├── judge.py                  # Entry point — khởi động backend
│   ├── config/                   # ⚙️ Cấu hình
│   │   ├── settings.py           # Settings từ .env
│   │   └── logging.py            # Logging system
│   ├── core/                     # Core engine
│   │   ├── compiler.py           # Biên dịch đa ngôn ngữ
│   │   └── judge.py              # Engine chấm điểm
│   ├── models/                   # Data models
│   │   └── submission.py         # Submission model
│   ├── services/                 # Services
│   │   ├── firebase_service.py   # Firebase operations
│   │   └── ai_service.py         # AI Mentor (Grok API)
│   └── routes/                   # API routes
│       └── auth_routes.py        # Auth API
│
├── frontend/                     # 🌐 Frontend (Web) cho AI Agent & Người dùng
│   ├── index.html                # Trang chủ
│   ├── login.html                # Đăng nhập / Đăng ký
│   ├── problems.html             # Kho bài tập
│   ├── solve.html                # Soạn thảo code + nộp bài
│   ├── contest.html              # Danh sách phòng thi
│   ├── contest_room.html         # Phòng thi
│   ├── history.html              # Lịch sử nộp bài
│   ├── rank.html                 # Bảng xếp hạng
│   ├── documents.html            # Thư viện tài liệu
│   ├── videos.html               # Video bài giảng
│   ├── about.html                # Giới thiệu
│   ├── guide.html                # Hướng dẫn cài đặt
│   │
│   ├── css/
│   │   └── neo-design.css        # Hệ thống thiết kế Neo
│   │
│   └── js/
│       ├── firebase-config.js    # 🔥 Cấu hình Firebase CHUNG
│       └── firebase-auth-check.js# Kiểm tra đăng nhập tự động
│
├── logs/                         # 📝 Log files
└── KEY/                          # Tài nguyên
```

---

## 3. LUỒNG HOẠT ĐỘNG

### 3.1. Luồng người dùng (Frontend)

```
1. NGƯỜI DÙNG truy cập website
       │
       ▼
2. TRANG CHỦ (index.html) → Giới thiệu
       │
       ▼
3. ĐĂNG NHẬP (login.html)
   ├── Email + Mật khẩu
   ├── Google (Gmail)
   └── GitHub
       │
       ▼
4. KHO BÀI TẬP (problems.html)
   ├── Dashboard: điểm, hạng, biểu đồ
   ├── Lọc: Tất cả / Dễ / TB / Khó
   ├── Tìm kiếm bài tập
   └── Random bài ngẫu nhiên
       │
       ▼
5. SOẠN THẢO (solve.html?id=bai01)
   ├── Xem đề bài, input/output mẫu
   ├── Chọn ngôn ngữ (Python/C++/Java/Pascal)
   ├── Viết code
   ├── Nhấn "Chấm bài" → gửi lên Firebase
   └── Nhấn "AI Gợi Ý" → gọi AI Mentor
```

### 3.2. Luồng chấm bài (Backend)

```
1. NGƯỜI DÙNG nộp bài trên solve.html
       │
       ▼
2. Firebase ghi submission {status: "pending"}
       │
       ▼
3. JUDGE SERVER (backend/judge.py) polling mỗi 1.5 giây
       │
       ▼
4. Phát hiện submission mới
       │
       ▼
5. BIÊN DỊCH (compiler.py)
   ├── Python → chạy trực tiếp
   ├── C++ → g++ biên dịch
   ├── Java → javac biên dịch
   └── Pascal → chạy trực tiếp
       │
       ▼
6. CHẤM ĐIỂM (backend/core/judge.py - JudgeEngine)
   ├── Chạy từng test case
   ├── So sánh output
   └── Tính % điểm
       │
       ▼
7. GHI KẾT QUẢ vào Firebase
   ├── status: "completed"
   ├── score: 100/0/xxx
   └── message: chi tiết
```

### 3.3. Luồng AI Mentor

```
1. NGƯỜI DÙNG nhấn "AI Gợi Ý"
       │
       ▼
2. Gửi request lên Firebase (ai_requests)
   ├── code
   ├── problem_desc
   └── status: "pending"
       │
       ▼
3. JUDGE SERVER phát hiện request
       │
       ▼
4. AI SERVICE (ai_service.py)
   ├── Gọi Grok API (hoặc OpenAI)
   ├── Phân tích code
   └── Trả về nhận xét + gợi ý
       │
       ▼
5. GHI PHẢN HỒI vào Firebase
   ├── status: "completed"
   └── response: nội dung phân tích
       │
       ▼
6. FRONTEND hiển thị modal AI
```

---

## 4. CÁCH VẬN HÀNH

### 4.1. Yêu cầu hệ thống

- **Python** 3.9+
- **Node.js** 18+ (cho firebase hosting, optional)
- **g++** (cho C++)
- **gcc** (cho C, optional)
- **JDK** 11+ (cho Java, optional)

### 4.2. Cài đặt dependencies

```bash
# Cài thư viện Python
pip install -r requirements.txt

# Nội dung requirements.txt:
#   firebase-admin
#   python-dotenv
#   requests
#   flask
#   flask-cors
#   python-json-logger
```

### 4.3. Cấu hình .env

```bash
# Tạo file .env từ template
cp .env.example .env

# Sau đó điền các giá trị:
```

| Biến | Mô tả | Bắt buộc |
|------|-------|---------|
| `CRED_PATH` | Đường dẫn file service-account.json | ✅ |
| `DB_URL` | URL Firebase Realtime Database | ✅ |
| `OPENAI_API_KEY` | API key OpenAI (hoặc Grok) | ✅ (cho AI) |
| `AI_MODEL` | Model AI (mặc định: gpt-4o-mini) | ❌ |
| `JUDGE_TIMEOUT` | Timeout chấm bài (giây) | ❌ |
| `POLL_INTERVAL` | Tần suất polling (giây) | ❌ |
| `HOST` | Host backend API | ❌ |
| `PORT` | Cổng backend API | ❌ |

### 4.4. Khởi động hệ thống

#### Bước 1: Chuẩn bị Firebase

1. Vào [Firebase Console](https://console.firebase.google.com)
2. Chọn dự án `gtsv2-a93c5`
3. Vào **Project settings** → **Service accounts**
4. Generate key → lưu file `service-account.json` vào thư mục gốc
5. Vào **Realtime Database**, copy URL `https://gtsv2-a93c5-default-rtdb.firebaseio.com`
6. Vào **Authentication** → **Sign-in method** → Bật Email, Google, GitHub

#### Bước 2: Chạy Judge Server

```bash
# Cách 1: Chạy trực tiếp
python backend/judge.py

# Cách 2: Chạy module
python -m backend.app
```

Server sẽ in ra:
```
╔══════════════════════════════════════════════════╗
║              NEO ONLINE JUDGE v2.0               ║
║          Online Code Judge + AI Mentor           ║
╠══════════════════════════════════════════════════╣
║  Mode:          Independent Scoring              ║
║  AI Model:      gpt-4o-mini                      ║
║  API Server:    0.0.0.0:5000                     ║
║  Poll Interval: 1.5s                             ║
║  Judge Timeout: 3s                               ║
╚══════════════════════════════════════════════════╝
```

#### Bước 3: Mở Frontend

```bash
# Cách 1: Mở file trực tiếp
# Mở frontend/index.html trong trình duyệt

# Cách 2: Dùng web server
python -m http.server 8000
# Truy cập http://localhost:8000/frontend/
```

#### Bước 4: Deploy lên Firebase Hosting (tùy chọn)

```bash
npm install -g firebase-tools
firebase login
firebase init hosting
# Chọn frontend/ làm thư mục
firebase deploy
```

---

## 5. QUẢN TRỊ DỮ LIỆU

### 5.1. Thêm bài tập mới

**Cách 1: Qua giao diện web (dành cho giáo viên)**

1. Đăng nhập với tài khoản **giáo viên** (teacher)
2. Vào **Kho bài tập** → nhấn **"Thêm bài"**
3. Điền thông tin:
   - **Mã bài (ID)**: VD: `bai01`, `tong-hai-so`
   - **Tên bài tập**: VD: "Tính tổng hai số"
   - **Mô tả đề bài**: Nội dung bài toán
   - **Độ khó**: Dễ / Trung bình / Khó
   - **Input mẫu / Output mẫu**: Ví dụ minh họa
   - **Test cases (JSON)**: Danh sách test case

**Cách 2: Qua Firebase Console**

1. Vào Firebase Console → **Realtime Database**
2. Thêm node `problems/{id}` với cấu trúc:

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
      "tutorial_vid": "dQw4w9WgXcQ",
      "author": "teacher@gmail.com",
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

### 5.2. Cấp quyền giáo viên

Để cấp quyền giáo viên (teacher) cho một tài khoản:

1. Vào Firebase Console → **Realtime Database**
2. Tìm node `users/{uid_của_người_dùng}`
3. Thêm/sửa: `"role": "teacher"`
4. Hoặc dùng script:

```python
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("service-account.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://gtsv2-a93c5-default-rtdb.firebaseio.com'
})

# Thay UID bằng UID của tài khoản cần nâng quyền
USER_UID = "abc123..."
db.reference(f'users/{USER_UID}').update({"role": "teacher"})
print("✅ Đã cấp quyền giáo viên!")
```

### 5.3. Thêm tài liệu học tập

**Dành cho giáo viên:**
1. Vào **Tài liệu** → nhấn **"Upload tài liệu"**
2. Nhập tên, link (Google Drive/PDF), loại file, mô tả

**Hoặc qua Firebase Console:**
```json
{
  "documents": {
    "-key123": {
      "title": "Đề cương Python cơ bản",
      "url": "https://drive.google.com/file/d/...",
      "type": "PDF",
      "desc": "Tài liệu ôn tập Python cho người mới",
      "date": "15/1/2025",
      "author": "teacher@gmail.com"
    }
  }
}
```

### 5.4. Thêm video bài giảng

**Dành cho giáo viên:**
1. Vào **Video** → nhấn **"Thêm video mới"**
2. Nhập: tiêu đề, YouTube ID, mô tả

### 5.5. Tạo phòng thi

Tạo node `contests/{id}` với cấu trúc:

```json
{
  "contests": {
    "contest01": {
      "title": "Thi thử giữa kỳ",
      "description": "Bài kiểm tra 45 phút",
      "created_by": "teacher@gmail.com",
      "duration_minutes": 45,
      "start_time": 1705000000000,
      "is_active": true,
      "problems": {
        "bai01": true,
        "bai02": true,
        "bai03": true
      },
      "participants": {
        "uid_cua_hoc_sinh": {
          "name": "Nguyễn Văn A",
          "score": 85,
          "finished": false,
          "started_at": 1705000200000
        }
      }
    }
  }
}
```

---

## 6. CẤU TRÚC FIREBASE DATABASE

```
gtsv2-a93c5-default-rtdb/
│
├── users/{uid}                    # 👤 Người dùng
│   ├── email: "user@gmail.com"
│   ├── display_name: "Nguyễn Văn A"
│   ├── role: "student" | "teacher"
│   ├── avatar: "https://..."
│   ├── score: 0
│   ├── problems_solved: 0
│   ├── join_date: "2025-01-15T..."
│   └── last_login: "2025-01-15T..."
│
├── problems/{id}                  # 📝 Bài tập
│   ├── title: "Tính tổng hai số"
│   ├── description: "..."
│   ├── level: "Easy"|"Medium"|"Hard"
│   ├── difficulty: "Dễ"|"Trung bình"|"Khó"
│   ├── example_input: "3 5"
│   ├── example_output: "8"
│   ├── tutorial_vid: "dQw4w9WgXcQ" (optional)
│   ├── author: "teacher@gmail.com"
│   └── testcases: [
│       {"input": "3 5", "output": "8"},
│       ...
│   ]
│
├── submissions/{id}               # 📤 Bài nộp (luyện tập)
│   ├── uid: "user_uid"
│   ├── problem_id: "bai01"
│   ├── code: "print(input()...)"
│   ├── language: "python"
│   ├── status: "pending"|"completed"
│   ├── score: 100
│   ├── message: "Passed 3/3 test cases."
│   ├── name: "Nguyễn Văn A"
│   └── timestamp: 1705000000000
│
├── contest_submissions/{id}       # 📤 Bài nộp (phòng thi)
│   (Cấu trúc tương tự submissions + contest_id)
│
├── contests/{id}                  # 🏆 Phòng thi
│   ├── title: "Thi thử giữa kỳ"
│   ├── description: "..."
│   ├── created_by: "teacher@gmail.com"
│   ├── duration_minutes: 45
│   ├── start_time: 1705000000000
│   ├── is_active: true
│   ├── problems: { "bai01": true, ... }
│   └── participants: { uid: {...}, ... }
│
├── ai_requests/{id}               # 🤖 AI Mentor requests
│   ├── uid: "user_uid"
│   ├── name: "Nguyễn Văn A"
│   ├── code: "..."
│   ├── problem_desc: "..."
│   ├── status: "pending"|"processing"|"completed"|"error"
│   ├── response: "✅ Code của bạn..."
│   └── timestamp: 1705000000000
│
├── documents/{id}                 # 📚 Tài liệu học tập
│   ├── title: "Đề cương Python"
│   ├── url: "https://drive..."
│   ├── type: "PDF"
│   ├── desc: "..."
│   ├── date: "15/1/2025"
│   └── author: "teacher@gmail.com"
│
├── videos/{id}                    # 🎥 Video bài giảng
│   ├── title: "Hướng dẫn..."
│   ├── youtube_id: "dQw4w9WgXcQ"
│   ├── desc: "..."
│   ├── author: "teacher@gmail.com"
│   └── timestamp: 1705000000000
│
└── global_chat/{id}               # 💬 Chat chung
    ├── name: "Nguyễn Văn A"
    ├── text: "Chào mọi người!"
    ├── role: "student"
    └── timestamp: 1705000000000
```

---

## 7. XỬ LÝ SỰ CỐ THƯỜNG GẶP

### 7.1. "This domain is not authorized" khi đăng nhập

```
Nguyên nhân: Domain chưa được thêm vào Authorized domains của Firebase Auth.
Cách khắc phục:
1. Vào Firebase Console → Authentication → Settings
2. Thêm domain vào "Authorized domains"
3. Ví dụ: localhost, gtsv2-a93c5.web.app
```

### 7.2. AI Mentor không phản hồi

```
Nguyên nhân 1: Thiếu API key
Cách khắc phục:
1. Kiểm tra .env có OPENAI_API_KEY chưa
2. Hoặc thêm GROK_API_KEY vào .env

Nguyên nhân 2: Backend chưa chạy
Cách khắc phục:
- Chạy: python backend/judge.py

Nguyên nhân 3: Hết quota API
Cách khắc phục:
- Kiểm tra billing trên OpenAI/Grok dashboard
```

### 7.3. Chấm bài không ra kết quả

```
Nguyên nhân 1: Judge server chưa chạy
Cách khắc phục:
- Chạy: python backend/judge.py

Nguyên nhân 2: Thiếu compiler
Cách khắc phục:
- Python: đã có sẵn
- C++: cài g++ (sudo apt install g++ / brew install gcc)
- Java: cài JDK

Nguyên nhân 3: Submission lưu ở contest_submissions nhưng sever
chỉ check submissions
Cách khắc phục: Server tự động kiểm tra cả 2 bảng.
```

### 7.4. Avatar không hiển thị

```
Nguyên nhân: photoURL null hoặc lỗi
Giải pháp: Hệ thống tự động fallback về ui-avatars.com.
Nếu vẫn lỗi → kiểm tra kết nối mạng.
```

### 7.5. Lỗi "Không tìm thấy đề bài"

```
Nguyên nhân: Problem ID sai hoặc chưa có trong database.
Cách khắc phục:
1. Kiểm tra Firebase Console → problems có dữ liệu chưa
2. Thêm bài tập mới (xem mục 5.1)
```

### 7.6. Logs để debug

```bash
# Xem log realtime
tail -f logs/judge_*.log

# Xem log lỗi
tail -f logs/errors_*.log
```

---

## 8. BẢO TRÌ & NÂNG CẤP

### 8.1. Cập nhật frontend

```bash
# Deploy lại lên Firebase Hosting
firebase deploy --only hosting
```

### 8.2. Cập nhật backend

```bash
# Dừng server cũ (Ctrl+C)
# Pull code mới
git pull

# Cài dependencies mới
pip install -r requirements.txt

# Khởi động lại
python backend/judge.py
```

### 8.3. Sao lưu dữ liệu Firebase

```bash
# Cài firebase-tools
npm install -g firebase-tools

# Export database
firebase database:export --project gtsv2-a93c5 backup.json
```

### 8.4. Xóa dữ liệu test

Để tránh đầy database, nên xóa định kỳ:
- `ai_requests` cũ (request test)
- `submissions` test

### 8.5. Kiểm tra log thường xuyên

Kiểm tra `logs/` để phát hiện sớm lỗi hệ thống:

```bash
# Kiểm tra lỗi
grep -i error logs/judge_*.log | tail -20

# Kiểm tra dung lượng logs
du -sh logs/
```

### 8.6. Tối ưu hóa

- Nếu nhiều người dùng cùng lúc, tăng `POLL_INTERVAL` lên 2-3s
- Nếu cần realtime hơn, thiết lập Redis queue
- Nếu chấm C++/Java nhiều, đảm bảo server có đủ RAM

---

## 📌 TÓM TẮT NHANH

```bash
# 1. Chạy backend (luôn cần để chấm bài + AI)
python backend/judge.py

# 2. Mở frontend
# Mở frontend/index.html trong trình duyệt

# 3. Kiểm tra logs
tail -f logs/judge_*.log

# 4. Deploy hosting
firebase deploy --only hosting

# 5. Sao lưu dữ liệu
firebase database:export --project gtsv2-a93c5 backup.json
```

---

> **Phiên bản:** 2.0 | **Cập nhật:** 01/2025 | **Hỗ trợ:** phamvanchung2k7@gmail.com
