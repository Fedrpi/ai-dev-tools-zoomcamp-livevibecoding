"""
WebSocket message schemas
"""

from typing import Literal

from pydantic import BaseModel, Field


class WebSocketMessage(BaseModel):
    """Base WebSocket message"""

    type: str = Field(..., description="Message type")


class CodeUpdateMessage(WebSocketMessage):
    """Code update message from candidate"""

    type: Literal["code_update"] = "code_update"
    problemId: int = Field(..., description="Problem being edited")
    code: str = Field(..., description="Current code content")
    cursorPosition: dict | None = Field(None, description="Cursor position (line, column)")


class ProblemChangeMessage(WebSocketMessage):
    """Problem change message from interviewer"""

    type: Literal["problem_change"] = "problem_change"
    problemId: int = Field(..., description="New active problem ID")


class UserJoinedMessage(WebSocketMessage):
    """User joined session message"""

    type: Literal["user_joined"] = "user_joined"
    userName: str = Field(..., description="Name of user who joined")
    role: Literal["interviewer", "candidate"] = Field(..., description="User role")


class UserLeftMessage(WebSocketMessage):
    """User left session message"""

    type: Literal["user_left"] = "user_left"
    userName: str = Field(..., description="Name of user who left")
    role: Literal["interviewer", "candidate"] = Field(..., description="User role")


class ConnectionStatusMessage(WebSocketMessage):
    """Connection status message"""

    type: Literal["connection_status"] = "connection_status"
    status: Literal["connected", "disconnected"] = Field(..., description="Connection status")
    sessionId: str = Field(..., description="Session ID")
    activeUsers: int = Field(..., description="Number of active users in session")


class ErrorMessage(WebSocketMessage):
    """Error message"""

    type: Literal["error"] = "error"
    message: str = Field(..., description="Error message")
    code: str | None = Field(None, description="Error code")


class RunCodeMessage(WebSocketMessage):
    """Run code message"""

    type: Literal["run_code"] = "run_code"
    problemId: int = Field(..., description="Problem to run")
    code: str = Field(..., description="Code to execute")


class CodeResultMessage(WebSocketMessage):
    """Code execution result message"""

    type: Literal["code_result"] = "code_result"
    problemId: int = Field(..., description="Problem that was run")
    success: bool = Field(..., description="Whether execution succeeded")
    output: str | None = Field(None, description="Execution output")
    error: str | None = Field(None, description="Error message if failed")
    testResults: list | None = Field(None, description="Test case results")
