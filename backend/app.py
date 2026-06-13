"""
NEO Online Judge - Application Entry Point
Modern async-compatible judge server with modular architecture.
"""

import sys
import time
from typing import Optional

from config.settings import settings
from config.logging import setup_logging

logger = setup_logging()


class JudgeApplication:
    """
    Main application that orchestrates:
    1. Firebase polling for pending submissions
    2. Code compilation and grading
    3. AI Mentor request processing
    """

    def __init__(self):
        self.running = False
        self._firebase = None
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

        # Step 1: Compile
        cmd, err = Compiler.compile(submission.language, f"temp_{key}", submission.code)
        if err:
            self._firebase.update_submission(table, key, 0, f"Compilation Error:\n{err}")
            logger.warning(f"Submission {key}: Compilation failed")
            Compiler.cleanup(f"temp_{key}")
            return

        # Step 2: Get problem test cases
        problem = self._firebase.get_problem(submission.problem_id)
        if not problem or "testcases" not in problem:
            self._firebase.update_submission(
                table, key, 0,
                f"Error: Problem '{submission.problem_id}' not found or has no test cases."
            )
            logger.warning(f"Submission {key}: Problem {submission.problem_id} not found")
            Compiler.cleanup(f"temp_{key}")
            return

        # Step 3: Grade
        result = JudgeEngine.grade_all(cmd, problem["testcases"], timeout=settings.JUDGE_TIMEOUT)
        self._firebase.update_submission(table, key, result["score"], result["summary"])

        logger.info(f"Submission {key}: {result['passed']}/{result['total']} passed (score: {result['score']})")
        Compiler.cleanup(f"temp_{key}")

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
    # MAIN LOOP
    # ======================================================================

    def run(self):
        """Start the main polling loop."""
        self.running = True

        print(f"""
╔══════════════════════════════════════════════════╗
║              NEO ONLINE JUDGE v2.0               ║
║          Online Code Judge + AI Mentor           ║
╠══════════════════════════════════════════════════╣
║  Mode:          Independent Scoring              ║
║  AI Model:      {settings.AI_MODEL:<34}║
║  Poll Interval: {settings.POLL_INTERVAL}s                               ║
║  Judge Timeout: {settings.JUDGE_TIMEOUT}s                               ║
║  Log Level:     {settings.LOG_LEVEL:<34}║
╚══════════════════════════════════════════════════╝
        """)

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
        logger.info("NEO Online Judge shutdown complete.")
        print("\n🛑 Server stopped.")


def main():
    app = JudgeApplication()
    app.run()


if __name__ == "__main__":
    main()
