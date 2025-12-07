"""
Session schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
from .user import User
from .problem import Problem


class SessionCreate(BaseModel):
    """Schema for creating a new session"""

    interviewerName: str = Field(..., min_length=3, example="John Doe")
    difficulty: Literal["junior", "middle", "senior"] = Field(..., example="junior")
    language: Literal["python"] = Field(..., example="python")
    numberOfProblems: int = Field(..., ge=1, le=5, example=3)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "interviewerName": "John Doe",
                    "difficulty": "junior",
                    "language": "python",
                    "numberOfProblems": 3
                }
            ]
        }
    }


class SessionInfo(BaseModel):
    """Limited session info for candidate join page"""

    id: str = Field(..., example="sess_abc123")
    difficulty: str = Field(..., example="junior")
    language: str = Field(..., example="python")
    numberOfProblems: int = Field(..., example=3)
    interviewer: dict = Field(
        ...,
        example={"name": "John Doe"}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "sess_abc123",
                    "difficulty": "junior",
                    "language": "python",
                    "numberOfProblems": 3,
                    "interviewer": {"name": "John Doe"}
                }
            ]
        }
    }


class Session(BaseModel):
    """Full session model"""

    id: str = Field(..., example="sess_abc123")
    difficulty: Literal["junior", "middle", "senior"] = Field(..., example="junior")
    language: Literal["python"] = Field(..., example="python")
    numberOfProblems: int = Field(..., example=3)
    problems: List[Problem] = Field(default_factory=list)
    interviewer: User
    candidate: Optional[User] = None
    status: Literal["waiting", "active", "ended"] = Field(..., example="waiting")
    createdAt: datetime = Field(default_factory=datetime.now)
    endedAt: Optional[datetime] = None

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": "sess_abc123",
                    "difficulty": "junior",
                    "language": "python",
                    "numberOfProblems": 3,
                    "problems": [],
                    "interviewer": {"name": "John Doe", "role": "interviewer"},
                    "candidate": None,
                    "status": "waiting",
                    "createdAt": "2025-12-06T10:00:00Z",
                    "endedAt": None
                }
            ]
        }
    }
