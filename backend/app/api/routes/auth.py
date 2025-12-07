"""
Authentication endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.schemas import User

router = APIRouter()


class LoginRequest(BaseModel):
    """Login request body"""

    name: str = Field(..., min_length=3, example="John Doe")


class LoginResponse(BaseModel):
    """Login response"""

    user: User


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Interviewer login

    Authenticate interviewer by name (simple auth for MVP)
    """
    if len(request.name) < 3:
        raise HTTPException(
            status_code=400,
            detail={"error": "ValidationError", "message": "Name must be at least 3 characters"},
        )

    # Mock response
    user = User(name=request.name, role="interviewer")

    return LoginResponse(user=user)
