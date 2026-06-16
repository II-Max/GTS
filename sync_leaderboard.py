import os
import sys
import logging

logging.basicConfig(level=logging.WARNING)

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services.firebase_service import FirebaseService

def resync_all_scores():
    print("Khởi tạo Firebase...")
    fb = FirebaseService()
    fb.initialize()
    
    print("Lấy danh sách users...")
    users = fb.get_data("users")
    if not users:
        print("Không có users!")
        return
        
    for uid, data in users.items():
        if not isinstance(data, dict):
            continue
            
        role = data.get('role', 'student')
        if role == 'teacher':
            continue
            
        name = data.get('display_name') or data.get('name') or 'Unknown'
        print(f"Đang tính lại điểm cho: {name} (UID: {uid})")
        score = fb.recalculate_user_score(uid)
        print(f" => Tổng điểm: {score}")

    print("Hoàn tất tính điểm!")

if __name__ == "__main__":
    resync_all_scores()
