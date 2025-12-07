"""
WebSocket connection manager for real-time synchronization
"""
from typing import Dict, Set
from fastapi import WebSocket
import json


class ConnectionManager:
    """Manages WebSocket connections for sessions"""

    def __init__(self):
        # session_id -> set of websockets
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept WebSocket connection and add to session room"""
        await websocket.accept()

        if session_id not in self.active_connections:
            self.active_connections[session_id] = set()

        self.active_connections[session_id].add(websocket)

    def disconnect(self, websocket: WebSocket, session_id: str):
        """Remove WebSocket connection from session room"""
        if session_id in self.active_connections:
            self.active_connections[session_id].discard(websocket)

            # Clean up empty session rooms
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific WebSocket connection"""
        await websocket.send_json(message)

    async def broadcast_to_session(self, message: dict, session_id: str, exclude: WebSocket = None):
        """Broadcast message to all connections in a session, optionally excluding sender"""
        if session_id not in self.active_connections:
            return

        disconnected = set()

        for connection in self.active_connections[session_id]:
            if exclude and connection == exclude:
                continue

            try:
                await connection.send_json(message)
            except Exception:
                # Connection is broken, mark for removal
                disconnected.add(connection)

        # Clean up disconnected connections
        for connection in disconnected:
            self.disconnect(connection, session_id)

    def get_session_connection_count(self, session_id: str) -> int:
        """Get number of active connections in a session"""
        if session_id not in self.active_connections:
            return 0
        return len(self.active_connections[session_id])


# Global connection manager instance
manager = ConnectionManager()
