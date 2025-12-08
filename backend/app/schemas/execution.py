"""
Code execution schemas
"""

from pydantic import BaseModel, Field


class ExecutionResult(BaseModel):
    """Result of code execution"""

    success: bool = Field(..., example=True)
    output: str = Field(..., example="8\n0\n350\n")
    error: str | None = Field(None, example=None)

    model_config = {
        "json_schema_extra": {
            "examples": [{"success": True, "output": "8\n0\n350\n", "error": None}]
        }
    }
