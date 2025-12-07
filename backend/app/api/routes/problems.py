"""
Problems endpoints
"""

from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Literal
from pydantic import BaseModel
from app.schemas import Problem as ProblemSchema, TestCase
from app.database import get_db
from app.services import problems as problems_service
import json

router = APIRouter()


# Mock problems data removed - now using database

# Kept old mock code commented out for reference
"""
_MOCK_PROBLEMS = [
    # Junior problems
    ProblemSchema(
        id=1,
        title="Sum Two Numbers",
        difficulty="junior",
        language="python",
        description="Write a function that takes two numbers as parameters and returns their sum.",
        starterCode="def sum_two_numbers(a, b):\n    # Write your code here\n    pass",
        testCases=[
            TestCase(input=[5, 3], expected=8),
            TestCase(input=[0, 0], expected=0),
            TestCase(input=[100, 250], expected=350),
        ]
    ),
    Problem(
        id=2,
        title="Find Maximum",
        difficulty="junior",
        language="python",
        description="Write a function that takes a list of numbers and returns the maximum value.",
        starterCode="def find_max(numbers):\n    # Write your code here\n    pass",
        testCases=[
            TestCase(input=[[1, 5, 3, 9, 2]], expected=9),
            TestCase(input=[[10]], expected=10),
            TestCase(input=[[-5, -2, -10]], expected=-2),
        ]
    ),
    Problem(
        id=3,
        title="Reverse String",
        difficulty="junior",
        language="python",
        description="Write a function that takes a string and returns it reversed.",
        starterCode="def reverse_string(s):\n    # Write your code here\n    pass",
        testCases=[
            TestCase(input=["hello"], expected="olleh"),
            TestCase(input=["Python"], expected="nohtyP"),
            TestCase(input=[""], expected=""),
        ]
    ),
    # Middle problems
    Problem(
        id=4,
        title="Find Duplicates",
        difficulty="middle",
        language="python",
        description="Write a function that takes a list and returns all duplicate elements.",
        starterCode="def find_duplicates(arr):\n    # Write your code here\n    pass",
        testCases=[
            TestCase(input=[[1, 2, 3, 2, 4, 5, 1]], expected=[1, 2]),
            TestCase(input=[[1, 1, 1, 1]], expected=[1]),
            TestCase(input=[[1, 2, 3]], expected=[]),
        ]
    ),
    Problem(
        id=5,
        title="Fibonacci Sequence",
        difficulty="middle",
        language="python",
        description="Write a function that returns the nth number in the Fibonacci sequence.",
        starterCode="def fibonacci(n):\n    # Write your code here\n    pass",
        testCases=[
            TestCase(input=[0], expected=0),
            TestCase(input=[1], expected=1),
            TestCase(input=[6], expected=8),
        ]
    ),
    Problem(
        id=6,
        title="Valid Parentheses",
        difficulty="middle",
        language="python",
        description="Write a function that checks if a string of parentheses is valid.",
        starterCode="def is_valid_parentheses(s):\n    # Write your code here\n    pass",
        testCases=[
            TestCase(input=["()"], expected=True),
            TestCase(input=["()[]{}"], expected=True),
            TestCase(input=["(]"], expected=False),
        ]
    ),
    # Senior problems
    Problem(
        id=7,
        title="Binary Tree Traversal",
        difficulty="senior",
        language="python",
        description="Implement in-order traversal of a binary tree.",
        starterCode="def inorder_traversal(root):\n    # Write your code here\n    pass",
        testCases=[
            TestCase(input=[{"val": 1, "left": None, "right": {"val": 2, "left": {"val": 3, "left": None, "right": None}, "right": None}}], expected=[1, 3, 2]),
        ]
    ),
    Problem(
        id=8,
        title="LRU Cache",
        difficulty="senior",
        language="python",
        description="Design and implement a Least Recently Used (LRU) cache.",
        starterCode="class LRUCache:\n    def __init__(self, capacity):\n        pass\n    \n    def get(self, key):\n        pass\n    \n    def put(self, key, value):\n        pass",
        testCases=[
            TestCase(input=[2, ["put", 1, 1], ["put", 2, 2], ["get", 1], ["put", 3, 3], ["get", 2]], expected=[None, None, 1, None, -1]),
        ]
    ),
    Problem(
        id=9,
        title="Word Ladder",
        difficulty="senior",
        language="python",
        description="Find the shortest transformation sequence from beginWord to endWord.",
        starterCode="def ladder_length(beginWord, endWord, wordList):\n    # Write your code here\n    pass",
        testCases=[
            TestCase(input=["hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]], expected=5),
            TestCase(input=["hit", "cog", ["hot", "dot", "dog", "lot", "log"]], expected=0),
        ]
    ),
]
"""


class ProblemsResponse(BaseModel):
    """Response with list of problems"""

    problems: List[ProblemSchema]


@router.get("", response_model=ProblemsResponse)
async def get_problems(
    difficulty: Optional[Literal["junior", "middle", "senior"]] = Query(None, description="Filter by difficulty level"),
    language: Optional[Literal["python"]] = Query(None, description="Filter by programming language"),
    count: int = Query(3, ge=1, le=5, description="Number of random problems to return"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get coding problems

    Get list of coding problems with optional filters
    """
    # Get problems from database
    problems = await problems_service.get_problems(db, difficulty, language, count)

    # Convert to schema
    problem_schemas = []
    for p in problems:
        # Parse test_cases JSON
        test_cases = [TestCase(**tc) for tc in p.test_cases]

        problem_schema = ProblemSchema(
            id=p.id,
            title=p.title,
            difficulty=p.difficulty.value.lower(),
            language=p.language.value.lower(),
            description=p.description,
            starterCode=p.starter_code,
            testCases=test_cases
        )
        problem_schemas.append(problem_schema)

    return ProblemsResponse(problems=problem_schemas)
