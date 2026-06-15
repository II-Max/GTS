# GTS (GO TO SUCCESS) - V02 NÂNG CẤP HỆ THỐNG

## 🔐 HỆ THỐNG XÁC THỰC (AUTHENTICATION)

Trước đây, trang **problems.html** dùng Firebase Auth nhưng redirect về **index.html** - nơi chỉ có nút "Đăng nhập Google" đơn giản và không có form đăng ký. Hệ thống không có trang đăng nhập riêng.

### Thay đổi:

**1. Trang đăng nhập mới: `frontend/login.html`**
- Giao diện Cyberpunk với hiệu ứng particles, glitch text, background lưới
- Form **Đăng nhập**: email + password
- Form **Đăng ký**: họ tên + email + password + xác nhận password
- Password toggle (ẩn/hiện mật khẩu)
- Nút "Quên mật khẩu" - gửi email reset
- Đăng nhập xã hội: **Google**, **GitHub** (đã bỏ Facebook)
- Chuyển hướng thông minh về problems.html sau khi đăng nhập

**2. Trang gateway mới: `frontend/index.html`**
- UI Cyberpunk với hiệu ứng glitch, background hoạt ảnh grid
- Mặc định hiển thị: **Google login** + **"TẤT CẢ PHƯƠNG THỨC ĐĂNG NHẬP"** (dẫn đến login.html)
- Khi đã đăng nhập: hiển thị thông tin user + nút "VÀO HỆ THỐNG"
- Quick links: Đăng nhập, Đăng ký, Bài tập, Bảng xếp hạng
- Đồng bộ user với backend

**3. Script kiểm tra auth: `frontend/js/firebase-auth-check.js`**
- Tự động redirect sang login.html nếu chưa đăng nhập
- Thêm avatar người dùng vào navbar
- Hiển thị tên, email ở góc navbar

**4. Backend API Auth: `backend/services/auth_service.py` + `backend/routes/auth_routes.py`**
- `POST /api/auth/register` - Đăng ký tài khoản
- `POST /api/auth/login` - Đăng nhập (hỗ trợ id_token + email)
- `POST /api/auth/sync` - Đồng bộ user OAuth
- `GET /api/auth/profile` - Lấy profile
- `PUT /api/auth/profile` - Cập nhật profile
- `GET /api/auth/rank` - Bảng xếp hạng
- `GET /api/auth/admin/users` - [Admin] Quản lý user
- JWT token authentication
- Decorator: `@require_auth`, `@require_admin`

## 🔧 UI & INPUT FIXES

### Vấn đề:
- Icon trong ô input bị lệch/tràn
- Placeholder quá mờ
- Nút toggle password bị đè lên icon

### Đã sửa:
- `input-wrapper` dùng `display: flex + align-items: center`
- Icon dùng `z-index: 2 + pointer-events: none`
- Toggle password dùng `z-index: 2` để không bị chồng lấn
- Placeholder opacity = 1 cho dễ đọc

## 🚀 CÁC NÂNG CẤP KHÁC

### Backend:
- **Flask API server** chạy trên luồng riêng (port 5000)
- Thêm **backend/config/settings.py** với biến môi trường
- JWT_SECRET_KEY tự động cấu hình
- **Chấm bài tự động**:
  - Hỗ trợ C++, Python, Java
  - Test case so sánh output chính xác
  - Xử lý timeout và memory limit
- **AI Mentor** tích hợp OpenAI/GPT
- **Hàng đợi Redis** tùy chọn

### Frontend:
- Tất cả trang chính được đồng bộ auth script
- Dashboard hiển thị thống kê (điểm, rank, biểu đồ tròn)
- Chat global realtime kèm timestamp
- Role-based UI (Student / Teacher)

### Cấu trúc thư mục:
- `backend/core/` - Engine chấm bài & compiler
- `backend/models/` - Model Submission
- `backend/services/` - Auth, Firebase, AI service
- `backend/config/` - Settings + Logging
- `frontend/js/` - Firebase config + auth check
- `setup/scripts/` - Deployment scripts

