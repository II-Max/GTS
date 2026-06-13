import firebase_admin
from firebase_admin import credentials, db
import requests
import time
import sys
import os
import subprocess
import json

# ==============================================================================
# MODULE 1: CẤU HÌNH HỆ THỐNG
# ==============================================================================
print(">> [SYSTEM] Đang khởi động NEO JUDGE CORE...")

# 1. Sửa lỗi hiển thị tiếng Việt trên Console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except: pass

# 2. Cấu hình Firebase
CRED_PATH = 'service-account.json' 
DB_URL = 'https://neo-online-judge-default-rtdb.firebaseio.com'

CURRENT_MODEL = "gpt-4o-mini"

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(CRED_PATH)
        firebase_admin.initialize_app(cred, {'databaseURL': DB_URL})
    print("   -> [OK] Kết nối Firebase thành công.")
except Exception as e:
    print(f"   -> [ERROR] Lỗi Firebase: {e}")
    sys.exit()

# ==============================================================================
# MODULE 2: AI MENTOR ENGINE
# ==============================================================================
def call_openai_engine(prompt):
    """Gọi OpenAI để nhận xét code"""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    system_instruction = """
    Bạn là Mentor lập trình AI. Hãy nhận xét code ngắn gọn, dùng định dạng Markdown:
    1. Dùng Emoji đầu dòng (✅, ❌, 💡).
    2. Giải thích lỗi sai (nếu có).
    3. Gợi ý hướng sửa (KHÔNG viết code giải hoàn chỉnh).
    Cấu trúc: **📊 Đánh giá:** ... **❌ Vấn đề:** ... **💡 Gợi ý:** ...
    """

    payload = {
        "model": CURRENT_MODEL,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        elif response.status_code == 401: return "Lỗi Key OpenAI (401) - Kiểm tra lại Key."
        elif response.status_code == 429: return "Hết hạn mức OpenAI (Quota Exceeded)."
        else: return f"Lỗi OpenAI ({response.status_code}): {response.text}"
    except Exception as e:
        return f"Lỗi mạng khi gọi AI: {e}"

def compile_code(lang, filename, code):
    """Xử lý file code và biên dịch nếu cần"""
    if os.path.exists(filename): os.remove(filename)
    if os.path.exists(filename + ".exe"): os.remove(filename + ".exe")

    # Python
    if lang == 'python':
        with open(filename, "w", encoding="utf-8") as f: f.write(code)
        return [sys.executable, filename], None

    # C++
    elif lang == 'cpp':
        with open(filename + ".cpp", "w", encoding="utf-8") as f: f.write(code)
        # Lệnh biên dịch g++
        res = subprocess.run(["g++", filename + ".cpp", "-o", filename + ".exe"], capture_output=True, text=True)
        if res.returncode != 0: return None, res.stderr # Trả về lỗi biên dịch
        return [filename + ".exe"], None
    
    return None, "Ngôn ngữ chưa hỗ trợ"

def execute_and_grade(run_cmd, input_data, expected_output):
    """Chạy code với input và so sánh output"""
    try:
        if input_data is None: input_data = ""
        
        process = subprocess.run(
            run_cmd,
            input=str(input_data),
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=3
        )
        
        actual = process.stdout.strip()
        expected = str(expected_output).strip()

        if process.stderr: 
            return 0, f"Runtime Error: {process.stderr}"
        
        if actual == expected: 
            return 100, "Chính xác tuyệt đối!"
        else: 
            short_actual = (actual[:50] + '...') if len(actual) > 50 else actual
            return 0, f"Sai kết quả.\nInput: {input_data}\nOutput của bạn: {short_actual}\nĐáp án đúng: {expected}"

    except subprocess.TimeoutExpired: return 0, "Time Limit Exceeded (Chạy quá 3s)"
    except Exception as e: return 0, f"Lỗi hệ thống chấm: {e}"
def process_submission_queue(table_name):
    """
    Hàm xử lý chung cho cả Practice và Contest.
    table_name: 'submissions' hoặc 'contest_submissions'
    """
    data_dict = db.reference(table_name).get()
    
    if not data_dict: return

    for key, val in data_dict.items():
        if isinstance(val, dict) and val.get('status') == 'pending':
            
            mode_prefix = "[THI ĐẤU]" if table_name == 'contest_submissions' else "[LUYỆN TẬP]"
            print(f"{mode_prefix} ⚖️ Đang chấm bài {key} của {val.get('name')}...")
            lang = val.get('language')
            code = val.get('code')
            prob_id = val.get('problem_id')

            cmd, err = compile_code(lang, f"temp_{key}", code)
            
            if err:
                db.reference(f'{table_name}/{key}').update({
                    'status': 'completed', 'score': 0, 'message': f"Lỗi biên dịch:\n{err}"
                })
                print("   -> ❌ Lỗi biên dịch.")
                continue

            problem_data = db.reference(f'problems/{prob_id}').get()

            if not problem_data or 'testcases' not in problem_data:
                msg = f"Lỗi: Không tìm thấy dữ liệu bài tập '{prob_id}' trên hệ thống."
                db.reference(f'{table_name}/{key}').update({
                    'status': 'completed', 'score': 0, 'message': msg
                })
                print(f"   -> ❌ Không thấy đề bài {prob_id}")
                continue

            # 4. Chấm điểm từng Test Case
            test_cases = problem_data['testcases']
            total_tests = len(test_cases)
            passed_tests = 0
            first_error_msg = ""

            print(f"   -> Tìm thấy {total_tests} test cases.")

            for idx, test in enumerate(test_cases):
                inp = test.get('input', "")
                out = test.get('output', "")
                
                score_case, msg_case = execute_and_grade(cmd, inp, out)
                
                if score_case == 100:
                    passed_tests += 1
                elif not first_error_msg:
                    first_error_msg = f"Test #{idx+1}: {msg_case}"

            if total_tests > 0:
                final_score = int((passed_tests / total_tests) * 100)
            else:
                final_score = 0
            
            final_msg = f"Đúng {passed_tests}/{total_tests} test cases."
            if first_error_msg: final_msg += f"\n{first_error_msg}"

            db.reference(f'{table_name}/{key}').update({
                'status': 'completed',
                'score': final_score,
                'message': final_msg
            })
            print(f"   -> ✅ Kết quả: {final_score} điểm.")

            try: os.remove(f"temp_{key}")
            except: pass


def main():
    print(f"\n🚀 SERVER START (Mode: Independent Scoring)")
    print(f"🔧 AI Model: {CURRENT_MODEL}")
    print("="*50)

    while True:
        try:
            ai_reqs = db.reference('ai_requests').get()
            if ai_reqs:
                for key, val in ai_reqs.items():
                    if isinstance(val, dict) and val.get('status') == 'pending':
                        user = val.get('name', 'User')
                        print(f"[AI] 🧠 Đang suy nghĩ cho {user}...")
                        db.reference(f'ai_requests/{key}').update({'status': 'processing'})
                        
                        full_prompt = f"Đề bài: {val.get('problem_desc', '')}\nCode học sinh:\n{val.get('code', '')}"
                        reply = call_openai_engine(full_prompt)
                        
                        db.reference(f'ai_requests/{key}').update({'status': 'completed', 'response': reply})
                        print(f"   -> Xong AI.")

            process_submission_queue('submissions')

            process_submission_queue('contest_submissions')
            
            time.sleep(1.5)

        except KeyboardInterrupt:
            print("\n🛑 Server đã dừng.")
            break
        except Exception as e:
            print(f"❌ Lỗi vòng lặp chính: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()