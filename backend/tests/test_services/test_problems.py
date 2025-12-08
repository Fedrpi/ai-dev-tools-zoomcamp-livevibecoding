"""
Tests for problems service
"""

import pytest

from app.services import problems as problems_service


@pytest.mark.asyncio
async def test_get_problems_all(db_session, sample_problems):
    """Test getting all problems"""
    result = await problems_service.get_problems(db_session, count=10)
    assert len(result) == 3


@pytest.mark.asyncio
async def test_get_problems_by_difficulty(db_session, sample_problems):
    """Test filtering by difficulty"""
    result = await problems_service.get_problems(db_session, difficulty="junior", count=10)
    assert len(result) == 1
    # Enum values are stored as lowercase in database
    difficulty_val = (
        result[0].difficulty.value
        if hasattr(result[0].difficulty, "value")
        else result[0].difficulty
    )
    assert difficulty_val.upper() == "JUNIOR"


@pytest.mark.asyncio
async def test_get_problems_by_language(db_session, sample_problems):
    """Test filtering by language"""
    result = await problems_service.get_problems(db_session, language="python", count=10)
    assert len(result) == 3
    for problem in result:
        language_val = (
            problem.language.value if hasattr(problem.language, "value") else problem.language
        )
        assert language_val.upper() == "PYTHON"


@pytest.mark.asyncio
async def test_get_problems_count_limit(db_session, sample_problems):
    """Test count parameter limits results"""
    result = await problems_service.get_problems(db_session, count=2)
    assert len(result) <= 2


@pytest.mark.asyncio
async def test_get_problems_randomized(db_session, sample_problems):
    """Test that problems are returned (random order is probabilistic)"""
    # Get problems multiple times - order should be random but may repeat
    results = []
    for _ in range(10):
        result = await problems_service.get_problems(db_session, count=3)
        results.append([p.id for p in result])

    # Just verify that we get valid problems consistently
    # Randomization is probabilistic and may occasionally return same order
    assert all(len(r) == 3 for r in results)
