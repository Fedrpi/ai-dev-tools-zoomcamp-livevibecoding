"""
Sessions service - business logic for interview sessions
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from datetime import datetime
import random
import string

from app.models import Session, SessionProblem, User, Problem
from app.services import users, problems as problems_service


def generate_session_id() -> str:
    """Generate unique session ID"""
    return f"sess_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}"


def generate_link_code() -> str:
    """Generate unique link code for candidate"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


async def create_session(
    db: AsyncSession,
    interviewer_name: str,
    difficulty: str,
    language: str,
    number_of_problems: int
) -> tuple[Session, str]:
    """
    Create a new interview session
    Returns: (session, link_code)
    """
    # Create interviewer user
    interviewer = await users.create_user(db, interviewer_name, "interviewer")

    # Get random problems
    problem_list = await problems_service.get_problems(
        db, difficulty=difficulty, language=language, count=number_of_problems
    )

    if len(problem_list) < number_of_problems:
        raise ValueError(f"Not enough problems available for {difficulty} difficulty")

    # Generate IDs
    session_id = generate_session_id()
    link_code = generate_link_code()

    # Create session
    session = Session(
        id=session_id,
        link_code=link_code,
        difficulty=difficulty,
        language=language,
        number_of_problems=number_of_problems,
        interviewer_id=interviewer.id,
        status="waiting",
        created_at=datetime.now()
    )
    db.add(session)
    await db.flush()

    # Add session problems
    for idx, problem in enumerate(problem_list):
        session_problem = SessionProblem(
            session_id=session_id,
            problem_id=problem.id,
            order_index=idx
        )
        db.add(session_problem)

    await db.flush()

    # Re-query session with relationships loaded
    query = (
        select(Session)
        .options(
            selectinload(Session.interviewer),
            selectinload(Session.candidate),
            selectinload(Session.session_problems).selectinload(SessionProblem.problem)
        )
        .where(Session.id == session_id)
    )
    result = await db.execute(query)
    session = result.scalar_one()

    return session, link_code


async def get_session_by_id(db: AsyncSession, session_id: str) -> Optional[Session]:
    """
    Get session by ID with all relationships loaded
    """
    query = (
        select(Session)
        .options(
            selectinload(Session.interviewer),
            selectinload(Session.candidate),
            selectinload(Session.session_problems).selectinload(SessionProblem.problem)
        )
        .where(Session.id == session_id)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_session_by_link_code(db: AsyncSession, link_code: str) -> Optional[Session]:
    """
    Get session by link code
    """
    query = (
        select(Session)
        .options(selectinload(Session.interviewer))
        .where(Session.link_code == link_code)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def join_session(
    db: AsyncSession,
    session_id: str,
    candidate_name: str
) -> Session:
    """
    Candidate joins a session
    """
    session = await get_session_by_id(db, session_id)
    if not session:
        raise ValueError("Session not found")

    if session.status != "waiting":
        raise ValueError("Session is not available for joining")

    # Create candidate user
    candidate = await users.create_user(db, candidate_name, "candidate")

    # Update session
    session.candidate_id = candidate.id
    session.status = "active"

    await db.flush()

    # Expire the session to force a fresh query
    db.expire(session)

    # Re-query session with relationships loaded
    session = await get_session_by_id(db, session_id)

    return session


async def end_session(db: AsyncSession, session_id: str) -> Session:
    """
    End an interview session
    """
    session = await get_session_by_id(db, session_id)
    if not session:
        raise ValueError("Session not found")

    session.status = "ended"
    session.ended_at = datetime.now()

    await db.flush()

    # Re-query session with relationships loaded
    session = await get_session_by_id(db, session_id)

    return session


def get_session_problems(session: Session) -> List[Problem]:
    """
    Get ordered list of problems for a session
    """
    session_problems = sorted(session.session_problems, key=lambda sp: sp.order_index)
    return [sp.problem for sp in session_problems]
