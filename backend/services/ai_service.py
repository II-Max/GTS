"""
NEO Online Judge - AI Mentor Service
Handles communication with DeepSeek API for code review and feedback.
"""

import logging
from typing import Dict, Any

import requests

from backend.config.settings import settings

logger = logging.getLogger("neo")

SYSTEM_INSTRUCTION = (
    "Ban la Mentor lap trinh AI chuyen nghiep. Hay nhan xet code cua hoc sinh "
    "mot cach ngan gon, dung dinh dang Markdown voi emoji:\n\n"
    "1. \u2705 **Diem tot:** Khen ngoi nhung gi hoc sinh lam dung\n"
    "2. \u274c **Van de:** Chi ra loi sai hoac cho can cai thien\n"
    "3. \U0001f4a1 **Goi y:** Huong dan cach sua (KHONG viet code giai hoan chinh)\n"
    "4. \U0001f4da **Hoc them:** Goi y kien thuc can on tap\n\n"
    "LUU Y: Khong bao gio dua ra dap an hoan chinh. Hay de hoc sinh tu tim ra giai phap."
)


class AIService:
    """AI Mentor Service. Supports DeepSeek (default) + OpenAI (fallback)."""

    DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

    @classmethod
    def get_default_model(cls) -> str:
        return getattr(settings, 'DEEPSEEK_MODEL', None) or \
               getattr(settings, 'AI_MODEL', 'deepseek-chat')

    @classmethod
    def review_code(cls, code: str, problem_description: str,
                    model: str = None) -> Dict[str, Any]:
        model = model or cls.get_default_model()

        api_key = getattr(settings, 'DEEPSEEK_API_KEY', None) or \
                  getattr(settings, 'OPENAI_API_KEY', None)

        if not api_key:
            logger.error("AI API key not configured")
            return {
                "success": False,
                "response": (
                    "\u26a0\ufe0f AI chua duoc cau hinh. "
                    "Them DEEPSEEK_API_KEY hoac OPENAI_API_KEY vao .env"
                ),
                "model": model,
                "error": "API key missing",
            }

        is_deepseek = bool(getattr(settings, 'DEEPSEEK_API_KEY', None))
        api_url = cls.DEEPSEEK_API_URL if is_deepseek \
                  else "https://api.openai.com/v1/chat/completions"
        provider_name = "DeepSeek" if is_deepseek else "OpenAI"

        prompt = f"**De bai:**\n{problem_description}\n\n**Code cua hoc sinh:**\n```\n{code}\n```"

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": prompt},
            ],
            "temperature": settings.AI_TEMPERATURE,
            "max_tokens": settings.AI_MAX_TOKENS,
            "stream": False,
        }

        try:
            logger.info("Calling %s model: %s", provider_name, model)
            resp = requests.post(
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
                logger.info("AI response received (%d chars)", len(reply))
                return {"success": True, "response": reply, "model": model}

            if resp.status_code == 401:
                return {
                    "success": False,
                    "response": "\u274c Loi xac thuc " + provider_name + ". Kiem tra lai API key.",
                    "model": model, "error": "401",
                }
            if resp.status_code == 429:
                return {
                    "success": False,
                    "response": "\u26a0\ufe0f Da vuot qua gioi han su dung. Thu lai sau.",
                    "model": model, "error": "429",
                }

            err_detail = resp.text[:200] if resp.text else str(resp.status_code)
            return {
                "success": False,
                "response": f"\u274c Loi AI (HTTP {resp.status_code})",
                "model": model, "error": err_detail,
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "response": "\u23f0 Yeu cau AI bi timeout.",
                "model": model, "error": "Timeout",
            }
        except Exception as e:
            logger.error("AI request failed: %s", e, exc_info=True)
            return {
                "success": False,
                "response": f"\u274c Loi ket noi AI: {str(e)}",
                "model": model, "error": str(e),
            }
