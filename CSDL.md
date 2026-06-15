# Cơ Sở Dữ Liệu — NEO Online Judge

> Tài liệu mô tả toàn bộ cấu trúc cơ sở dữ liệu của hệ thống NEO Online Judge.
> **Phiên bản:** 3.0 | **Cập nhật:** 06/2026 | **Trạng thái:** Production — Đã kiểm tra bảo mật

---

## 1. Tổng Quan

Hệ thống sử dụng **Firebase Realtime Database** làm cơ sở dữ liệu chính.

| Thông tin | Giá trị |
|-----------|---------|
| **Project ID** | `gtsv2-a93c5` |
| **Database URL** | `https://gtsv2-a93c5-default-rtdb.firebaseio.com` |
| **Kiểu CSDL** | NoSQL (JSON tree) |
| **Xác thực** | Firebase Authentication |
| **Region** | us-central1 (mặc định) |
| **Security Rules** | Đã deploy v3.0 — Phân quyền chi tiết theo từng node |

---

## 2. Sơ Đồ Cây Dữ Liệu

```
gtsv2-a93c5-default-rtdb/
│
├── users/                              # [NODE] Thông tin người dùng (chỉ đọc chính mình)
│   └── {uid}/
│       ├── email: "nguyenvana@gmail.com"
│       ├── display_name: "Nguyen Van A"
│       ├── role: "student" | "teacher"
│       ├── avatar: "https://ui-avatars.com/..."
│       ├── score: 1250
│       ├── problems_solved: 15
│       ├── join_date: "2025-01-15T10:30:00Z"
│       └── last_login: "2025-01-20T08:00:00Z"
│
├── public_leaderboard/                 # [NODE] Điểm xếp hạng công khai (ai cũng đọc được)
│   └── {uid}/                          # UID dùng làm key, KHÔNG trả về cho Frontend
│       ├── display_name: "Nguyen Van A"
│       ├── avatar: "https://..."
│       ├── score: 1250
│       ├── problems_solved: 15
│       └── updated_at: "2026-06-15T..."
│
├── problems/                           # [NODE] Bài tập (công khai — ai cũng đọc được)
│   └── {problem_id}/
│       ├── title: "Tong Hai So"
│       ├── description: "Cho hai so nguyen a va b..."
│       ├── level: "Easy"              # Easy | Medium | Hard
│       ├── difficulty: "De"           # Hien thi tieng Viet
│       ├── example_input: "3 5"
│       ├── example_output: "8"
│       ├── tutorial_vid: ""           # YouTube video ID
│       ├── author: "teacher@gmail.com"
│       └── testcases: [
│           {"input": "3 5", "output": "8"},
│           {"input": "0 0", "output": "0"},
│           {"input": "-1 1", "output": "0"}
│       ]
│
├── submissions/                        # [NODE] Bài nộp (luyện tập)
│   └── {submission_id}/               # Chỉ đọc được bài của chính mình hoặc teacher
│       ├── uid: "abc123..."
│       ├── problem_id: "bai01"
│       ├── name: "Nguyen Van A"
│       ├── code: "print(sum(map(int, input().split())))"
│       ├── language: "python"
│       ├── status: "pending" | "completed" | "error"
│       ├── score: 100
│       ├── message: "Passed 3/3 test cases."
│       └── timestamp: 1705000000000
│
├── contest_submissions/                # [NODE] Bài nộp (phòng thi)
│   └── {submission_id}/               # Cấu trúc tương tự submissions + contest_id
│
├── contests/                           # [NODE] Phòng thi (yêu cầu đăng nhập)
│   └── {contest_id}/
│       ├── title: "Thi thu giua ky"
│       ├── description: "Bai kiem tra 45 phut"
│       ├── created_by: "teacher@gmail.com"
│       ├── duration_minutes: 45
│       ├── start_time: 1705000000000
│       ├── is_active: true
│       ├── problems: { "bai01": true, ... }
│       └── participants: { uid: {...}, ... }
│
├── ai_requests/                        # [NODE] Yêu cầu AI Mentor
│   └── {request_id}/                  # Chỉ đọc được request của chính mình hoặc teacher
│       ├── uid: "abc123..."
│       ├── name: "Nguyen Van A"
│       ├── code: "print('hello')"
│       ├── problem_desc: "..."
│       ├── status: "pending" | "processing" | "completed" | "error"
│       ├── response: "Phan hoi tu AI"
│       └── timestamp: 1705000000000
│
├── documents/                          # [NODE] Tài liệu học tập (yêu cầu đăng nhập)
├── videos/                             # [NODE] Video bài giảng (yêu cầu đăng nhập)
└── global_chat/                        # [NODE] Chat chung (yêu cầu đăng nhập)
    └── {message_id}/
        ├── name: "Nguyen Van A"         # Được validate phải khớp display_name của UID
        ├── text: "Chao moi nguoi!"
        ├── role: "student"              # Được validate phải khớp role của UID
        └── timestamp: 1705000000000
```

---

## 3. Security Rules v3.0 (Hiện Tại)

File: [`database.rules.json`](database.rules.json)

```json
{
  "rules": {
    ".read": false,
    ".write": false,

    "users": {
      "$uid": {
        ".read": "auth != null && ($uid === auth.uid || root.child('users/' + auth.uid + '/role').val() === 'teacher')",
        ".write": "auth != null && (auth.uid === $uid || root.child('users/' + auth.uid + '/role').val() === 'teacher')",
        "role": {
          ".validate": "(!data.exists() && newData.val() === 'student') || (data.exists() && newData.val() === data.val()) || root.child('users/' + auth.uid + '/role').val() === 'teacher'"
        },
        "score": {
          ".validate": "..."
        }
      }
    },

    "public_leaderboard": {
      ".read": true,
      ".write": false
    },

    "problems": {
      ".read": true,
      ".write": "auth != null && root.child('users/' + auth.uid + '/role').val() === 'teacher'"
    },

    "submissions": {
      ".indexOn": ["uid"],
      "$submission_id": {
        ".read": "auth != null && (data.child('uid').val() === auth.uid || root.child('users/' + auth.uid + '/role').val() === 'teacher')",
        ".write": "auth != null && !data.exists()",
        ".validate": "newData.child('uid').val() === auth.uid && newData.child('status').val() === 'pending'"
      }
    },

    "global_chat": {
      ".read": "auth != null",
      "$message_id": {
        ".write": "auth != null && !data.exists()",
        ".validate": "newData.child('name').val() === root.child('users/' + auth.uid + '/display_name').val() && newData.child('role').val() === root.child('users/' + auth.uid + '/role').val()"
      }
    }
  }
}
```

### Nguyên tắc bảo mật áp dụng

| Node | Ai đọc | Ai ghi |
|------|--------|--------|
| `users/{uid}` | Chính mình + Teacher | Chính mình (không sửa role/score) + Teacher |
| `public_leaderboard` | Tất cả (public) | **Chỉ Backend** qua Admin SDK |
| `problems` | Tất cả (public) | Chỉ Teacher |
| `submissions/$id` | Chính mình + Teacher | Chỉ tạo mới, không sửa |
| `contest_submissions/$id` | Chính mình + Teacher | Chỉ tạo mới, không sửa |
| `ai_requests/$id` | Chính mình + Teacher | Chỉ tạo mới với status=pending |
| `global_chat/$id` | Đăng nhập | Đăng nhập + validate name/role |
| `documents`, `videos` | Đăng nhập | Chỉ Teacher |
| `contests` | Đăng nhập | Chỉ Teacher |

---

## 4. Luồng Ghi Dữ Liệu

### 4.1. Luồng nộp bài & cập nhật Leaderboard

```
Người dùng
   │
   ▼
Frontend (solve.html)
   │
   ├── Kiểm tra đăng nhập (currentUser != null)
   ├── Rate-limit: không cho nộp quá 1 lần / 5 giây
   ├── Ghi vào submissions/ { uid, problem_id, code, status: "pending" }
   │
   ▼
Backend (judge.py) — Admin SDK bypass rules
   │
   ├── Polling: phát hiện pending submissions
   ├── Đọc problems/{id}/testcases
   ├── Biên dịch code
   ├── Chạy test cases
   ├── Ghi kết quả: submissions/{id} { status: "completed", score }
   │
   └── Cập nhật public_leaderboard/{uid} { display_name, score, problems_solved }
```

### 4.2. Luồng chat — Chống giả mạo danh tính

```
Người dùng gửi tin nhắn
   │
   ▼
Firebase Database Rules kiểm tra:
   ├── name trong tin nhắn === users/{uid}/display_name
   └── role trong tin nhắn === users/{uid}/role
   
Nếu không khớp → Firebase TỰ ĐỘNG từ chối
```

---

## 5. Indexing

Firebase Realtime Database yêu cầu khai báo index cho các query `orderByChild`:

```json
"submissions": {
  ".indexOn": ["uid"]
},
"contest_submissions": {
  ".indexOn": ["uid"]
}
```

Điều này giúp query lịch sử nộp bài (`orderByChild('uid').equalTo(uid)`) chạy hiệu quả thay vì quét toàn bộ.

---

## 6. Backup & Restore

```bash
# Export toàn bộ database
firebase database:export --project gtsv2-a93c5 backup.json

# Import lại
firebase database:import --project gtsv2-a93c5 backup.json
```

> **Lưu ý:** Nên backup định kỳ trước khi thay đổi rules hoặc cấu trúc data.

---

## 7. Cấp Quyền Giáo Viên

Chỉ có thể làm qua **Backend Python** (Admin SDK) hoặc **Firebase Console** trực tiếp — không thể tự nâng quyền từ Frontend.

```python
from firebase_admin import db
db.reference(f'users/{USER_UID}').update({"role": "teacher"})
```

---

> **Tài liệu được tạo:** 01/2025
> **Phiên bản CSDL:** 3.0 (Security Hardened)
> **Cập nhật lần cuối:** 06/2026
> **Dự án:** NEO Online Judge
