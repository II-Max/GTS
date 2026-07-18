"""
GTS (Go to Success) - Playground API Routes
HTTP API endpoints for the "Thử Nghiệm" (Playground) feature.
Allows students to run code freely and chat with AI Agent.
"""

import os
import time
import tempfile
import logging
import subprocess
from functools import wraps
from typing import Optional

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from backend.core.compiler import Compiler
from backend.services.ai_service import AIService
from backend.config.settings import settings

logger = logging.getLogger("neo")
playground_bp = Blueprint("playground", __name__, url_prefix="/api/playground")


# ======================================================================
# AUTH DECORATOR (reuse logic from auth_routes)
# ======================================================================

def playground_require_auth(f):
    """Lightweight auth decorator for playground endpoints."""
    @wraps(f)
    @cross_origin()
    def decorated(*args, **kwargs):
        from backend.services.auth_service import AuthService
        auth_service = AuthService()

        token = None
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]

        # Local debug bypass
        if settings.DEBUG and token == "local-test-token":
            payload = {
                "uid": "local-test-uid",
                "email": "local-test@gts.com",
                "role": "student",
            }
        else:
            if not token:
                return jsonify({"success": False, "message": "Thiếu token xác thực."}), 401

            # Try JWT first, then Firebase token
            payload = auth_service.verify_jwt_token(token)
            if not payload:
                firebase_user = auth_service.verify_firebase_token(token)
                if firebase_user:
                    uid = firebase_user.get("uid")
                    profile = auth_service.get_user_profile(uid) or {}
                    payload = {
                        "uid": uid,
                        "email": firebase_user.get("email", ""),
                        "role": profile.get("role", "student"),
                    }
                else:
                    return jsonify({"success": False, "message": "Token không hợp lệ."}), 401

        kwargs["user"] = payload
        return f(*args, **kwargs)
    return decorated


# ======================================================================
# POST /api/playground/run — Execute code directly
# ======================================================================

PLAYGROUND_TIMEOUT = 5        # Max execution time (seconds)
MAX_OUTPUT_LENGTH = 10240     # Max output size (10 KB)
RUN_COOLDOWN_MS = 2000        # Min interval between runs per user

# Simple in-memory rate limiter: { uid: last_run_timestamp }
_last_run = {}


@playground_bp.route("/run", methods=["POST"])
@playground_require_auth
def run_code(**kwargs):
    """
    Execute code and return stdout/stderr.
    
    Request JSON:
        code (str): Source code
        language (str): Programming language
        stdin (str, optional): Standard input data
    
    Response JSON:
        success (bool)
        stdout (str)
        stderr (str)
        execution_time (float): seconds
        exit_code (int)
    """
    user = kwargs.get("user", {})
    uid = user.get("uid", "anonymous")

    # Rate limiting
    now_ms = int(time.time() * 1000)
    last = _last_run.get(uid, 0)
    if now_ms - last < RUN_COOLDOWN_MS:
        remaining = (RUN_COOLDOWN_MS - (now_ms - last)) / 1000
        return jsonify({
            "success": False,
            "message": f"Vui lòng chờ {remaining:.1f}s trước khi chạy tiếp.",
        }), 429

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Dữ liệu không hợp lệ."}), 400

    code = data.get("code", "").strip()
    language = data.get("language", "python").strip().lower()
    stdin_data = data.get("stdin", "")

    if not code:
        return jsonify({"success": False, "message": "Bạn chưa nhập code!"}), 400

    if not Compiler.is_supported(language):
        supported = ", ".join(Compiler.SUPPORTED_LANGUAGES.keys())
        return jsonify({
            "success": False,
            "message": f"Ngôn ngữ '{language}' chưa được hỗ trợ. Hỗ trợ: {supported}",
        }), 400

    _last_run[uid] = now_ms

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Step 1: Compile
            run_cmd, compile_err = Compiler.compile(language, "playground", code, temp_dir)

            if compile_err:
                return jsonify({
                    "success": False,
                    "stdout": "",
                    "stderr": compile_err,
                    "execution_time": 0,
                    "exit_code": -1,
                    "phase": "compilation",
                })

            # Step 2: Execute
            start_time = time.time()
            try:
                process = subprocess.run(
                    run_cmd,
                    input=str(stdin_data) if stdin_data else "",
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=PLAYGROUND_TIMEOUT,
                )
                elapsed = time.time() - start_time

                stdout = (process.stdout or "")[:MAX_OUTPUT_LENGTH]
                stderr = (process.stderr or "")[:MAX_OUTPUT_LENGTH]

                return jsonify({
                    "success": True,
                    "stdout": stdout.strip(),
                    "stderr": stderr.strip(),
                    "execution_time": round(elapsed, 3),
                    "exit_code": process.returncode,
                    "phase": "execution",
                })

            except subprocess.TimeoutExpired:
                elapsed = time.time() - start_time
                return jsonify({
                    "success": False,
                    "stdout": "",
                    "stderr": f"⏱️ Time Limit Exceeded — Chương trình chạy quá {PLAYGROUND_TIMEOUT} giây.",
                    "execution_time": round(elapsed, 3),
                    "exit_code": -1,
                    "phase": "execution",
                })

    except Exception as e:
        logger.error(f"Playground run error: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "stdout": "",
            "stderr": f"Lỗi hệ thống: {str(e)}",
            "execution_time": 0,
            "exit_code": -1,
            "phase": "system",
        }), 500


# ======================================================================
# POST /api/playground/ai-chat — AI Agent conversational chat
# ======================================================================

PLAYGROUND_AI_SYSTEM = (
    "Bạn là GTS AI Assistant — trợ lý lập trình. "
    "Đây là chế độ Thử Nghiệm, hãy giúp đỡ học sinh một cách NHANH NHẤT và NGẮN GỌN NHẤT ĐỂ TIẾT KIỆM TOKEN:\n\n"
    "1. 💡 Đi thẳng vào vấn đề, không vòng vo.\n"
    "2. 🐛 Chỉ ra lỗi sai ngay lập tức.\n"
    "3. ✨ Gợi ý tối ưu ngắn gọn (1-2 câu).\n"
    "4. 📝 Chỉ viết code mẫu những phần quan trọng, không viết lại toàn bộ code nếu không cần.\n\n"
    "Quy tắc tuyệt đối:\n"
    "- SIÊU NGẮN GỌN, TRỌNG TÂM.\n"
    "- KHÔNG GIẢI THÍCH DÀI DÒNG.\n"
    "- Dùng tiếng Việt và Markdown."
)


@playground_bp.route("/ai-chat", methods=["POST"])
@playground_require_auth
def ai_chat(**kwargs):
    """
    AI Agent conversational chat with code context.
    
    Request JSON:
        message (str): User's message
        code (str, optional): Current code in editor
        language (str, optional): Current language
        history (list, optional): Previous messages [{role, content}]
    
    Response JSON:
        success (bool)
        response (str): AI's reply in markdown
    """
    user = kwargs.get("user", {})

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Dữ liệu không hợp lệ."}), 400

    message = data.get("message", "").strip()
    code = data.get("code", "").strip()
    language = data.get("language", "python")
    history = data.get("history", [])

    if not message:
        return jsonify({"success": False, "message": "Bạn chưa nhập tin nhắn!"}), 400

    # Build API key
    api_key = getattr(settings, 'NVIDIA_API_KEY', None) or \
              getattr(settings, 'OPENAI_API_KEY', None)

    if not api_key:
        return jsonify({
            "success": False,
            "response": "⚠️ AI chưa được cấu hình. Liên hệ quản trị viên.",
        })

    is_nvidia = bool(getattr(settings, 'NVIDIA_API_KEY', None))
    api_url = AIService.NVIDIA_API_URL if is_nvidia \
              else "https://api.openai.com/v1/chat/completions"
    model = AIService.get_default_model()

    # Build messages
    messages = [{"role": "system", "content": PLAYGROUND_AI_SYSTEM}]

    # Add conversation history (limit to last 10 messages to control token usage)
    if history:
        for msg in history[-10:]:
            if isinstance(msg, dict) and msg.get("role") in ("user", "assistant"):
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"][:2000],  # Truncate long messages
                })

    # Build current user message with code context
    user_msg = message
    if code:
        user_msg = f"**Code hiện tại ({language}):**\n```{language}\n{code[:3000]}\n```\n\n**Câu hỏi:** {message}"

    messages.append({"role": "user", "content": user_msg})

    # Call AI API
    import requests as http_requests

    payload = {
        "model": model,
        "messages": messages,
        "temperature": settings.AI_TEMPERATURE,
        "max_tokens": 800,  # Giới hạn token thấp hơn để tiết kiệm chi phí
        "stream": False,
    }

    try:
        resp = http_requests.post(
            api_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json=payload,
            timeout=settings.AI_TIMEOUT,
        )

        if resp.status_code == 200:
            reply = resp.json()["choices"][0]["message"]["content"]
            return jsonify({"success": True, "response": reply})

        if resp.status_code == 429:
            return jsonify({
                "success": False,
                "response": "⚠️ Đã vượt giới hạn sử dụng AI. Thử lại sau ít phút.",
            })

        return jsonify({
            "success": False,
            "response": f"❌ Lỗi AI (HTTP {resp.status_code})",
        })

    except http_requests.exceptions.Timeout:
        return jsonify({
            "success": False,
            "response": "⏰ AI phản hồi quá chậm. Thử lại nhé!",
        })
    except Exception as e:
        logger.error(f"Playground AI chat error: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "response": f"❌ Lỗi kết nối AI: {str(e)}",
        })
