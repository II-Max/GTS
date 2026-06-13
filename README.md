# NEO ONLINE JUDGE v2.0

**Hệ thống chấm bài tập code online tích hợp AI Mentor — sẵn sàng cho cuộc nâng cấp lớn.**

---

## Tổng Quan

NEO ONLINE JUDGE là nền tảng học lập trình tương tác, cho phép học sinh nộp bài code và nhận điểm tự động, kèm nhận xét từ AI Mentor.

### Kiến Trúc Mới (v2.0)

```
NEO-ONLINE-JUDGE/
│
├── judge.py                  # Entry point (giữ nguyên để tương thích)
├── backend/                  # Backend modular
│   ├── __init__.py
│   ├── app.py                # Ứng dụng chính (JudgeApplication)
│   ├── core/
│   │   ├── compiler.py       # Biên dịch đa ngôn ngữ (Python, C++, C, Java, JS)
│   │   └── judge.py          # Engine chấm điểm
│   ├── models/
│   │   └── submission.py     # Data models (Submission, Problem, AIRequest)
│   └── services/
│       ├── firebase_service.py  # Firebase operations
│       └── ai_service.py        # OpenAI AI Mentor
│
├── config/
│   ├── settings.py           # Cấu hình từ .env
│   └── logging.py            # Logging system
│
├── public/                   # Frontend (sẽ được nâng cấp)
├── tests/                    # Unit tests
├── scripts/                  # Utility scripts
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

### Công Nghệ

| Thành Phần | Công Nghệ |
|-----------|-----------|
| Backend | Python 3.11+, modular architecture |
| Database | Firebase Realtime Database |
| AI Mentor | OpenAI GPT-4o-mini (có thể đổi model) |
| Queue | Redis (optional) |
| Container | Docker & Docker Compose |
| Frontend | HTML/CSS/JS (sẽ nâng cấp lên React) |

---

## 🚀 Chuẩn Bị Cho Nâng Cấp

Dự án đã được tổ chức lại thành kiến trúc module sẵn sàng cho các nâng cấp tiếp theo:

### ✅ Đã Hoàn Thành

- [x] Module hóa backend (core, models, services)
- [x] Quản lý cấu hình qua `.env`
- [x] Logging có cấu trúc (JSON, rotating files)
- [x] Clean architecture, dễ mở rộng
- [x] Xóa tài liệu cũ, chuẩn bị viết lại

### 🔜 Kế Hoạch Nâng Cấp

| Giai Đoạn | Nội Dung | Ưu Tiên |
|-----------|---------|---------|
| 1 | **Nâng cấp Frontend** (React + Monaco Editor) | Cao |
| 2 | **Authentication** (Firebase Auth) | Cao |
| 3 | **Queue System** (Redis) | Trung |
| 4 | **Multi AI Models** | Trung |
| 5 | **Plagiarism Detection** | Thấp |
| 6 | **Mobile App** | Thấp |

---

## Cài Đặt & Chạy

### Yêu Cầu
- Python 3.11+
- g++ (cho C++)
- Node.js (cho JavaScript - tùy chọn)
- JDK (cho Java - tùy chọn)

### Quick Start

```bash
# 1. Cài dependencies
pip install -r requirements.txt

# 2. Tạo file .env từ mẫu
cp .env.example .env
# Sau đó điền OPENAI_API_KEY, DB_URL, CRED_PATH

# 3. Đặt service-account.json vào thư mục gốc

# 4. Chạy server
python judge.py
```

### Docker

```bash
docker-compose up -d
```

---

## API Firebase

### Database Structure

```
/ (root)
├── users/{uid}/
├── problems/{id}/
│   ├── title, description, level
│   └── testcases/[{input, output}]
├── submissions/{id}/
│   ├── user_id, problem_id, code
│   ├── language, status, score, message
├── contest_submissions/{id}/
├── contests/{id}/
└── ai_requests/{id}/
    ├── user_id, problem_desc, code
    └── status, response
```

---

## Liên Hệ

- GitHub Issues: https://github.com/II-Max/NEO-ONLINE-JUDGE/issues
- Email: phamvanchung2k7@gmail.com
