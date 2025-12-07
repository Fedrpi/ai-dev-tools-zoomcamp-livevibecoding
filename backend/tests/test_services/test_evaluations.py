"""
Tests for evaluations service
"""
import pytest
from app.services import evaluations as evaluations_service
from app.services import sessions as sessions_service


@pytest.mark.asyncio
async def test_create_evaluations(db_session, sample_problems):
    """Test creating evaluations"""
    # Create and end a session
    session, _ = await sessions_service.create_session(
        db_session, "John Doe", "junior", "python", 1
    )
    await sessions_service.end_session(db_session, session.id)

    # Reload to get problems
    session = await sessions_service.get_session_by_id(db_session, session.id)
    problems = sessions_service.get_session_problems(session)
    problem_id = problems[0].id

    # Create evaluations
    evaluations_data = [
        {
            "problemId": problem_id,
            "rating": 4,
            "comment": "Good solution",
            "candidateCode": "def solution(): pass"
        }
    ]

    result = await evaluations_service.create_evaluations(
        db_session,
        session.id,
        evaluations_data
    )

    assert len(result) == 1
    assert result[0].rating == 4
    assert result[0].comment == "Good solution"


@pytest.mark.asyncio
async def test_create_evaluations_session_not_found(db_session):
    """Test creating evaluations for non-existent session"""
    with pytest.raises(ValueError, match="Session not found"):
        await evaluations_service.create_evaluations(
            db_session,
            "nonexistent",
            []
        )


@pytest.mark.asyncio
async def test_create_evaluations_session_not_ended(db_session, sample_problems):
    """Test that evaluations fail if session not ended"""
    session, _ = await sessions_service.create_session(
        db_session, "John Doe", "junior", "python", 1
    )

    with pytest.raises(ValueError, match="must be ended"):
        await evaluations_service.create_evaluations(
            db_session,
            session.id,
            []
        )


@pytest.mark.asyncio
async def test_create_evaluations_invalid_problem_id(db_session, sample_problems):
    """Test that evaluations fail with invalid problem ID"""
    # Create and end a session
    session, _ = await sessions_service.create_session(
        db_session, "John Doe", "junior", "python", 1
    )
    await sessions_service.end_session(db_session, session.id)

    # Try to create evaluation with invalid problem ID
    evaluations_data = [
        {
            "problemId": 99999,  # Invalid ID
            "rating": 4,
            "comment": "Test",
            "candidateCode": "# code"
        }
    ]

    with pytest.raises(ValueError, match="Invalid problem IDs"):
        await evaluations_service.create_evaluations(
            db_session,
            session.id,
            evaluations_data
        )


@pytest.mark.asyncio
async def test_create_multiple_evaluations(db_session, sample_problems):
    """Test creating evaluations for multiple problems"""
    # Create session with 2 problems
    session, _ = await sessions_service.create_session(
        db_session, "John Doe", "junior", "python", 1
    )
    await sessions_service.end_session(db_session, session.id)

    # Reload to get problems
    session = await sessions_service.get_session_by_id(db_session, session.id)
    problems = sessions_service.get_session_problems(session)

    # Create evaluations for all problems
    evaluations_data = [
        {
            "problemId": p.id,
            "rating": i + 1,
            "comment": f"Comment {i}",
            "candidateCode": f"# code {i}"
        }
        for i, p in enumerate(problems)
    ]

    result = await evaluations_service.create_evaluations(
        db_session,
        session.id,
        evaluations_data
    )

    assert len(result) == len(problems)
