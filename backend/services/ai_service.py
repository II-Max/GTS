"""
NEO Online Judge - AI Mentor Service
Handles communication with Grok API (xAI) for code review and feedback.
Grok API is fully compatible with OpenAI API format.
"""

import logging
from typing import Dict, Any

import requests

from config.settings import settings

logger = logging.getLogger("neo")

# System instruction for AI Mentor
SYSTEM_INSTRUCTION = """
Bạn là Mentor lập trình AI chuyên nghiệp. Hãy nhận xét code của học sinh một cách ngắn gọn, 
dùng định dạng Markdown với emoji:

1. ✅ **Điểm tốt:** Khen ngợi những gì học sinh làm đúng
2. ❌ **Vấn đề:** Chỉ ra lỗi sai hoặc chỗ cần cải thiện 
3. 💡 **Gợi ý:** Hướng dẫn cách sửa (KHÔNG viết code giải hoàn chỉnh)
4. 📚 **Học thêm:** Gợi ý kiến thức cần ôn tập

LƯU Ý: Không bao giờ đưa ra đáp án hoàn chỉnh. Hãy để học sinh tự tìm ra giải pháp.
"""


class AIService:
    """
    Service for interacting with Grok API (xAI) to provide AI-powered code mentoring.
    Grok API is compatible with OpenAI API format — only URL and model name differ.
    """

    # Grok API endpoint (xAI) — compatible with OpenAI format
    API_URL = "https://api.x.ai/v1/chat/completions"

    AVAILABLE_MODELS = {
        "grok-3-mini": {
            "name": "Grok 3 Mini",
            "cost": "free",
            "quality": "good",
            "description": "Fast, free tier, good for basic code reviews",
        },
        "grok-3": {
            "name": "Grok 3",
            "cost": "low",
            "quality": "excellent",
            "description": "Best quality, best for detailed code analysis",
        },
    }

    @classmethod
    def get_default_model(cls) -> str:
        """Get the default AI model from settings (defaults to grok-3-mini)."""
        return getattr(settings, 'AI_MODEL', 'grok-3-mini')

    @classmethod
    def review_code(cls, code: str, problem_description: str, model: str = None) -> Dict[str, Any]:
        """
        Send code and problem to AI for review.

        Args:
            code: The student's code
            problem_description: The problem statement
            model: AI model to use (default from settings)

        Returns:
            Dict with keys: success (bool), response (str), model (str), error (str, optional)
        """
        model = model or cls.get_default_model()

        # Support both GROK_API_KEY (new) and OPENAI_API_KEY (legacy)
        api_key = getattr(settings, 'GROK_API_KEY', None) or getattr(settings, 'OPENAI_API_KEY', None)
        if not api_key:
            logger.error("Grok API key not configured")
            return {
                "success": False,
                "response": "⚠️ AI chưa được cấu hình. Vui lòng thêm GROK_API_KEY vào file .env",
                "model": model,
                "error": "API key missing",
            }

        prompt = (
            f"**Đề bài:**\n{problem_description}\n\n"
            f"**Code của học sinh:**\n```\n{code}\n```"
        )

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": prompt},
            ],
            "temperature": settings.AI_TEMPERATURE,
            "max_tokens": settings.AI_MAX_TOKENS,
        }

        try:
            logger.info(f"Calling AI model: {model}")
            response = requests.post(
                cls.API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
                json=payload,
                timeout=settings.AI_TIMEOUT,
            )

            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"]
                logger.info(f"AI response received successfully ({len(reply)} chars)")
                return {
                    "success": True,
                    "response": reply,
                    "model": model,
                }
            elif response.status_code == 401:
                return {
                    "success": False,
                    "response": "❌ Lỗi xác thực OpenAI API. Kiểm tra lại API key.",
                    "model": model,
                    "error": "401 Unauthorized",
                }
            elif response.status_code == 429:
                return {
                    "success": False,
                    "response": "⚠️ Đã vượt quá giới hạn sử dụng API. Vui lòng thử lại sau.",
                    "model": model,
                    "error": "429 Rate Limited",
                }
            else:
                return {
                    "success": False,
                    "response": f"❌ Lỗi AI (HTTP {response.status_code})",
                    "model": model,
                    "error": response.text,
                }

        except requests.exceptions.Timeout:
            logger.error("AI request timed out")
            return {
                "success": False,
                "response": "⏰ Yêu cầu AI bị timeout. Vui lòng thử lại.",
                "model": model,
                "error": "Timeout",
            }
        except Exception as e:
            logger.error(f"AI request failed: {e}", exc_info=True)
            return {
                "success": False,
                "response": f"❌ Lỗi kết nối AI: {str(e)}",
                "model": model,
                "error": str(e),
            }
