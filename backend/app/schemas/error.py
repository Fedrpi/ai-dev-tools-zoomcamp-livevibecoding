"""
Error schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Error(BaseModel):
    """Error response model"""

    error: str = Field(..., example="ValidationError")
    message: str = Field(..., example="Name must be at least 3 characters")
    details: Optional[Dict[str, Any]] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "ValidationError",
                    "message": "Name must be at least 3 characters",
                    "details": None
                }
            ]
        }
    }
