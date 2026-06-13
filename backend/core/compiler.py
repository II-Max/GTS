"""
NEO Online Judge - Compiler Manager
Handles code compilation and execution for multiple programming languages.
"""

import os
import re
import subprocess
import sys
import logging
from typing import Optional, Tuple

logger = logging.getLogger("neo")


class CompilerError(Exception):
    """Raised when code compilation or execution fails."""
    pass


class Compiler:
    """
    Manages compilation and execution for supported programming languages.
    
    Supported languages:
        - Python (interpreted)
        - C++ (compiled with g++)
        - C (compiled with gcc)
        - Java (compiled with javac)
        - JavaScript (interpreted with Node.js)
    """

    TIMEOUT = 3  # Default execution timeout in seconds

    SUPPORTED_LANGUAGES = {
        "python": {"extension": ".py", "compiler": None, "runner": sys.executable},
        "cpp": {"extension": ".cpp", "compiler": "g++", "runner": None, "flags": ["-std=c++17"]},
        "c": {"extension": ".c", "compiler": "gcc", "runner": None, "flags": ["-std=c11"]},
        "java": {"extension": ".java", "compiler": "javac", "runner": "java"},
        "javascript": {"extension": ".js", "compiler": None, "runner": "node"},
    }

    @classmethod
    def is_supported(cls, lang: str) -> bool:
        """Check if a language is supported."""
        return lang.lower() in cls.SUPPORTED_LANGUAGES

    @classmethod
    def compile_python(cls, filename: str, code: str) -> Tuple[Optional[list], Optional[str]]:
        """Python: interpreted, write file and return run command."""
        filepath = f"{filename}.py"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        return [sys.executable, filepath], None

    @classmethod
    def compile_cpp(cls, filename: str, code: str) -> Tuple[Optional[list], Optional[str]]:
        """C++: compile with g++."""
        src = f"{filename}.cpp"
        out = f"{filename}.exe"
        with open(src, "w", encoding="utf-8") as f:
            f.write(code)

        result = subprocess.run(
            ["g++", src, "-o", out, "-std=c++17"],
            capture_output=True, text=True, timeout=cls.TIMEOUT,
        )
        if result.returncode != 0:
            return None, result.stderr
        return [out], None

    @classmethod
    def compile_c(cls, filename: str, code: str) -> Tuple[Optional[list], Optional[str]]:
        """C: compile with gcc."""
        src = f"{filename}.c"
        out = f"{filename}.exe"
        with open(src, "w", encoding="utf-8") as f:
            f.write(code)

        result = subprocess.run(
            ["gcc", src, "-o", out, "-std=c11"],
            capture_output=True, text=True, timeout=cls.TIMEOUT,
        )
        if result.returncode != 0:
            return None, result.stderr
        return [out], None

    @classmethod
    def compile_java(cls, filename: str, code: str) -> Tuple[Optional[list], Optional[str]]:
        """Java: compile with javac, extract class name."""
        match = re.search(r"public\s+class\s+(\w+)", code)
        class_name = match.group(1) if match else "Main"

        src = f"{class_name}.java"
        with open(src, "w", encoding="utf-8") as f:
            f.write(code)

        result = subprocess.run(
            ["javac", src],
            capture_output=True, text=True, timeout=cls.TIMEOUT,
        )
        if result.returncode != 0:
            return None, result.stderr
        return ["java", "-cp", ".", class_name], None

    @classmethod
    def compile_javascript(cls, filename: str, code: str) -> Tuple[Optional[list], Optional[str]]:
        """JavaScript: run with Node.js."""
        filepath = f"{filename}.js"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        return ["node", filepath], None

    @classmethod
    def compile(cls, lang: str, filename: str, code: str, timeout: int = None) -> Tuple[Optional[list], Optional[str]]:
        """
        Compile/interpret code for the given language.
        
        Args:
            lang: Programming language name
            filename: Base filename (without extension)
            code: Source code string
            timeout: Execution timeout in seconds
            
        Returns:
            Tuple of (run_command_list, error_message)
            - If successful: (["python", "file.py"], None)
            - If failed: (None, "error message")
        """
        if timeout:
            cls.TIMEOUT = timeout

        lang = lang.lower()
        if not cls.is_supported(lang):
            return None, f"Unsupported language: '{lang}'. Supported: {', '.join(cls.SUPPORTED_LANGUAGES.keys())}"

        compilers = {
            "python": cls.compile_python,
            "cpp": cls.compile_cpp,
            "c": cls.compile_c,
            "java": cls.compile_java,
            "javascript": cls.compile_javascript,
        }

        return compilers[lang](filename, code)

    @classmethod
    def cleanup(cls, filename: str):
        """Remove temporary files created during compilation."""
        extensions = [".py", ".cpp", ".c", ".java", ".js", ".exe", ".class"]
        for ext in extensions:
            path = f"{filename}{ext}"
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass
