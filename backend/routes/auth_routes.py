"""
NEO Online Judge - Auth API Routes
HTTP API endpoints cho đăng nhập, đăng ký, quản lý user.
"""

import logging
from functools import wraps
from typing import Optional

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from backend.services.auth_service import AuthService
from backend.services.firebase_service import FirebaseService

logger = logging.getLogger("neo")
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
auth_service = AuthService()


# ======================================================================
# DECORATOR: Xác thực token
# ======================================================================

def require_auth(f):
    """Decorator yêu cầu xác thực token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Lấy token từ header
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]

        if not token:
            return jsonify({"success": False, "message": "Thiếu token xác thực."}), 401

        # Verify token
        payload = auth_service.verify_jwt_token(token)
        if not payload:
            # Thử verify với Firebase token
            firebase_user = auth_service.verify_firebase_token(token)
            if firebase_user:
                payload = {
                    "uid": firebase_user.get("uid"),
                    "email": firebase_user.get("email", ""),
                    "role": firebase_user.get("role", "student"),
                }
            else:
                return jsonify({"success": False, "message": "Token không hợp lệ hoặc đã hết hạn."}), 401

        kwargs["user"] = payload
        return f(*args, **kwargs)
    return decorated


def require_admin(f):
    """Decorator yêu cầu quyền admin."""
    @wraps(f)
    @require_auth
    def decorated(*args, **kwargs):
        user = kwargs.get("user", {})
        if user.get("role") != "admin":
            return jsonify({"success": False, "message": "Bạn không có quyền truy cập."}), 403
        return f(*args, **kwargs)
    return decorated


# ======================================================================
# API ENDPOINTS
# ======================================================================

@auth_bp.route("/register", methods=["POST"])
@cross_origin()
def register():
    """Đăng ký tài khoản mới (Email & Password)."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Dữ liệu không hợp lệ."}), 400

    email = data.get("email", "").strip()
    password = data.get("password", "")
    display_name = data.get("display_name", "").strip()

    success, message, user_data = auth_service.register_user(email, password, display_name)
    
    if success and user_data:
        # Tạo token
        token = auth_service.generate_jwt_token(user_data)
        return jsonify({
            "success": True,
            "message": message,
            "token": token,
            "user": {
                "uid": user_data["uid"],
                "email": user_data["email"],
                "display_name": user_data["display_name"],
                "role": user_data["role"],
                "avatar": user_data.get("avatar", ""),
            }
        }), 201
    else:
        return jsonify({"success": False, "message": message}), 400


@auth_bp.route("/login", methods=["POST"])
@cross_origin()
def login():
    """Đăng nhập bằng email & password (xác thực Firebase ở client)."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Dữ liệu không hợp lệ."}), 400

    id_token = data.get("id_token", "")
    email = data.get("email", "")

    if id_token:
        # Verify Firebase ID Token (cho OAuth login)
        decoded = auth_service.verify_firebase_token(id_token)
        if not decoded:
            return jsonify({"success": False, "message": "Token không hợp lệ."}), 401

        # Đồng bộ user từ OAuth
        user_data = auth_service.sync_oauth_user(decoded)
    elif email:
        # Login với email (dành cho password login đã xác thực client)
        success, message, user_data = auth_service.login_with_email(email, "")
        if not success:
            return jsonify({"success": False, "message": message}), 401
    else:
        return jsonify({"success": False, "message": "Thiếu thông tin đăng nhập."}), 400

    if not user_data:
        return jsonify({"success": False, "message": "Không tìm thấy người dùng."}), 404

    token = auth_service.generate_jwt_token(user_data)
    return jsonify({
        "success": True,
        "message": "Đăng nhập thành công!",
        "token": token,
        "user": {
            "uid": user_data["uid"],
            "email": user_data["email"],
            "display_name": user_data["display_name"],
            "role": user_data["role"],
            "avatar": user_data.get("avatar", ""),
            "score": user_data.get("score", 0),
            "problems_solved": user_data.get("problems_solved", 0),
        }
    })


@auth_bp.route("/profile", methods=["GET"])
@require_auth
def get_profile(**kwargs):
    """Lấy thông tin profile người dùng."""
    user = kwargs.get("user", {})
    profile = auth_service.get_user_profile(user.get("uid"))
    
    if not profile:
        return jsonify({"success": False, "message": "Không tìm thấy người dùng."}), 404

    return jsonify({
        "success": True,
        "user": {
            "uid": profile.get("uid"),
            "email": profile.get("email"),
            "display_name": profile.get("display_name"),
            "avatar": profile.get("avatar", ""),
            "role": profile.get("role", "student"),
            "score": profile.get("score", 0),
            "problems_solved": profile.get("problems_solved", 0),
            "join_date": profile.get("join_date", ""),
            "last_login": profile.get("last_login", ""),
            "auth_provider": profile.get("auth_provider", ""),
        }
    })


@auth_bp.route("/profile", methods=["PUT"])
@require_auth
def update_profile(**kwargs):
    """Cập nhật thông tin profile."""
    user = kwargs.get("user", {})
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "Dữ liệu không hợp lệ."}), 400

    allowed = {"display_name", "avatar"}
    updates = {k: v for k, v in data.items() if k in allowed}

    if not updates:
        return jsonify({"success": False, "message": "Không có dữ liệu để cập nhật."}), 400

    success = auth_service.update_user_profile(user.get("uid"), updates)
    return jsonify({
        "success": success,
        "message": "Cập nhật thành công!" if success else "Cập nhật thất bại."
    })


@auth_bp.route("/sync", methods=["POST"])
@cross_origin()
def sync_oauth():
    """Đồng bộ user sau khi đăng nhập bằng OAuth (Google/GitHub)."""
    data = request.get_json()
    if not data or not data.get("id_token"):
        return jsonify({"success": False, "message": "Thiếu ID token."}), 400

    decoded = auth_service.verify_firebase_token(data["id_token"])
    if not decoded:
        return jsonify({"success": False, "message": "Token không hợp lệ."}), 401

    user_data = auth_service.sync_oauth_user(decoded)
    token = auth_service.generate_jwt_token(user_data)

    return jsonify({
        "success": True,
        "token": token,
        "user": {
            "uid": user_data.get("uid"),
            "email": user_data.get("email"),
            "display_name": user_data.get("display_name"),
            "avatar": user_data.get("avatar", ""),
            "role": user_data.get("role", "student"),
            "score": user_data.get("score", 0),
            "problems_solved": user_data.get("problems_solved", 0),
        }
    })


@auth_bp.route("/rank", methods=["GET"])
@cross_origin()
def get_rank():
    """Lấy bảng xếp hạng."""
    limit = request.args.get("limit", 50, type=int)
    rank = auth_service.get_user_rank(limit)
    return jsonify({"success": True, "rank": rank})


@auth_bp.route("/admin/users", methods=["GET"])
@require_admin
def admin_get_users(**kwargs):
    """[Admin] Lấy danh sách tất cả người dùng."""
    users = auth_service.get_all_users()
    return jsonify({"success": True, "users": users})


@auth_bp.route("/admin/users/<uid>", methods=["PUT"])
@require_admin
def admin_update_user(uid, **kwargs):
    """[Admin] Cập nhật thông tin user (role, active status)."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Dữ liệu không hợp lệ."}), 400

    allowed = {"role", "is_active", "display_name", "score"}
    updates = {k: v for k, v in data.items() if k in allowed}
    
    if auth_service.update_user_profile(uid, updates):
        return jsonify({"success": True, "message": "Cập nhật thành công!"})
    return jsonify({"success": False, "message": "Cập nhật thất bại."}), 500
