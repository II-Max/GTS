"""
GTS (Go to Success) - Authentication Service
Xử lý đăng nhập, đăng ký, xác thực token và phân quyền người dùng.


"""

import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple

import jwt
from firebase_admin import auth as firebase_auth

from backend.config.settings import settings
from backend.services.firebase_service import FirebaseService

logger = logging.getLogger("neo")


class AuthService:
    """
    Service quản lý xác thực và phân quyền người dùng.
    
    Phương thức hỗ trợ:
    - Email & Password (đăng ký / đăng nhập)
    - Google OAuth (qua Firebase)
    - GitHub OAuth (qua Firebase)
    - Quên mật khẩu (gửi email reset)
    """

    def __init__(self):
        self._firebase = FirebaseService()
        self._firebase.initialize()

    # ======================================================================
    # 1. ĐĂNG KÝ TÀI KHOẢN (Email & Password)
    # ======================================================================

    def register_user(
        self, 
        email: str, 
        password: str, 
        display_name: str,
        role: str = "student"
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        Đăng ký tài khoản mới với email & password.
        
        Returns:
            (success, message, user_data)
        """
        try:
            # Validate input
            if not email or not password or not display_name:
                return False, "Vui lòng điền đầy đủ thông tin.", None

            if len(password) < 6:
                return False, "Mật khẩu phải có ít nhất 6 ký tự.", None

            # Tạo user trên Firebase Authentication
            user_record = firebase_auth.create_user(
                email=email,
                password=password,
                display_name=display_name,
            )

            # Lưu thông tin vào Realtime Database
            user_data = {
                "uid": user_record.uid,
                "email": email,
                "display_name": display_name,
                "role": role,
                "avatar": "",
                "score": 0,
                "problems_solved": 0,
                "join_date": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat(),
                "auth_provider": "password",
                "is_active": True,
            }
            self._firebase.update(f"users/{user_record.uid}", user_data)

            logger.info(f"User registered: {email} (uid: {user_record.uid})")
            return True, "Đăng ký thành công!", user_data

        except firebase_auth.EmailAlreadyExistsError:
            return False, "Email này đã được đăng ký. Vui lòng dùng email khác hoặc đăng nhập.", None
        except Exception as e:
            logger.error(f"Registration error: {e}", exc_info=True)
            return False, f"Lỗi đăng ký: {str(e)}", None

    # ======================================================================
    # 2. ĐĂNG NHẬP (Email & Password - xác thực Firebase)
    # ======================================================================

    def login_with_email(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Đăng nhập bằng email & password.
        NOTE: Việc xác thực Firebase diễn ra ở client-side (JavaScript).
        Backend chỉ verify token và lấy thông tin user.
        """
        try:
            # Cập nhật last_login
            users = self._firebase.get_data("users")
            if users:
                for uid, data in users.items():
                    if isinstance(data, dict) and data.get("email") == email:
                        self._firebase.update(f"users/{uid}", {
                            "last_login": datetime.now().isoformat()
                        })
                        return True, "Đăng nhập thành công!", data

            return False, "Không tìm thấy người dùng.", None
        except Exception as e:
            logger.error(f"Login error: {e}", exc_info=True)
            return False, f"Lỗi đăng nhập: {str(e)}", None

    # ======================================================================
    # 3. XÁC THỰC TOKEN (JWT / Firebase ID Token)
    # ======================================================================

    def verify_firebase_token(self, id_token: str) -> Optional[Dict]:
        """
        Xác thực Firebase ID Token từ client.

        Dùng cho Google, GitHub login (Firebase xử lý OAuth).
        """
        try:
            decoded = firebase_auth.verify_id_token(id_token)
            return decoded
        except Exception as e:
            logger.warning(f"Token verification failed: {e}")
            return None

    def create_custom_token(self, uid: str) -> Optional[str]:
        """Tạo Firebase custom token cho user."""
        try:
            return firebase_auth.create_custom_token(uid).decode("utf-8")
        except Exception as e:
            logger.error(f"Custom token error: {e}")
            return None

    def generate_jwt_token(self, user_data: Dict) -> str:
        """Tạo JWT token cho phiên đăng nhập."""
        payload = {
            "uid": user_data.get("uid"),
            "email": user_data.get("email"),
            "role": user_data.get("role", "student"),
            "exp": datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRY_HOURS),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def verify_jwt_token(self, token: str) -> Optional[Dict]:
        """Xác thực JWT token."""
        try:
            payload = jwt.decode(
                token, 
                settings.JWT_SECRET_KEY, 
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            return None

    # ======================================================================
    # 4. QUẢN LÝ NGƯỜI DÙNG
    # ======================================================================

    def get_user_profile(self, uid: str) -> Optional[Dict]:
        """Lấy thông tin profile người dùng."""
        return self._firebase.get_child("users", uid)

    def get_all_users(self) -> Dict[str, Any]:
        """Lấy danh sách tất cả người dùng (cho admin)."""
        return self._firebase.get_data("users") or {}

    def update_user_profile(self, uid: str, updates: Dict) -> bool:
        """Cập nhật thông tin người dùng."""
        try:
            # Không cho phép thay đổi role từ client
            forbidden = {"role", "uid", "is_active"}
            safe_updates = {k: v for k, v in updates.items() if k not in forbidden}

            if safe_updates:
                self._firebase.update(f"users/{uid}", safe_updates)
            return True
        except Exception as e:
            logger.error(f"Update profile error: {e}")
            return False

    def update_user_score(self, uid: str, score_delta: int, problem_id: str = ""):
        """Cập nhật điểm số sau khi chấm bài."""
        try:
            user = self.get_user_profile(uid)
            if user:
                current_score = user.get("score", 0)
                solved = user.get("problems_solved", 0)
                solved_list = user.get("solved_problems", [])

                if problem_id and problem_id not in solved_list:
                    solved_list.append(problem_id)
                    solved += 1

                self._firebase.update(f"users/{uid}", {
                    "score": current_score + score_delta,
                    "problems_solved": solved,
                    "solved_problems": solved_list,
                })
                logger.info(f"Score updated for {uid}: +{score_delta}")
        except Exception as e:
            logger.error(f"Score update error: {e}")

    # ======================================================================
    # 5. PHÂN QUYỀN
    # ======================================================================

    def is_admin(self, uid: str) -> bool:
        """Kiểm tra user có quyền admin không."""
        user = self.get_user_profile(uid)
        return user is not None and user.get("role") == "admin"

    def require_admin(self, uid: str) -> bool:
        """Yêu cầu quyền admin."""
        if not self.is_admin(uid):
            logger.warning(f"Access denied for non-admin user: {uid}")
            return False
        return True

    def get_user_rank(self, limit: int = 50) -> list:
        """Lấy bảng xếp hạng người dùng theo điểm."""
        users = self.get_all_users()
        ranked = []
        for uid, data in users.items():
            if isinstance(data, dict) and data.get("role") != "admin":
                ranked.append({
                    "uid": uid,
                    "display_name": data.get("display_name", "Unknown"),
                    "avatar": data.get("avatar", ""),
                    "score": data.get("score", 0),
                    "problems_solved": data.get("problems_solved", 0),
                })

        ranked.sort(key=lambda x: x["score"], reverse=True)
        return ranked[:limit]

    # ======================================================================
    # 6. ĐỒNG BỘ USER SAU KHI ĐĂNG NHẬP BẰNG OAuth
    # ======================================================================

    def sync_oauth_user(self, firebase_user: dict) -> Dict:
        """
        Nếu user chưa tồn tại trong DB, tạo mới.
        """
        uid = firebase_user.get("uid")
        if not uid:
            return {}

        existing = self.get_user_profile(uid)
        if existing:
            # Cập nhật last_login và avatar mới nhất
            avatar = firebase_user.get("picture", "")
            update_data = {"last_login": datetime.now().isoformat()}
            if avatar and existing.get("avatar") != avatar:
                update_data["avatar"] = avatar
                # Cập nhật public_leaderboard avatar
                score = existing.get("score", 0)
                problems_solved = existing.get("problems_solved", 0)
                display_name = existing.get("display_name") or existing.get("name") or "Ẩn danh"
                self._firebase.update_public_leaderboard(uid, display_name, score, problems_solved, avatar)
                
            self._firebase.update(f"users/{uid}", update_data)
            existing.update(update_data)
            return existing

        # Tạo user mới từ OAuth
        provider = firebase_user.get("firebase", {}).get("sign_in_provider", "google")
        user_data = {
            "uid": uid,
            "email": firebase_user.get("email", ""),
            "display_name": firebase_user.get("name", firebase_user.get("display_name", "User")),
            "avatar": firebase_user.get("picture", ""),
            "role": "student",
            "score": 0,
            "problems_solved": 0,
            "join_date": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat(),
            "auth_provider": provider,
            "is_active": True,
        }
        self._firebase.update(f"users/{uid}", user_data)
        logger.info(f"New OAuth user created: {user_data['email']} via {provider}")
        return user_data

