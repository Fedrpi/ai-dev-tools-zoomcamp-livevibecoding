"""
Sessions endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import List
from app.schemas import (
    Session as SessionSchema,
    SessionCreate,
    SessionInfo,
    User as UserSchema,
    Problem as ProblemSchema,
    TestCase
)
from app.database import get_db
from app.services import sessions as sessions_service

router = APIRouter()


class CreateSessionResponse(BaseModel):
    """Response after creating session"""

    session: SessionSchema
    linkCode: str = Field(..., description="Unique link code for candidate to join")


class SessionResponse(BaseModel):
    """Response with session"""

    session: SessionSchema


class SessionInfoResponse(BaseModel):
    """Response with limited session info"""

    session: SessionInfo


class JoinSessionRequest(BaseModel):
    """Request to join session"""

    candidateName: str = Field(..., min_length=3, example="Jane Smith")


class EndSessionResponse(BaseModel):
    """Response after ending session"""

    success: bool = True


def db_session_to_schema(session, problems_list, interviewer_data, candidate_data=None) -> SessionSchema:
    """Convert database Session to schema"""
    # Convert problems to schema
    problem_schemas = []
    for p in problems_list:
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

    # Interviewer
    interviewer_schema = UserSchema(
        name=interviewer_data["name"],
        role=interviewer_data["role"]
    )

    # Candidate (optional)
    candidate_schema = None
    if candidate_data:
        candidate_schema = UserSchema(
            name=candidate_data["name"],
            role=candidate_data["role"]
        )

    return SessionSchema(
        id=session.id,
        difficulty=session.difficulty,
        language=session.language,
        numberOfProblems=session.number_of_problems,
        problems=problem_schemas,
        interviewer=interviewer_schema,
        candidate=candidate_schema,
        status=session.status.value if hasattr(session.status, 'value') else session.status,
        createdAt=session.created_at,
        endedAt=session.ended_at
    )


@router.post("", response_model=CreateSessionResponse, status_code=201)
async def create_session(
    request: SessionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create new interview session

    Create a new coding interview session with selected problems
    """
    try:
        session, link_code = await sessions_service.create_session(
            db,
            request.interviewerName,
            request.difficulty,
            request.language,
            request.numberOfProblems
        )

        # Access relationships in async context
        problems = sessions_service.get_session_problems(session)
        interviewer_data = {
            "name": session.interviewer.name,
            "role": session.interviewer.role.value if hasattr(session.interviewer.role, 'value') else session.interviewer.role
        }

        session_schema = db_session_to_schema(session, problems, interviewer_data)

        return CreateSessionResponse(session=session_schema, linkCode=link_code)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "ValidationError",
                "message": str(e)
            }
        )


@router.get("/by-link/{linkCode}", response_model=SessionInfoResponse)
async def get_session_by_link(
    linkCode: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get session by link code

    Retrieve session information using the candidate join link code
    """
    session = await sessions_service.get_session_by_link_code(db, linkCode)

    if not session:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "NotFound",
                "message": "Session not found"
            }
        )

    # Return limited info
    session_info = SessionInfo(
        id=session.id,
        difficulty=session.difficulty,
        language=session.language,
        numberOfProblems=session.number_of_problems,
        interviewer={"name": session.interviewer.name}
    )

    return SessionInfoResponse(session=session_info)


@router.get("/{sessionId}", response_model=SessionResponse)
async def get_session(
    sessionId: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get session details

    Get full session details including problems and participants
    """
    session = await sessions_service.get_session_by_id(db, sessionId)

    if not session:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "NotFound",
                "message": "Session not found"
            }
        )

    # Access relationships in async context
    problems = sessions_service.get_session_problems(session)
    interviewer_data = {
        "name": session.interviewer.name,
        "role": session.interviewer.role.value if hasattr(session.interviewer.role, 'value') else session.interviewer.role
    }
    candidate_data = None
    if session.candidate:
        candidate_data = {
            "name": session.candidate.name,
            "role": session.candidate.role.value if hasattr(session.candidate.role, 'value') else session.candidate.role
        }

    session_schema = db_session_to_schema(session, problems, interviewer_data, candidate_data)
    return SessionResponse(session=session_schema)


@router.post("/{sessionId}/join", response_model=SessionResponse)
async def join_session(
    sessionId: str,
    request: JoinSessionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Candidate joins session

    Candidate joins the interview session with their name
    """
    try:
        session = await sessions_service.join_session(db, sessionId, request.candidateName)

        # Access relationships in async context
        problems = sessions_service.get_session_problems(session)
        interviewer_data = {
            "name": session.interviewer.name,
            "role": session.interviewer.role.value if hasattr(session.interviewer.role, 'value') else session.interviewer.role
        }
        candidate_data = None
        if session.candidate:
            candidate_data = {
                "name": session.candidate.name,
                "role": session.candidate.role.value if hasattr(session.candidate.role, 'value') else session.candidate.role
            }

        session_schema = db_session_to_schema(session, problems, interviewer_data, candidate_data)
        return SessionResponse(session=session_schema)

    except ValueError as e:
        status_code = 404 if "not found" in str(e).lower() else 400
        raise HTTPException(
            status_code=status_code,
            detail={
                "error": "NotFound" if status_code == 404 else "ValidationError",
                "message": str(e)
            }
        )


@router.post("/{sessionId}/end", response_model=EndSessionResponse)
async def end_session(
    sessionId: str,
    db: AsyncSession = Depends(get_db)
):
    """
    End interview session

    Mark the session as ended
    """
    try:
        await sessions_service.end_session(db, sessionId)
        return EndSessionResponse(success=True)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "NotFound",
                "message": str(e)
            }
        )
