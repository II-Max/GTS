"""
GTS (Go to Success) - Application Entry Point
Modern async-compatible judge server with modular architecture.
Includes HTTP API server for authentication and user management.
"""

import sys
import time
import threading
from typing import Optional

from flask import Flask
from flask_cors import CORS

from backend.config.settings import settings
from backend.config.logging import setup_logging

logger = setup_logging()

# ======================================================================
# Flask API Server
# ======================================================================

def create_api_app() -> Flask:
    """Create and configure the Flask API application."""
    app = Flask(__name__)
    CORS(app, origins=settings.ALLOWED_ORIGINS)

    # Register blueprints
    from backend.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from backend.routes.playground_routes import playground_bp
    app.register_blueprint(playground_bp)

    # Health check
    @app.route("/api/health")
    def health():
        return {"status": "ok", "service": "GTS", "version": "2.0"}

    # Platform Stats
    _stats_cache = {}
    _stats_cache_time = 0

    @app.route("/api/stats")
    def get_stats():

        nonlocal _stats_cache_time, _stats_cache
        current_time = time.time()

        # Cache for 60 seconds to prevent O(N) database reads
        if current_time - _stats_cache_time < 60 and _stats_cache:
            return _stats_cache

        try:
            from backend.services.firebase_service import FirebaseService
            fb = FirebaseService()
            p = fb.get_data("problems")
            u = fb.get_data("users")
            s = fb.get_data("submissions")

            _stats_cache = {
                "problems": len(p) if p else 0,
                "users": len(u) if u else 0,
                "submissions": len(s) if s else 0
            }
            _stats_cache_time = current_time
            return _stats_cache
        except Exception as e:
            return {"problems": 0, "users": 0, "submissions": 0}

    return app


class JudgeApplication:
    """
    Main application that orchestrates:
    1. HTTP API server (Flask) for auth & user management
    2. Firebase polling for pending submissions
    3. Code compilation and grading
    4. AI Mentor request processing
    """

    def __init__(self):
        self.running = False
        self._firebase = None
        self._api_app = create_api_app()
        self._init_services()

    def _init_services(self):
        """Initialize backend services."""
        try:
            from backend.services.firebase_service import FirebaseService
            self._firebase = FirebaseService()
            self._firebase.initialize()
        except Exception as e:
            logger.critical(f"Failed to initialize services: {e}")
            sys.exit(1)

    # ======================================================================
    # POLLING LOOP: Process pending submissions
    # ======================================================================

    def _process_submissions(self, table: str = "submissions"):
        """Process all pending submissions from a Firebase table."""
        pending = self._firebase.get_pending_submissions(table)
        if not pending:
            return

        mode = "[CONTEST]" if table == "contest_submissions" else "[PRACTICE]"
        logger.info(f"{mode} Processing {len(pending)} pending submission(s)...")

        for key, data in pending:
            self._process_single_submission(key, data, table)

    def _process_single_submission(self, key: str, data: dict, table: str):
        """Grade a single submission."""
        from backend.models.submission import Submission
        from backend.core.compiler import Compiler
        from backend.core.judge import JudgeEngine

        submission = Submission.from_firebase(key, data)
        logger.info(f"Grading submission {key} ({submission.language}) for problem {submission.problem_id}")

        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Step 1: Compile
            cmd, err = Compiler.compile(submission.language, f"main", submission.code, temp_dir)
            if err:
                self._firebase.update_submission(table, key, 0, f"Compilation Error:\n{err}")
                logger.warning(f"Submission {key}: Compilation failed")
                return

            # Step 2: Get problem test cases
            problem = self._firebase.get_problem(submission.problem_id)
            if not problem or "testcases" not in problem:
                self._firebase.update_submission(
                    table, key, 0,
                    f"Error: Problem '{submission.problem_id}' not found or has no test cases."
                )
                logger.warning(f"Submission {key}: Problem {submission.problem_id} not found")
                return

            # Step 3: Grade
            result = JudgeEngine.grade_all(cmd, problem["testcases"], timeout=settings.JUDGE_TIMEOUT)
            self._firebase.update_submission(table, key, result["score"], result["summary"])

            logger.info(f"Submission {key}: {result['passed']}/{result['total']} passed (score: {result['score']})")

        # Step 4: Cap nhat diem va public leaderboard
        try:
            uid = data.get("uid", "")
            if uid and result["score"] >= 0:
                self._firebase.recalculate_user_score(uid)
        except Exception as e:
            logger.warning(f"Could not update user score: {e}")

    # ======================================================================
    # POLLING LOOP: Process AI requests
    # ======================================================================

    def _process_ai_requests(self):
        """Process all pending AI mentor requests."""
        pending = self._firebase.get_pending_ai_requests()
        if not pending:
            return

        logger.info(f"[AI] Processing {len(pending)} pending request(s)...")

        for key, data in pending:
            from backend.services.ai_service import AIService

            user = data.get("name", "User")
            logger.info(f"[AI] Analyzing code for {user}...")

            self._firebase.mark_ai_processing(key)

            result = AIService.review_code(
                code=data.get("code", ""),
                problem_description=data.get("problem_desc", ""),
            )

            self._firebase.update_ai_request(
                key,
                status="completed",
                response=result["response"],
            )
            logger.info(f"[AI] Completed for {user} (success={result['success']})")

    # ======================================================================
    # HTTP API Server (chạy trên thread riêng)
    # ======================================================================

    def _run_api_server(self):
        """Start Flask API server in a separate thread."""
        logger.info(f"API server starting on {settings.HOST}:{settings.PORT}")
        self._api_app.run(
            host=settings.HOST,
            port=settings.PORT,
            debug=False,
            use_reloader=False,
        )

    # ======================================================================
    # MAIN LOOP
    # ======================================================================

    def run(self):
        """Start the judge server and API server."""
        self.running = True

        print(f"""
╔══════════════════════════════════════════════════╗
║         GTS — Go to Success  v2.0                ║
║          Online Code Judge + AI Mentor           ║
╠══════════════════════════════════════════════════╣
║  Mode:          Independent Scoring              ║
║  AI Model:      {settings.AI_MODEL:<34}║
║  API Server:    {settings.HOST}:{settings.PORT:<28}║
║  Poll Interval: {settings.POLL_INTERVAL}s                               ║
║  Judge Timeout: {settings.JUDGE_TIMEOUT}s                               ║
║  Log Level:     {settings.LOG_LEVEL:<34}║
╚══════════════════════════════════════════════════╝
        """)

        # Start API server in background thread
        api_thread = threading.Thread(target=self._run_api_server, daemon=True)
        api_thread.start()

        # Main polling loop
        try:
            while self.running:
                self._process_ai_requests()
                self._process_submissions("submissions")
                self._process_submissions("contest_submissions")
                time.sleep(settings.POLL_INTERVAL)
        except KeyboardInterrupt:
            logger.info("Server stopped by user.")
            self.shutdown()
        except Exception as e:
            logger.critical(f"Main loop error: {e}", exc_info=True)
            self.shutdown()

    def shutdown(self):
        """Gracefully shut down the application."""
        self.running = False
        logger.info("GTS shutdown complete.")
        print("\n🛑 Server stopped.")


def main():
    app = JudgeApplication()
    app.run()


if __name__ == "__main__":
    main()
