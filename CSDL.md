# Co So Du Lieu NEO Online Judge

> Tai lieu mo ta toan bo cau truc co so du lieu cua he thong NEO Online Judge.

## 1. Tong Quan

He thong su dung **Firebase Realtime Database** lam co so du lieu chinh.

| Thong tin | Gia tri |
|-----------|---------|
| **Project ID** | `gtsv2-a93c5` |
| **Database URL** | `https://gtsv2-a93c5-default-rtdb.firebaseio.com` |
| **Kieu CSDL** | NoSQL (JSON tree) |
| **Xac thuc** | Firebase Authentication |
| **Region** | us-central1 (mac dinh) |

---

## 2. So Do Cay Du Lieu

```
gtsv2-a93c5-default-rtdb/
│
├── users/                              # [NODE] Thong tin nguoi dung
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
├── problems/                           # [NODE] Bai tap
│   └── {problem_id}/
│       ├── title: "Tong Hai So"
│       ├── description: "Cho hai so nguyen a va b..."
│       ├── level: "Easy"              # Easy | Medium | Hard
│       ├── difficulty: "De"            # Hien thi tieng Viet
│       ├── example_input: "3 5"
│       ├── example_output: "8"
│       ├── tutorial_vid: ""            # YouTube video ID
│       ├── author: "teacher@gmail.com" # Nguoi tao
│       └── testcases: [                # Danh sach test case
│           {"input": "3 5", "output": "8"},
│           {"input": "0 0", "output": "0"},
│           {"input": "-1 1", "output": "0"}
│       ]
│
├── submissions/                        # [NODE] Bai nop (luyen tap)
│   └── {submission_id}/
│       ├── uid: "abc123..."            # Firebase Auth UID
│       ├── problem_id: "bai01"
│       ├── name: "Nguyen Van A"
│       ├── code: "print(sum(map(int, input().split())))"
│       ├── language: "python"
│       ├── status: "pending" | "completed" | "error"
│       ├── score: 100                  # 0 - 100
│       ├── message: "Passed 3/3 test cases."
│       └── timestamp: 1705000000000    # milliseconds
│
├── contest_submissions/                # [NODE] Bai nop (phong thi)
│   └── {submission_id}/
│       ├── uid: "abc123..."
│       ├── problem_id: "bai01"
│       ├── contest_id: "contest01"
│       ├── name: "Nguyen Van A"
│       ├── code: "..."
│       ├── language: "python"
│       ├── status: "pending" | "completed"
│       ├── score: 100
│       ├── message: "Passed 3/3 test cases."
│       └── timestamp: 1705000000000
│
├── contests/                           # [NODE] Phong thi
│   └── {contest_id}/
│       ├── title: "Thi thu giua ky"
│       ├── description: "Bai kiem tra 45 phut"
│       ├── created_by: "teacher@gmail.com"
│       ├── duration_minutes: 45
│       ├── start_time: 1705000000000
│       ├── is_active: true
│       ├── problems: {                 # Danh sach bai thi
│       │   "bai01": true,
│       │   "bai02": true,
│       │   "bai03": true
│       └── }
│       └── participants: {             # Nguoi tham gia
│           "uid_cua_hoc_sinh": {
│               "name": "Nguyen Van A",
│               "score": 85,
│               "finished": false,
│               "started_at": 1705000200000
│           }
│       }
│
├── ai_requests/                        # [NODE] Yeu cau AI Mentor
│   └── {request_id}/
│       ├── uid: "abc123..."
│       ├── name: "Nguyen Van A"
│       ├── code: "print('hello')"
│       ├── problem_desc: "Bai toan yeu cau in ra hello"
│       ├── status: "pending" | "processing" | "completed" | "error"
│       ├── response: "✅ Code cua ban... (phan hoi tu AI)"
│       └── timestamp: 1705000000000
│
├── documents/                          # [NODE] Tai lieu hoc tap
│   └── {document_key}/
│       ├── title: "De cuong Python"
│       ├── url: "https://drive.google.com/file/d/..."
│       ├── type: "PDF"
│       ├── desc: "Tai lieu on tap Python"
│       ├── date: "15/1/2025"
│       └── author: "teacher@gmail.com"
│
├── videos/                             # [NODE] Video bai giang
│   └── {video_key}/
│       ├── title: "Huong dan bai 1"
│       ├── youtube_id: "dQw4w9WgXcQ"
│       ├── desc: "Video huong dan giai bai tap"
│       ├── author: "teacher@gmail.com"
│       └── timestamp: 1705000000000
│
└── global_chat/                        # [NODE] Chat chung
    └── {message_key}/
        ├── name: "Nguyen Van A"
        ├── text: "Chao moi nguoi!"
        ├── role: "student"
        └── timestamp: 1705000000000
```

---

## 3. Chi Tiet Cac Node

### 3.1. users/{uid}

Node nay duoc tao tu dong khi nguoi dung dang nhap lan dau.

| Truong | Kieu | Mo ta | Bat buoc |
|--------|------|-------|----------|
| `email` | string | Email nguoi dung | Yes |
| `display_name` | string | Ten hien thi | Yes |
| `role` | string | `"student"` hoac `"teacher"` | Yes |
| `avatar` | string | URL avatar | No (auto fallback) |
| `score` | number | Tong diem tich luy | No |
| `problems_solved` | number | So bai da giai dung | No |
| `join_date` | string | Ngay tham gia (ISO 8601) | No |
| `last_login` | string | Lan dang nhap cuoi | No |

### 3.2. problems/{problem_id}

Node chua bai tap. `problem_id` la ma duy nhat.

| Truong | Kieu | Mo ta | Bat buoc |
|--------|------|-------|----------|
| `title` | string | Ten bai tap | Yes |
| `description` | string | Noi dung de bai | Yes |
| `level` | string | `Easy`, `Medium`, `Hard` | Yes |
| `difficulty` | string | Hien thi: `De`, `Trung binh`, `Kho` | No |
| `example_input` | string | Input mau | No |
| `example_output` | string | Output mau | No |
| `tutorial_vid` | string | YouTube video ID (optional) | No |
| `author` | string | Email nguoi tao | No |
| `testcases` | array | Danh sach test case | Yes |

**Cau truc testcases:**
```json
"testcases": [
  {"input": "3 5", "output": "8"},
  {"input": "0 0", "output": "0"}
]
```

### 3.3. submissions/{submission_id}

Khi hoc sinh nop bai, he thong tao ban ghi moi.

| Truong | Kieu | Mo ta |
|--------|------|-------|
| `uid` | string | Firebase Auth UID |
| `problem_id` | string | Ma bai tap |
| `name` | string | Ten nguoi dung |
| `code` | string | Ma nguon |
| `language` | string | Ngon ngu: `python`, `cpp`, `java`, `pascal` |
| `status` | string | Trang thai: `pending` -> `completed` |
| `score` | number | Diem 0-100 |
| `message` | string | Chi tiet ket qua |
| `timestamp` | number | Thoi gian nop (ms) |

**Cac trang thai:**
- `pending` -> Dang cho cham
- `completed` -> Da cham xong
- `error` -> Loi he thong

### 3.4. ai_requests/{request_id}

Khi hoc sinh nhan "AI Goi Y".

| Truong | Kieu | Mo ta |
|--------|------|-------|
| `uid` | string | Firebase Auth UID |
| `name` | string | Ten nguoi dung |
| `code` | string | Ma nguon can phan tich |
| `problem_desc` | string | Mo ta bai toan |
| `status` | string | Trang thai: `pending` -> `completed` |
| `response` | string | Phan hoi tu AI (Grok/OpenAI) |
| `timestamp` | number | Thoi gian yeu cau (ms) |

### 3.5. contests/{contest_id}

Phong thi do giao vien tao.

| Truong | Kieu | Mo ta |
|--------|------|-------|
| `title` | string | Ten cuoc thi |
| `description` | string | Mo ta |
| `created_by` | string | Email giao vien |
| `duration_minutes` | number | Thoi gian lam bai (phut) |
| `start_time` | number | Thoi gian bat dau (ms) |
| `is_active` | boolean | Dang mo hay dong |
| `problems` | object | Danh sach bai thi `{"bai01": true}` |
| `participants` | object | Nguoi tham gia |

---

## 4. Quy Tac Firebase Database

### 4.1. Security Rules

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

**Giai thich:**
- Cho phep **doc** toan bo database (de hien thi bai tap, bang xep hang)
- Cho phep **ghi** khi da xac thuc
- **users/{uid}**: Chi user do hoac teacher moi co the ghi

> **Chu y:** Rules tren la co ban cho development. Trong production, can gioi han chat che hon.

### 4.2. Indexing

Firebase Realtime Database tu dong danh index cho cac truong. Khong can cau hinh them.

---

## 5. Luong Ghi Du Lieu

### 5.1. Luong nop bai

```
Nguoi dung
   │
   ▼
Frontend (solve.html)
   │
   ├── Ghi vao submissions/ { status: "pending" }
   │
   ▼
Backend (judge.py)
   │
   ├── Polling: phat hien pending submissions
   ├── Doc problems/{id}/testcases
   ├── Bien dich code
   ├── Chay test cases
   │
   ▼
   └── Ghi ket qua: submissions/{id} { status: "completed", score: 100 }
```

### 5.2. Luong AI Mentor

```
Nguoi dung
   │
   ▼
Frontend (solve.html)
   │
   ├── Ghi vao ai_requests/ { status: "pending" }
   │
   ▼
Backend (judge.py)
   │
   ├── Polling: phat hien pending ai_requests
   ├── Goi Grok/OpenAI API
   │
   ▼
   └── Ghi phan hoi: ai_requests/{id} { status: "completed", response: "..." }
```

### 5.3. Luong dang nhap

```
Nguoi dung
   │
   ▼
Firebase Auth (login.html)
   │
   ├── Dang nhap thanh cong
   │
   ▼
Frontend
   │
   ├── Kiem tra users/{uid} ton tai chua
   ├── Neu chua: tao users/{uid} moi
   ├── Neu co: cap nhat last_login
   │
   ▼
Vao trang chu
```

---

## 6. Cau Hoi Thuong Gap

### Lam sao de xoa du lieu?

Vao **Firebase Console** > **Realtime Database** > Chon node > Click `X` (delete).

### Lam sao de backup?

```bash
# Cai firebase-tools
npm install -g firebase-tools

# Export toan bo database
firebase database:export --project gtsv2-a93c5 backup.json

# Import lai
firebase database:import --project gtsv2-a93c5 backup.json
```

### Tai sao submission bi pending mai?

1. Kiem tra judge server da chay chua: `python judge.py`
2. Kiem tra log: `tail -f logs/judge_*.log`
3. Kiem tra `status` trong Firebase co phai `"pending"` khong

### Lam sao de them truong moi vao database?

Chi can ghi them truong moi vao node bang code hoac Firebase Console. Firebase Realtime Database khong co schema co dinh.

---

## 7. So Sanh Voi Cac Loai CSDL Khac

| Tinh nang | Firebase Realtime DB | MongoDB | MySQL |
|-----------|---------------------|---------|-------|
| Kieu | NoSQL (JSON tree) | NoSQL (Document) | SQL (Quan he) |
| Schema | Khong co dinh | Linh hoat | Co dinh |
| Real-time | ✅ Co san | Can them thu vien | Can them thu vien |
| Truy van | Gioi han (filter/sort) | Manh (aggregation) | Rat manh (JOIN) |
| Authentication | Tich hop san | Can tu xay dung | Can tu xay dung |
| Hosting | Firebase (serverless) | Atlas/MongoDB | RDS/Cloud SQL |
| Gia | Pay-as-you-go | Pay-as-you-go | Fixed/On-demand |

**Tai sao chon Firebase Realtime DB cho du an nay?**
- Tich hop san voi Firebase Authentication
- Cap nhat real-time ma khong can WebSocket
- Khong can quan ly server
- Chi phi thap cho luong nguoi dung vua phai

---

## 8. Danh Sach Bai Tap Hien Tai

| ID | Ten bai | Cap do | So test |
|----|---------|--------|---------|
| bai01 | Tong Hai So | De (Easy) | 10 |
| bai02 | So Chan Hay Le | De (Easy) | 10 |
| bai03 | Kiem Tra So Nguyen To | De (Easy) | 10 |
| bai04 | FizzBuzz | De (Easy) | 10 |
| bai05 | Tong Chu So | De (Easy) | 10 |
| bai06 | Dao Nguoc Chuoi | De (Easy) | 10 |
| bai07 | Kiem Tra Palindrome | De (Easy) | 10 |
| bai08 | Day Fibonacci | De (Easy) | 10 |
| bai09 | Sap Xep Noi Bot | Trung binh (Medium) | 10 |
| bai10 | Tim Kiem Nhi Phan | Trung binh (Medium) | 10 |
| bai11 | Tong Cap Bang K | Trung binh (Medium) | 10 |
| bai12 | Day Con Tang Dai Nhat (LIS) | Trung binh (Medium) | 10 |
| bai13 | Leo Cau Thang (DP) | Trung binh (Medium) | 10 |
| bai14 | Kiem Tra Ngoac Hop Le | Trung binh (Medium) | 10 |
| bai15 | Kiem Tra Anagram | Trung binh (Medium) | 10 |
| bai16 | Bai Toan Balo 0/1 | Trung binh (Medium) | 10 |
| bai17 | Xau Con Chung Dai Nhat (LCS) | Kho (Hard) | 10 |
| bai18 | Duong Di Ngan Nhat BFS | Kho (Hard) | 10 |
| bai19 | Sap Xep Merge Sort | Kho (Hard) | 10 |
| bai20 | Cay Khung Nho Nhat (Kruskal) | Kho (Hard) | 10 |

**Thong ke:**
- **Easy:** 8 bai
- **Medium:** 8 bai
- **Hard:** 4 bai
- **Tong:** 20 bai
- **Tong test cases:** 200

---

> **Tai lieu duoc tao:** 01/2025
> **Phien ban CSDL:** 2.0
> **Du an:** NEO Online Judge
