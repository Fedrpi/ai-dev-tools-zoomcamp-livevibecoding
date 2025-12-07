"""
Evaluation schemas
"""

from pydantic import BaseModel, Field


class ProblemEvaluation(BaseModel):
    """Evaluation for a single problem"""

    problemId: int = Field(..., example=1)
    rating: int = Field(..., ge=1, le=5, example=4, description="Star rating (1-5)")
    comment: str | None = Field(None, example="Good solution, but could be optimized")
    candidateCode: str | None = Field(
        None,
        example="def sum_two_numbers(a, b):\n    return a + b",
        description="The code written by candidate for this problem",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "problemId": 1,
                    "rating": 4,
                    "comment": "Good solution, but could be optimized",
                    "candidateCode": "def sum_two_numbers(a, b):\n    return a + b",
                }
            ]
        }
    }
