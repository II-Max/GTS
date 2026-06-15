"""
NEO Online Judge - Auth API Routes
HTTP API endpoints cho dang nhap, dang ky, quan ly user.
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
# DECORATOR: Xac thuc token
# ======================================================================

def require_auth(f):
    """Decorator yeu cau xac thuc token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]

        if not token:
            return jsonify({"success": False, "message": "Thieu token xac thuc."}), 401

        # Thu verify JWT truoc
        payload = auth_service.verify_jwt_token(token)
        if not payload:
            # Thu verify Firebase ID Token
            firebase_user = auth_service.verify_firebase_token(token)
            if firebase_user:
                # Lay role tu DB thay vi tin tuong token
                uid = firebase_user.get("uid")
                profile = auth_service.get_user_profile(uid) or {}
                payload = {
                    "uid": uid,
                    "email": firebase_user.get("email", ""),
                    "role": profile.get("role", "student"),
                }
            else:
                return jsonify({"success": False, "message": "Token khong hop le hoac da het han."}), 401

        kwargs["user"] = payload
        return f(*args, **kwargs)
    return decorated


def require_teacher(f):
    """Decorator yeu cau quyen giao vien."""
    @wraps(f)
    @require_auth
    def decorated(*args, **kwargs):
        user = kwargs.get("user", {})
        if user.get("role") not in ("teacher", "admin"):
            return jsonify({"success": False, "message": "Ban khong co quyen truy cap."}), 403
        return f(*args, **kwargs)
    return decorated


def require_admin(f):
    """Decorator yeu cau quyen admin."""
    @wraps(f)
    @require_auth
    def decorated(*args, **kwargs):
        user = kwargs.get("user", {})
        if user.get("role") != "admin":
            return jsonify({"success": False, "message": "Ban khong co quyen truy cap."}), 403
        return f(*args, **kwargs)
    return decorated


# ======================================================================
# API ENDPOINTS
# ======================================================================

@auth_bp.route("/register", methods=["POST"])
@cross_origin()
def register():
    """Dang ky tai khoan moi (Email & Password)."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Du lieu khong hop le."}), 400

    email = data.get("email", "").strip()
    password = data.get("password", "")
    display_name = data.get("display_name", "").strip()

    # Validate co ban
    if not email or not password or not display_name:
        return jsonify({"success": False, "message": "Vui long dien day du thong tin."}), 400
    if len(password) < 6:
        return jsonify({"success": False, "message": "Mat khau phai co it nhat 6 ky tu."}), 400

    success, message, user_data = auth_service.register_user(email, password, display_name)

    if success and user_data:
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
    """Dang nhap — chi nhan Firebase ID Token (da xac thuc phia client)."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Du lieu khong hop le."}), 400

    id_token = data.get("id_token", "")
    if not id_token:
        return jsonify({"success": False, "message": "Thieu ID token Firebase."}), 400

    decoded = auth_service.verify_firebase_token(id_token)
    if not decoded:
        return jsonify({"success": False, "message": "Token khong hop le."}), 401

    user_data = auth_service.sync_oauth_user(decoded)
    if not user_data:
        return jsonify({"success": False, "message": "Khong tim thay nguoi dung."}), 404

    token = auth_service.generate_jwt_token(user_data)
    return jsonify({
        "success": True,
        "message": "Dang nhap thanh cong!",
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
    """Lay thong tin profile nguoi dung."""
    user = kwargs.get("user", {})
    profile = auth_service.get_user_profile(user.get("uid"))

    if not profile:
        return jsonify({"success": False, "message": "Khong tim thay nguoi dung."}), 404

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
    """Cap nhat thong tin profile."""
    user = kwargs.get("user", {})
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "Du lieu khong hop le."}), 400

    # Chi cho phep cap nhat cac truong an toan
    allowed = {"display_name", "avatar"}
    updates = {k: v for k, v in data.items() if k in allowed}

    if not updates:
        return jsonify({"success": False, "message": "Khong co du lieu de cap nhat."}), 400

    success = auth_service.update_user_profile(user.get("uid"), updates)
    return jsonify({
        "success": success,
        "message": "Cap nhat thanh cong!" if success else "Cap nhat that bai."
    })


@auth_bp.route("/sync", methods=["POST"])
@cross_origin()
def sync_oauth():
    """Dong bo user sau khi dang nhap bang OAuth (Google/GitHub)."""
    data = request.get_json()
    if not data or not data.get("id_token"):
        return jsonify({"success": False, "message": "Thieu ID token."}), 400

    decoded = auth_service.verify_firebase_token(data["id_token"])
    if not decoded:
        return jsonify({"success": False, "message": "Token khong hop le."}), 401

    user_data = auth_service.sync_oauth_user(decoded)
    if not user_data:
        return jsonify({"success": False, "message": "Khong the dong bo nguoi dung."}), 500

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
@require_auth
@cross_origin()
def get_rank(**kwargs):
    """Lay bang xep hang (yeu cau dang nhap) — chi tra ve du lieu public."""
    limit = min(request.args.get("limit", 50, type=int), 100)
    rank = auth_service.get_user_rank(limit)
    return jsonify({"success": True, "rank": rank})


@auth_bp.route("/admin/users", methods=["GET"])
@require_admin
def admin_get_users(**kwargs):
    """[Admin] Lay danh sach tat ca nguoi dung."""
    users = auth_service.get_all_users()
    return jsonify({"success": True, "users": users})


@auth_bp.route("/admin/users/<uid>", methods=["PUT"])
@require_admin
def admin_update_user(uid, **kwargs):
    """[Admin] Cap nhat thong tin user (role, active status)."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Du lieu khong hop le."}), 400

    allowed = {"role", "is_active", "display_name", "score"}
    updates = {k: v for k, v in data.items() if k in allowed}

    if auth_service.update_user_profile(uid, updates):
        return jsonify({"success": True, "message": "Cap nhat thanh cong!"})
    return jsonify({"success": False, "message": "Cap nhat that bai."}), 500
