"""
Problems service - business logic for coding problems
"""

import random

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Problem


async def get_problems(
    db: AsyncSession, difficulty: str | None = None, language: str | None = None, count: int = 3
) -> list[Problem]:
    """
    Get coding problems with optional filters
    """
    query = select(Problem)

    # Apply filters
    if difficulty:
        query = query.where(Problem.difficulty == difficulty.upper())

    if language:
        query = query.where(Problem.language == language.upper())

    result = await db.execute(query)
    all_problems = result.scalars().all()

    # Random selection
    if len(all_problems) > count:
        selected = random.sample(list(all_problems), count)
    else:
        selected = list(all_problems)

    return selected


async def get_problem_by_id(db: AsyncSession, problem_id: int) -> Problem | None:
    """
    Get a single problem by ID
    """
    query = select(Problem).where(Problem.id == problem_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()
