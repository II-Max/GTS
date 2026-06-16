"""
GTS (Go to Success) - Compiler Manager
Handles code compilation and execution for multiple programming languages.
"""

import os
import re
import subprocess
import sys
import logging
import shutil
import glob
import ast
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

    COMPILE_TIMEOUT = 10  # Longer timeout for compilation (e.g. Windows Defender, lazy loading)

    SUPPORTED_LANGUAGES = {
        "python": {"extension": ".py", "compiler": None, "runner": sys.executable},
        "cpp": {"extension": ".cpp", "compiler": "g++", "runner": None, "flags": ["-std=c++17"]},
        "c": {"extension": ".c", "compiler": "gcc", "runner": None, "flags": ["-std=c11"]},
        "java": {"extension": ".java", "compiler": "javac", "runner": "java"},
        "javascript": {"extension": ".js", "compiler": None, "runner": "node"},
        "pascal": {"extension": ".pas", "compiler": "fpc", "runner": None},
    }

    @classmethod
    def is_supported(cls, lang: str) -> bool:
        """Check if a language is supported."""
        return lang.lower() in cls.SUPPORTED_LANGUAGES

    @classmethod
    def _resolve_executable(cls, name: str) -> str:
        """Find executable in PATH or fallback to known WinGet installation directories."""
        if shutil.which(name):
            return name
        
        # Fallback for Windows if not in PATH
        if sys.platform == "win32":
            local_app_data = os.environ.get("LOCALAPPDATA", "")
            prog_files = os.environ.get("ProgramFiles", "")
            
            if name in ["g++", "gcc", "node"]:
                base_path = os.path.join(local_app_data, "Microsoft", "WinGet", "Packages")
                if os.path.exists(base_path):
                    if name in ["g++", "gcc"]:
                        dirs = glob.glob(os.path.join(base_path, "BrechtSanders.WinLibs*"))
                        if dirs:
                            exe_path = os.path.join(dirs[0], "mingw64", "bin", f"{name}.exe")
                            if os.path.exists(exe_path):
                                return exe_path
                    elif name == "node":
                        dirs = glob.glob(os.path.join(base_path, "OpenJS.NodeJS*"))
                        if dirs:
                            exe_path = os.path.join(dirs[0], f"{name}.exe")
                            if os.path.exists(exe_path):
                                return exe_path
            
            elif name in ["javac", "java"]:
                prog_files_64 = os.environ.get("ProgramW6432", "C:\\Program Files")
                for p_files in [prog_files, prog_files_64]:
                    if os.path.exists(p_files):
                        eclipse_path = os.path.join(p_files, "Eclipse Adoptium")
                        if os.path.exists(eclipse_path):
                            dirs = glob.glob(os.path.join(eclipse_path, "jdk*"))
                            if dirs:
                                exe_path = os.path.join(dirs[0], "bin", f"{name}.exe")
                                if os.path.exists(exe_path):
                                    return exe_path

        return name

    @classmethod
    def check_security(cls, lang: str, code: str) -> Optional[str]:
        """Perform basic static analysis to block dangerous system calls."""
        lang = lang.lower()
        if lang == "python":
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name in ["os", "subprocess", "sys", "shutil", "pty", "socket"]:
                                return f"Security Policy: module '{alias.name}' is blocked."
                    elif isinstance(node, ast.ImportFrom):
                        if node.module in ["os", "subprocess", "sys", "shutil", "pty", "socket"]:
                            return f"Security Policy: module '{node.module}' is blocked."
                    elif isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name):
                            if node.func.id in ["eval", "exec", "open", "compile"]:
                                return f"Security Policy: function '{node.func.id}' is blocked."
            except SyntaxError as e:
                return f"Syntax Error: {e}"
        elif lang in ["cpp", "c"]:
            dangerous_patterns = ["system(", "popen(", "fork(", "exec(", "<windows.h>", "<unistd.h>"]
            for pattern in dangerous_patterns:
                if pattern in code:
                    return f"Security Policy: '{pattern}' is blocked."
        elif lang == "java":
            dangerous_patterns = ["Runtime.getRuntime().exec", "ProcessBuilder", "java.io.File", "java.net."]
            for pattern in dangerous_patterns:
                if pattern in code:
                    return f"Security Policy: '{pattern}' is blocked."
        elif lang == "javascript":
            dangerous_patterns = ["require('child_process')", "require('fs')", "require('os')", "eval(", "setTimeout(", "setInterval("]
            for pattern in dangerous_patterns:
                if pattern in code:
                    return f"Security Policy: '{pattern}' is blocked."
        return None

    @classmethod
    def compile_python(cls, filename: str, code: str, temp_dir: str) -> Tuple[Optional[list], Optional[str]]:
        """Python: interpreted, write file and return run command."""
        filepath = os.path.join(temp_dir, f"{filename}.py")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        return [sys.executable, filepath], None

    @classmethod
    def compile_cpp(cls, filename: str, code: str, temp_dir: str) -> Tuple[Optional[list], Optional[str]]:
        """C++: compile with g++."""
        src = os.path.join(temp_dir, f"{filename}.cpp")
        out = os.path.join(temp_dir, f"{filename}.exe")
        with open(src, "w", encoding="utf-8") as f:
            f.write(code)

        gpp = cls._resolve_executable("g++")
        try:
            result = subprocess.run(
                [gpp, src, "-o", out, "-std=c++17"],
                capture_output=True, text=True, errors="replace", timeout=cls.COMPILE_TIMEOUT,
            )
            if result.returncode != 0:
                return None, result.stderr
            return [out], None
        except FileNotFoundError:
            return None, "System Error: Compiler 'g++' not found."
        except subprocess.TimeoutExpired:
            return None, f"System Error: Compilation timed out after {cls.COMPILE_TIMEOUT} seconds."

    @classmethod
    def compile_c(cls, filename: str, code: str, temp_dir: str) -> Tuple[Optional[list], Optional[str]]:
        """C: compile with gcc."""
        src = os.path.join(temp_dir, f"{filename}.c")
        out = os.path.join(temp_dir, f"{filename}.exe")
        with open(src, "w", encoding="utf-8") as f:
            f.write(code)

        gcc = cls._resolve_executable("gcc")
        try:
            result = subprocess.run(
                [gcc, src, "-o", out, "-std=c11"],
                capture_output=True, text=True, errors="replace", timeout=cls.COMPILE_TIMEOUT,
            )
            if result.returncode != 0:
                return None, result.stderr
            return [out], None
        except FileNotFoundError:
            return None, "System Error: Compiler 'gcc' not found."
        except subprocess.TimeoutExpired:
            return None, f"System Error: Compilation timed out after {cls.COMPILE_TIMEOUT} seconds."

    @classmethod
    def compile_java(cls, filename: str, code: str, temp_dir: str) -> Tuple[Optional[list], Optional[str]]:
        """Java: compile with javac, extract class name."""
        match = re.search(r"public\s+class\s+(\w+)", code)
        class_name = match.group(1) if match else "Main"

        src = os.path.join(temp_dir, f"{class_name}.java")
        with open(src, "w", encoding="utf-8") as f:
            f.write(code)

        javac = cls._resolve_executable("javac")
        java = cls._resolve_executable("java")
        try:
            result = subprocess.run(
                [javac, src],
                capture_output=True, text=True, errors="replace", timeout=cls.COMPILE_TIMEOUT,
            )
            if result.returncode != 0:
                return None, result.stderr
            return [java, "-Dfile.encoding=UTF-8", "-cp", temp_dir, class_name], None
        except FileNotFoundError:
            return None, "System Error: Compiler 'javac' not found."
        except subprocess.TimeoutExpired:
            return None, f"System Error: Compilation timed out after {cls.COMPILE_TIMEOUT} seconds."

    @classmethod
    def compile_javascript(cls, filename: str, code: str, temp_dir: str) -> Tuple[Optional[list], Optional[str]]:
        """JavaScript: run with Node.js."""
        filepath = os.path.join(temp_dir, f"{filename}.js")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        node = cls._resolve_executable("node")
        return [node, filepath], None

    @classmethod
    def compile_pascal(cls, filename: str, code: str, temp_dir: str) -> Tuple[Optional[list], Optional[str]]:
        """Pascal: compile with Free Pascal (fpc)."""
        src = os.path.join(temp_dir, f"{filename}.pas")
        out = os.path.join(temp_dir, f"{filename}.exe")
        with open(src, "w", encoding="utf-8") as f:
            f.write(code)

        fpc = cls._resolve_executable("fpc")
        try:
            # fpc puts the output executable in the same directory as the source file
            result = subprocess.run(
                [fpc, src],
                capture_output=True, text=True, errors="replace", timeout=cls.COMPILE_TIMEOUT,
                cwd=temp_dir
            )
            if result.returncode != 0:
                # fpc usually writes errors to stdout instead of stderr
                error_msg = (result.stdout + "\n" + result.stderr).strip()
                return None, error_msg
            return [out], None
        except FileNotFoundError:
            return None, "System Error: Compiler 'fpc' not found. Please install Free Pascal and add it to PATH."
        except subprocess.TimeoutExpired:
            return None, f"System Error: Compilation timed out after {cls.COMPILE_TIMEOUT} seconds."

    @classmethod
    def compile(cls, lang: str, filename: str, code: str, temp_dir: str) -> Tuple[Optional[list], Optional[str]]:
        """
        Compile/interpret code for the given language.
        
        Args:
            lang: Programming language name
            filename: Base filename (without extension)
            code: Source code string
            temp_dir: Directory to write temp files to
            
        Returns:
            Tuple of (run_command_list, error_message)
        """
        lang = lang.lower()
        if not cls.is_supported(lang):
            return None, f"Unsupported language: '{lang}'. Supported: {', '.join(cls.SUPPORTED_LANGUAGES.keys())}"

        # Step 0: Security Check
        security_error = cls.check_security(lang, code)
        if security_error:
            return None, security_error

        compilers = {
            "python": cls.compile_python,
            "cpp": cls.compile_cpp,
            "c": cls.compile_c,
            "java": cls.compile_java,
            "javascript": cls.compile_javascript,
            "pascal": cls.compile_pascal,
        }

        return compilers[lang](filename, code, temp_dir)
