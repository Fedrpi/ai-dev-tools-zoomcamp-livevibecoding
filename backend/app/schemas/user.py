"""
User schema
"""

from typing import Literal

from pydantic import BaseModel, Field


class User(BaseModel):
    """User model for interviewer or candidate"""

    name: str = Field(..., min_length=3, example="John Doe")
    role: Literal["interviewer", "candidate"] = Field(..., example="interviewer")

    model_config = {
        "json_schema_extra": {"examples": [{"name": "John Doe", "role": "interviewer"}]}
    }
