"""
Evaluations endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import List
from app.schemas import ProblemEvaluation
from app.database import get_db
from app.services import evaluations as evaluations_service

router = APIRouter()


class SubmitEvaluationRequest(BaseModel):
    """Request to submit evaluation"""

    evaluations: List[ProblemEvaluation] = Field(
        ...,
        description="List of evaluations for each problem"
    )


class SubmitEvaluationResponse(BaseModel):
    """Response after submitting evaluation"""

    success: bool = True
    evaluationId: str = Field(..., example="eval_123")


@router.post("/{sessionId}/evaluate", response_model=SubmitEvaluationResponse, status_code=201)
async def submit_evaluation(
    sessionId: str,
    request: SubmitEvaluationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit session evaluation

    Submit interviewer's evaluation and ratings for all problems
    """
    try:
        # Convert Pydantic models to dicts
        evaluations_data = [
            {
                "problemId": e.problemId,
                "rating": e.rating,
                "comment": e.comment,
                "candidateCode": e.candidateCode
            }
            for e in request.evaluations
        ]

        # Create evaluations in database
        evaluations = await evaluations_service.create_evaluations(
            db,
            sessionId,
            evaluations_data
        )

        # Use first evaluation ID as response ID (or could be session-based)
        evaluation_id = f"eval_{evaluations[0].id}" if evaluations else "eval_0"

        return SubmitEvaluationResponse(
            success=True,
            evaluationId=evaluation_id
        )

    except ValueError as e:
        status_code = 404 if "not found" in str(e).lower() else 400
        raise HTTPException(
            status_code=status_code,
            detail={
                "error": "NotFound" if status_code == 404 else "ValidationError",
                "message": str(e)
            }
        )
