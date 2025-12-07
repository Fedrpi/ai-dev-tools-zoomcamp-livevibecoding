"""
WebSocket endpoints for real-time synchronization
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import json

from app.websocket import manager
from app.database import get_db
from app.services import sessions as sessions_service
from app.schemas.websocket import (
    CodeUpdateMessage,
    ProblemChangeMessage,
    UserJoinedMessage,
    UserLeftMessage,
    ConnectionStatusMessage,
    ErrorMessage,
    RunCodeMessage,
)

router = APIRouter()


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str,
    user_name: Optional[str] = Query(None),
    user_role: Optional[str] = Query(None)
):
    """
    WebSocket endpoint for real-time session synchronization

    Query params:
    - user_name: Name of the user connecting
    - user_role: Role of the user (interviewer or candidate)
    """
    await manager.connect(websocket, session_id)

    try:
        # Send connection confirmation
        connection_count = manager.get_session_connection_count(session_id)
        await manager.send_personal_message(
            ConnectionStatusMessage(
                status="connected",
                sessionId=session_id,
                activeUsers=connection_count
            ).model_dump(),
            websocket
        )

        # Notify others that user joined
        if user_name and user_role:
            await manager.broadcast_to_session(
                UserJoinedMessage(
                    userName=user_name,
                    role=user_role
                ).model_dump(),
                session_id,
                exclude=websocket
            )

        # Listen for messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            message_type = message.get("type")

            # Handle different message types
            if message_type == "code_update":
                # Broadcast code update to others in session
                await manager.broadcast_to_session(
                    message,
                    session_id,
                    exclude=websocket  # Don't send back to sender
                )

            elif message_type == "problem_change":
                # Broadcast problem change to all in session
                await manager.broadcast_to_session(
                    message,
                    session_id,
                    exclude=websocket
                )

            elif message_type == "run_code":
                # For now, just echo back (execution will be implemented in Stage 12)
                # In production, this would trigger code execution
                await manager.send_personal_message(
                    {
                        "type": "code_result",
                        "problemId": message.get("problemId"),
                        "success": False,
                        "error": "Code execution not yet implemented"
                    },
                    websocket
                )

            else:
                # Unknown message type
                await manager.send_personal_message(
                    ErrorMessage(
                        message=f"Unknown message type: {message_type}",
                        code="UNKNOWN_MESSAGE_TYPE"
                    ).model_dump(),
                    websocket
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)

        # Notify others that user left
        if user_name and user_role:
            await manager.broadcast_to_session(
                UserLeftMessage(
                    userName=user_name,
                    role=user_role
                ).model_dump(),
                session_id
            )

    except Exception as e:
        # Handle other errors
        try:
            await manager.send_personal_message(
                ErrorMessage(
                    message=str(e),
                    code="INTERNAL_ERROR"
                ).model_dump(),
                websocket
            )
        except:
            pass

        manager.disconnect(websocket, session_id)
