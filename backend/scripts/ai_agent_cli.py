#!/usr/bin/env python3
"""
GTS (Go to Success) — AI Agent CLI
Công cụ test AI Mentor trực tiếp từ command line mà không cần khởi động toàn bộ backend.

Cách dùng:
    python backend/scripts/ai_agent_cli.py
    
Hoặc với arguments:
    python backend/scripts/ai_agent_cli.py --code "print(1+1)" --problem "Tính tổng hai số"
"""

import argparse
import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def load_grok_key() -> str:
    """Load Grok API key from .env file or environment variable."""
    # Try environment variable first
    key = os.environ.get("GROK_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if key:
        return key
    
    # Try .env file
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), ".env")
    
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GROK_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
                if line.startswith("OPENAI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def call_grok_api(code: str, problem: str, api_key: str, model: str = "grok-3-mini") -> str:
    """Call Grok API directly without settings module."""
    import requests
    
    SYSTEM_PROMPT = """Bạn là Mentor lập trình AI chuyên nghiệp. Hãy nhận xét code của học sinh một cách ngắn gọn, 
dùng định dạng Markdown với emoji:

1. ✅ **Điểm tốt:** Khen ngợi những gì học sinh làm đúng
2. ❌ **Vấn đề:** Chỉ ra lỗi sai hoặc chỗ cần cải thiện 
3. 💡 **Gợi ý:** Hướng dẫn cách sửa (KHÔNG viết code giải hoàn chỉnh)
4. 📚 **Học thêm:** Gợi ý kiến thức cần ôn tập

LƯU Ý: Không bao giờ đưa ra đáp án hoàn chỉnh."""

    user_prompt = f"**Đề bài:**\n{problem}\n\n**Code của học sinh:**\n```\n{code}\n```"
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 1500,
    }
    
    try:
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json=payload,
            timeout=30,
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ Lỗi API (HTTP {response.status_code}): {response.text}"
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"


def interactive_mode(api_key: str, model: str):
    """Interactive CLI mode for testing AI Agent."""
    print("\n" + "═" * 60)
    print("  GTS — AI AGENT CLI (Powered by Grok)")
    print("  Model:", model)
    print("═" * 60)
    print("  Nhập 'exit' hoặc Ctrl+C để thoát")
    print("  Nhập code Python/C++/Java rồi nhấn Enter 2 lần")
    print("═" * 60 + "\n")
    
    problem = input("📝 Nhập đề bài (hoặc Enter để bỏ qua): ").strip()
    if not problem:
        problem = "Giải bài tập lập trình theo yêu cầu."
    
    print("\n💻 Nhập code của bạn (nhấn Enter 2 lần khi xong):")
    lines = []
    empty_count = 0
    while True:
        try:
            line = input()
            if line == "exit":
                sys.exit(0)
            if line == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                lines.append(line)
        except KeyboardInterrupt:
            print("\n\nĐã thoát.")
            sys.exit(0)
    
    code = "\n".join(lines)
    if not code.strip():
        print("⚠️  Không có code nào được nhập!")
        return
    
    print("\n🤖 Đang phân tích code với Grok AI...\n")
    response = call_grok_api(code, problem, api_key, model)
    
    print("─" * 60)
    print("📊 NHẬN XÉT CỦA AI MENTOR:")
    print("─" * 60)
    print(response)
    print("─" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="GTS AI Agent CLI — Test Grok AI Mentor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  python backend/scripts/ai_agent_cli.py
  python backend/scripts/ai_agent_cli.py --model grok-3
  python backend/scripts/ai_agent_cli.py --code "n=int(input()); print(n*2)" --problem "Nhân đôi số"
        """
    )
    parser.add_argument("--code", help="Code cần review (nếu không nhập sẽ vào interactive mode)")
    parser.add_argument("--problem", help="Mô tả đề bài", default="Giải bài tập lập trình theo yêu cầu.")
    parser.add_argument("--model", help="Model Grok (grok-3-mini, grok-3)", default="grok-3-mini")
    parser.add_argument("--key", help="Grok API Key (nếu không đặt trong .env)")
    args = parser.parse_args()
    
    # Get API key
    api_key = args.key or load_grok_key()
    if not api_key:
        print("❌ Không tìm thấy GROK_API_KEY!")
        print("   Đặt trong file .env: GROK_API_KEY=your_key_here")
        print("   Hoặc dùng --key your_key_here")
        sys.exit(1)
    
    if args.code:
        # Direct mode
        print(f"\n🤖 Phân tích code với {args.model}...\n")
        response = call_grok_api(args.code, args.problem, api_key, args.model)
        print("─" * 60)
        print("📊 NHẬN XÉT CỦA AI MENTOR:")
        print("─" * 60)
        print(response)
        print("─" * 60)
    else:
        # Interactive mode
        interactive_mode(api_key, args.model)


if __name__ == "__main__":
    main()
