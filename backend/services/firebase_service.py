"""
GTS (Go to Success) - Firebase Service
Handles all Firebase Realtime Database operations.
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, db

from backend.config.settings import settings

logger = logging.getLogger("neo")


class FirebaseService:
    """Singleton service for Firebase operations."""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self):
        """Initialize Firebase app (idempotent)."""
        if self._initialized:
            return

        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(settings.CRED_PATH)
                firebase_admin.initialize_app(cred, {"databaseURL": settings.DB_URL})
            self._initialized = True
            logger.info("Firebase connection established.")
        except FileNotFoundError:
            logger.error(f"Credential file not found: {settings.CRED_PATH}")
            raise
        except Exception as e:
            logger.error(f"Firebase initialization failed: {e}", exc_info=True)
            raise

    # ---- Generic operations ----

    def get_data(self, path: str, shallow: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get all data at a database path.
        ⚡ Bolt: Added shallow parameter for performance optimization.
        """
        try:
            return db.reference(path).get(shallow=shallow)
        except Exception as e:
            logger.error(f"Error reading {path}: {e}")
            return None

    def get_child(self, path: str, key: str) -> Optional[Dict[str, Any]]:
        """Get a specific child node."""
        try:
            return db.reference(f"{path}/{key}").get()
        except Exception as e:
            logger.error(f"Error reading {path}/{key}: {e}")
            return None

    def update(self, path: str, data: Dict[str, Any]):
        """Update data at a path."""
        try:
            db.reference(path).update(data)
        except Exception as e:
            logger.error(f"Error updating {path}: {e}")
            raise

    def push(self, path: str, data: Dict[str, Any]) -> Optional[str]:
        """Push new data and return the generated key."""
        try:
            ref = db.reference(path).push(data)
            return ref.key
        except Exception as e:
            logger.error(f"Error pushing to {path}: {e}")
            return None

    # ---- Domain-specific operations ----

    def get_pending_submissions(self, table: str = "submissions") -> List[tuple]:
        """
        Fetch all pending submissions from a table.

        Returns:
            List of (key, data) tuples
        """
        try:
            data = (
                db.reference(table)
                .order_by_child("status")
                .equal_to("pending")
                .get()
            )
        except Exception as e:
            logger.warning(f"Indexed query failed for {table}, falling back: {e}")
            data = self.get_data(table)

        if not data:
            return []

        pending = []
        for key, val in data.items():
            if isinstance(val, dict) and val.get("status") == "pending":
                pending.append((key, val))
        return pending

    def update_submission(self, table: str, key: str, score: int, message: str, status: str = "completed"):
        """Update a submission with grading results."""
        self.update(f"{table}/{key}", {
            "status": status,
            "score": score,
            "message": message,
        })

    def get_problem(self, problem_id: str) -> Optional[Dict[str, Any]]:
        """Get problem data with test cases."""
        return self.get_child("problems", problem_id)

    def get_pending_ai_requests(self) -> List[tuple]:
        """Fetch pending AI mentor requests."""
        try:
            data = (
                db.reference("ai_requests")
                .order_by_child("status")
                .equal_to("pending")
                .get()
            )
        except Exception as e:
            logger.warning(f"Indexed query failed for ai_requests, falling back: {e}")
            data = self.get_data("ai_requests")

        if not data:
            return []

        pending = []
        for key, val in data.items():
            if isinstance(val, dict) and val.get("status") == "pending":
                pending.append((key, val))
        return pending

    def update_ai_request(self, key: str, status: str, response: str = ""):
        """Update an AI request with the response."""
        update_data = {"status": status}
        if response:
            update_data["response"] = response
        self.update(f"ai_requests/{key}", update_data)

    def mark_ai_processing(self, key: str):
        """Mark an AI request as being processed."""
        self.update(f"ai_requests/{key}", {"status": "processing"})

    def update_public_leaderboard(self, uid: str, display_name: str, score: int, problems_solved: int, avatar: str = ""):
        """
        Ghi thong tin diem so vao node public_leaderboard (doc duoc boi moi nguoi).
        Chi chua thong tin public — KHONG chua email, uid cu the hay thong tin nhay cam.
        Backend duoc goi sau moi lan cham bai hoan thanh.
        """
        try:
            self.update(f"public_leaderboard/{uid}", {
                "display_name": display_name,
                "avatar": avatar,
                "score": score,
                "problems_solved": problems_solved,
                "updated_at": datetime.now().isoformat(),
            })
        except Exception as e:
            logger.error(f"Error updating public_leaderboard for {uid}: {e}")

    def recalculate_user_score(self, uid: str):
        """Tính lại tổng điểm và số bài hoàn thành của user từ submissions, sau đó cập nhật vào users và public_leaderboard."""
        try:
            user = self.get_child("users", uid) or {}
            
            # Lấy tất cả bài nộp của user
            subs = db.reference("submissions").order_by_child("uid").equal_to(uid).get()
            
            problem_scores = {}
            if subs:
                for sub_id, sub_data in subs.items():
                    if isinstance(sub_data, dict) and sub_data.get("status") == "completed":
                        pid = sub_data.get("problem_id")
                        score = int(sub_data.get("score", 0))
                        if pid and score > problem_scores.get(pid, 0):
                            problem_scores[pid] = score
                            
            total_score = sum(problem_scores.values())
            problems_solved = sum(1 for s in problem_scores.values() if s == 100)
            
            # Cập nhật vào node users
            self.update(f"users/{uid}", {
                "score": total_score,
                "problems_solved": problems_solved
            })
            
            # Cập nhật public_leaderboard
            display_name = user.get("display_name") or user.get("name") or "Ẩn danh"
            avatar = user.get("avatar", "")
            
            self.update_public_leaderboard(uid, display_name, total_score, problems_solved, avatar)
            return total_score
        except Exception as e:
            logger.warning(f"Error recalculating user score for {uid}: {e}")
