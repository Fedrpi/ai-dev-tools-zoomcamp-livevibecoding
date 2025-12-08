"""
Error schemas
"""

from typing import Any

from pydantic import BaseModel, Field


class Error(BaseModel):
    """Error response model"""

    error: str = Field(..., example="ValidationError")
    message: str = Field(..., example="Name must be at least 3 characters")
    details: dict[str, Any] | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "ValidationError",
                    "message": "Name must be at least 3 characters",
                    "details": None,
                }
            ]
        }
    }
