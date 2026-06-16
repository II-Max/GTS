import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services.firebase_service import FirebaseService
from firebase_admin import auth

def fix_avatars():
    print("Khởi tạo Firebase...")
    fb = FirebaseService()
    fb.initialize()
    
    print("Lấy danh sách users từ Firebase Auth...")
    auth_users = auth.list_users().iterate_all()
    
    auth_dict = {}
    for user in auth_users:
        auth_dict[user.uid] = user.photo_url
        
    print("Lấy danh sách users từ Realtime Database...")
    db_users = fb.get_data("users")
    
    if not db_users:
        print("Không có users!")
        return
        
    for uid, data in db_users.items():
        if not isinstance(data, dict):
            continue
            
        current_avatar = data.get('avatar', '')
        auth_avatar = auth_dict.get(uid)
        
        if not current_avatar and auth_avatar:
            print(f"Cập nhật avatar cho: {data.get('name', uid)}")
            fb.update(f"users/{uid}", {
                "avatar": auth_avatar
            })
            
            # Cập nhật public_leaderboard luôn
            score = data.get("score", 0)
            problems_solved = data.get("problems_solved", 0)
            display_name = data.get("display_name") or data.get("name") or "Ẩn danh"
            fb.update_public_leaderboard(uid, display_name, score, problems_solved, auth_avatar)

    print("Hoàn tất cập nhật avatar!")

if __name__ == "__main__":
    fix_avatars()
