"""
Tests for sessions service
"""

import pytest

from app.services import sessions as sessions_service


@pytest.mark.asyncio
async def test_create_session(db_session, sample_problems):
    """Test creating a session"""
    session, link_code = await sessions_service.create_session(
        db_session,
        interviewer_name="John Doe",
        difficulty="junior",
        language="python",
        number_of_problems=1,
    )

    assert session.id is not None
    assert session.link_code == link_code
    assert session.difficulty == "junior"
    assert session.language == "python"
    assert session.number_of_problems == 1
    # Status may be enum or string depending on how it's loaded
    status_val = session.status.value if hasattr(session.status, "value") else session.status
    assert status_val.upper() == "WAITING"
    assert session.interviewer.name == "John Doe"


@pytest.mark.asyncio
async def test_create_session_link_code_unique(db_session, sample_problems):
    """Test that link codes are unique"""
    session1, link_code1 = await sessions_service.create_session(
        db_session, "User1", "junior", "python", 1
    )
    session2, link_code2 = await sessions_service.create_session(
        db_session, "User2", "junior", "python", 1
    )

    assert link_code1 != link_code2


@pytest.mark.asyncio
async def test_create_session_not_enough_problems(db_session, sample_problems):
    """Test error when not enough problems available"""
    with pytest.raises(ValueError, match="Not enough problems"):
        await sessions_service.create_session(
            db_session,
            interviewer_name="John Doe",
            difficulty="senior",
            language="python",
            number_of_problems=10,  # Only 1 senior problem available
        )


@pytest.mark.asyncio
async def test_get_session_by_id(db_session, sample_problems):
    """Test getting session by ID"""
    session, _ = await sessions_service.create_session(
        db_session, "John Doe", "junior", "python", 1
    )

    retrieved = await sessions_service.get_session_by_id(db_session, session.id)

    assert retrieved is not None
    assert retrieved.id == session.id
    assert retrieved.interviewer.name == "John Doe"


@pytest.mark.asyncio
async def test_get_session_by_id_not_found(db_session):
    """Test getting non-existent session"""
    result = await sessions_service.get_session_by_id(db_session, "nonexistent")
    assert result is None


@pytest.mark.asyncio
async def test_get_session_by_link_code(db_session, sample_problems):
    """Test getting session by link code"""
    session, link_code = await sessions_service.create_session(
        db_session, "John Doe", "junior", "python", 1
    )

    retrieved = await sessions_service.get_session_by_link_code(db_session, link_code)

    assert retrieved is not None
    assert retrieved.id == session.id
    assert retrieved.link_code == link_code


@pytest.mark.asyncio
async def test_join_session(db_session, sample_problems):
    """Test candidate joining session"""
    session, _ = await sessions_service.create_session(
        db_session, "John Doe", "junior", "python", 1
    )

    updated_session = await sessions_service.join_session(db_session, session.id, "Jane Smith")

    # Candidate should be loaded because join_session uses get_session_by_id
    assert updated_session.candidate is not None
    assert updated_session.candidate.name == "Jane Smith"
    status_val = (
        updated_session.status.value
        if hasattr(updated_session.status, "value")
        else updated_session.status
    )
    assert status_val.upper() == "ACTIVE"


@pytest.mark.asyncio
async def test_join_session_not_found(db_session):
    """Test joining non-existent session"""
    with pytest.raises(ValueError, match="Session not found"):
        await sessions_service.join_session(db_session, "nonexistent", "Jane Smith")


@pytest.mark.asyncio
async def test_join_session_not_waiting(db_session, sample_problems):
    """Test that cannot join session that's not waiting"""
    session, _ = await sessions_service.create_session(
        db_session, "John Doe", "junior", "python", 1
    )

    # Join once
    await sessions_service.join_session(db_session, session.id, "Jane Smith")

    # Try to join again - session is now active
    with pytest.raises(ValueError, match="not available for joining"):
        await sessions_service.join_session(db_session, session.id, "Bob Johnson")


@pytest.mark.asyncio
async def test_end_session(db_session, sample_problems):
    """Test ending a session"""
    session, _ = await sessions_service.create_session(
        db_session, "John Doe", "junior", "python", 1
    )

    ended_session = await sessions_service.end_session(db_session, session.id)

    status_val = (
        ended_session.status.value
        if hasattr(ended_session.status, "value")
        else ended_session.status
    )
    assert status_val.upper() == "ENDED"
    assert ended_session.ended_at is not None


@pytest.mark.asyncio
async def test_end_session_not_found(db_session):
    """Test ending non-existent session"""
    with pytest.raises(ValueError, match="Session not found"):
        await sessions_service.end_session(db_session, "nonexistent")


@pytest.mark.asyncio
async def test_get_session_problems(db_session, sample_problems):
    """Test getting ordered problems for session"""
    session, _ = await sessions_service.create_session(
        db_session, "John Doe", "junior", "python", 1
    )

    # Need to reload session with relationships
    session = await sessions_service.get_session_by_id(db_session, session.id)

    problems = sessions_service.get_session_problems(session)

    assert len(problems) == 1
    assert all(hasattr(p, "title") for p in problems)
