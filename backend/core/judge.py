"""
NEO Online Judge - Judge Engine
Core grading logic: executes code against test cases and scores results.
"""

import subprocess
import logging
from typing import Tuple, List, Dict, Any

from backend.core.compiler import Compiler, CompilerError

logger = logging.getLogger("neo")


class JudgeEngine:
    """
    Core engine that grades code submissions by:
    1. Compiling the code using Compiler
    2. Running each test case against the compiled/interpreted code
    3. Comparing outputs and calculating scores
    """

    @staticmethod
    def execute_code(run_cmd: list, input_data: str, timeout: int) -> Tuple[int, str, str]:
        """
        Execute compiled code with given input.
        
        Args:
            run_cmd: Command list to run (e.g., ["python", "file.py"])
            input_data: Input string to pass to stdin
            timeout: Execution timeout in seconds
            
        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        process = subprocess.run(
            run_cmd,
            input=str(input_data) if input_data else "",
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
        )
        return process.returncode, process.stdout.strip(), process.stderr.strip()

    @staticmethod
    def grade_test_case(run_cmd: list, test_input: str, expected_output: str, timeout: int) -> Tuple[float, str]:
        """
        Grade a single test case.
        
        Returns:
            Tuple of (score: 0.0 or 100.0, message)
        """
        try:
            retcode, actual_output, stderr = JudgeEngine.execute_code(run_cmd, test_input, timeout)

            if stderr:
                return 0.0, f"Runtime Error:\n{stderr}"

            actual = actual_output.strip()
            expected = str(expected_output).strip()

            if actual == expected:
                return 100.0, "Passed"
            else:
                actual_short = (actual[:80] + "...") if len(actual) > 80 else actual
                return 0.0, (
                    f"Wrong Answer.\n"
                    f"Input:    {test_input}\n"
                    f"Expected: {expected}\n"
                    f"Got:      {actual_short}"
                )

        except subprocess.TimeoutExpired:
            return 0.0, f"Time Limit Exceeded (>{timeout}s)"
        except Exception as e:
            logger.error(f"Grading error: {e}", exc_info=True)
            return 0.0, f"System Error: {str(e)}"

    @staticmethod
    def grade_all(
        run_cmd: list,
        test_cases: List[Dict[str, Any]],
        timeout: int = 3,
    ) -> Dict[str, Any]:
        """
        Grade all test cases for a submission.
        
        Args:
            run_cmd: Command to execute the code
            test_cases: List of {"input": ..., "output": ...} dicts
            timeout: Per-test-case timeout
            
        Returns:
            Dict with: score, passed, total, messages (list), first_error
        """
        total = len(test_cases)
        passed = 0
        messages = []
        first_error = ""

        for idx, tc in enumerate(test_cases):
            inp = tc.get("input", "")
            out = tc.get("output", "")
            score, msg = JudgeEngine.grade_test_case(run_cmd, inp, out, timeout)

            if score == 100.0:
                passed += 1
            elif not first_error:
                first_error = f"Test #{idx + 1}: {msg}"

            messages.append({
                "test_index": idx,
                "passed": score == 100.0,
                "message": msg,
            })

        final_score = int((passed / total) * 100) if total > 0 else 0
        summary = f"Passed {passed}/{total} test cases."
        if first_error:
            summary += f"\n{first_error}"

        return {
            "score": final_score,
            "passed": passed,
            "total": total,
            "summary": summary,
            "messages": messages,
        }
