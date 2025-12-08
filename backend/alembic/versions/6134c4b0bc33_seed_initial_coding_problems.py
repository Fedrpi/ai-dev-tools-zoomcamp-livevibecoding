"""seed_initial_coding_problems

Revision ID: 6134c4b0bc33
Revises: eae51518031b
Create Date: 2025-12-07 14:13:46.964831

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6134c4b0bc33"
down_revision: str | Sequence[str] | None = "eae51518031b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Seed initial coding problems."""

    # Use raw SQL with explicit ENUM casting for PostgreSQL
    op.execute("""
        INSERT INTO problems (id, title, difficulty, language, description, starter_code, test_cases)
        VALUES
            -- Junior problems
            (1, 'Sum Two Numbers', 'JUNIOR'::difficulty, 'PYTHON'::language,
             'Write a function that takes two numbers as parameters and returns their sum.',
             'def sum_two_numbers(a, b):
    # Write your code here
    pass',
             '[{"input": [5, 3], "expected": 8}, {"input": [0, 0], "expected": 0}, {"input": [100, 250], "expected": 350}]'::json),

            (2, 'Find Maximum', 'JUNIOR'::difficulty, 'PYTHON'::language,
             'Write a function that takes a list of numbers and returns the maximum value.',
             'def find_max(numbers):
    # Write your code here
    pass',
             '[{"input": [[1, 5, 3, 9, 2]], "expected": 9}, {"input": [[10]], "expected": 10}, {"input": [[-5, -2, -10]], "expected": -2}]'::json),

            (3, 'Reverse String', 'JUNIOR'::difficulty, 'PYTHON'::language,
             'Write a function that takes a string and returns it reversed.',
             'def reverse_string(s):
    # Write your code here
    pass',
             '[{"input": ["hello"], "expected": "olleh"}, {"input": ["Python"], "expected": "nohtyP"}, {"input": [""], "expected": ""}]'::json),

            -- Middle problems
            (4, 'Find Duplicates', 'MIDDLE'::difficulty, 'PYTHON'::language,
             'Write a function that takes a list and returns all duplicate elements.',
             'def find_duplicates(arr):
    # Write your code here
    pass',
             '[{"input": [[1, 2, 3, 2, 4, 5, 1]], "expected": [1, 2]}, {"input": [[1, 1, 1, 1]], "expected": [1]}, {"input": [[1, 2, 3]], "expected": []}]'::json),

            (5, 'Fibonacci Sequence', 'MIDDLE'::difficulty, 'PYTHON'::language,
             'Write a function that returns the nth number in the Fibonacci sequence.',
             'def fibonacci(n):
    # Write your code here
    pass',
             '[{"input": [0], "expected": 0}, {"input": [1], "expected": 1}, {"input": [6], "expected": 8}]'::json),

            (6, 'Valid Parentheses', 'MIDDLE'::difficulty, 'PYTHON'::language,
             'Write a function that checks if a string of parentheses is valid.',
             'def is_valid_parentheses(s):
    # Write your code here
    pass',
             '[{"input": ["()"], "expected": true}, {"input": ["()[]{}"], "expected": true}, {"input": ["(]"], "expected": false}]'::json),

            -- Senior problems
            (7, 'Binary Tree Traversal', 'SENIOR'::difficulty, 'PYTHON'::language,
             'Implement in-order traversal of a binary tree.',
             'def inorder_traversal(root):
    # Write your code here
    pass',
             '[{"input": [{"val": 1, "left": null, "right": {"val": 2, "left": {"val": 3, "left": null, "right": null}, "right": null}}], "expected": [1, 3, 2]}]'::json),

            (8, 'LRU Cache', 'SENIOR'::difficulty, 'PYTHON'::language,
             'Design and implement a Least Recently Used (LRU) cache.',
             'class LRUCache:
    def __init__(self, capacity):
        pass

    def get(self, key):
        pass

    def put(self, key, value):
        pass',
             '[{"input": [2, ["put", 1, 1], ["put", 2, 2], ["get", 1], ["put", 3, 3], ["get", 2]], "expected": [null, null, 1, null, -1]}]'::json),

            (9, 'Word Ladder', 'SENIOR'::difficulty, 'PYTHON'::language,
             'Find the shortest transformation sequence from beginWord to endWord.',
             'def ladder_length(beginWord, endWord, wordList):
    # Write your code here
    pass',
             '[{"input": ["hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]], "expected": 5}, {"input": ["hit", "cog", ["hot", "dot", "dog", "lot", "log"]], "expected": 0}]'::json)
    """)


def downgrade() -> None:
    """Remove seeded problems."""
    op.execute("DELETE FROM problems WHERE id BETWEEN 1 AND 9")
