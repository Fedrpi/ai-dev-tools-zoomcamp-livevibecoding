"""
Evaluations service - business logic for session evaluations
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.models import Evaluation
from app.services import sessions as sessions_service


async def create_evaluations(
    db: AsyncSession,
    session_id: str,
    evaluations_data: List[dict]
) -> List[Evaluation]:
    """
    Create evaluations for a session
    """
    # Validate session exists and is ended
    session = await sessions_service.get_session_by_id(db, session_id)
    if not session:
        raise ValueError("Session not found")

    if session.status != "ended":
        raise ValueError("Session must be ended before evaluation")

    # Get session problem IDs
    session_problem_ids = {sp.problem_id for sp in session.session_problems}

    # Validate all problem IDs
    evaluation_problem_ids = {e["problemId"] for e in evaluations_data}
    invalid_ids = evaluation_problem_ids - session_problem_ids
    if invalid_ids:
        raise ValueError(f"Invalid problem IDs: {invalid_ids}")

    # Create evaluations
    evaluations = []
    for eval_data in evaluations_data:
        evaluation = Evaluation(
            session_id=session_id,
            problem_id=eval_data["problemId"],
            rating=eval_data["rating"],
            comment=eval_data.get("comment"),
            candidate_code=eval_data.get("candidateCode")
        )
        db.add(evaluation)
        evaluations.append(evaluation)

    await db.flush()

    return evaluations
