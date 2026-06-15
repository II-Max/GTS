"""
NEO Online Judge - Data Models
Typed models for submissions, problems, and AI requests.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class TestCase:
    """A single test case for a problem."""
    input: str
    output: str
    description: str = ""


@dataclass
class Problem:
    """A coding problem."""
    id: str
    title: str
    description: str
    level: str  # "dễ", "trung bình", "khó"
    language_support: List[str]
    test_cases: List[TestCase]
    tags: List[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Submission:
    """A code submission from a user."""
    id: str
    user_id: str
    problem_id: str
    code: str
    language: str
    status: str = "pending"  # pending, processing, completed, error
    score: int = 0
    message: str = ""
    created_at: str = ""
    is_contest: bool = False
    contest_id: Optional[str] = None

    @classmethod
    def from_firebase(cls, key: str, data: dict) -> "Submission":
        """Create a Submission from Firebase data."""
        return cls(
            id=key,
            user_id=data.get("user_id", ""),
            problem_id=data.get("problem_id", ""),
            code=data.get("code", ""),
            language=data.get("language", "python"),
            status=data.get("status", "pending"),
            score=data.get("score", 0),
            message=data.get("message", ""),
            created_at=data.get("created_at", ""),
            is_contest=data.get("is_contest", False),
            contest_id=data.get("contest_id"),
        )


@dataclass
class AIRequest:
    """A request to the AI Mentor."""
    id: str
    user_id: str
    problem_desc: str
    code: str
    status: str = "pending"  # pending, processing, completed, error
    response: str = ""
    created_at: str = ""

    @classmethod
    def from_firebase(cls, key: str, data: dict) -> "AIRequest":
        return cls(
            id=key,
            user_id=data.get("user_id", ""),
            problem_desc=data.get("problem_desc", ""),
            code=data.get("code", ""),
            status=data.get("status", "pending"),
            response=data.get("response", ""),
            created_at=data.get("created_at", ""),
        )


@dataclass
class GradingResult:
    """Result of grading a submission."""
    score: int
    passed: int
    total: int
    summary: str
    messages: List[Dict[str, Any]]
