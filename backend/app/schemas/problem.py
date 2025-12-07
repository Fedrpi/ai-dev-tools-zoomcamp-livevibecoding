"""
Problem schemas
"""

from pydantic import BaseModel, Field
from typing import List, Any, Literal


class TestCase(BaseModel):
    """Test case for a problem"""

    input: List[Any] = Field(..., description="Input parameters for the test")
    expected: Any = Field(..., description="Expected output")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "input": [5, 3],
                    "expected": 8
                }
            ]
        }
    }


class Problem(BaseModel):
    """Coding problem/task"""

    id: int = Field(..., example=1)
    title: str = Field(..., example="Sum Two Numbers")
    difficulty: Literal["junior", "middle", "senior"] = Field(..., example="junior")
    language: Literal["python"] = Field(..., example="python")
    description: str = Field(
        ...,
        example="Write a function that takes two numbers as parameters and returns their sum."
    )
    starterCode: str = Field(
        ...,
        alias="starterCode",
        example="def sum_two_numbers(a, b):\n    # Write your code here\n    pass"
    )
    testCases: List[TestCase] = Field(default_factory=list, alias="testCases")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Sum Two Numbers",
                    "difficulty": "junior",
                    "language": "python",
                    "description": "Write a function that takes two numbers as parameters and returns their sum.",
                    "starterCode": "def sum_two_numbers(a, b):\n    # Write your code here\n    pass",
                    "testCases": [
                        {"input": [5, 3], "expected": 8}
                    ]
                }
            ]
        }
    }
