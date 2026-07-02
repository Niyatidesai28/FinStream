import json
from typing import List

from fastapi import WebSocket


class WebSocketManager:
    """Tracks connected WebSocket clients and handles broadcasting."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal(self, websocket: WebSocket, message: dict) -> None:
        await websocket.send_text(json.dumps(message, default=str))

    async def broadcast(self, message: dict) -> None:
        payload = json.dumps(message, default=str)
        stale_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_text(payload)
            except Exception:
                stale_connections.append(connection)
        for connection in stale_connections:
            self.disconnect(connection)


# Singleton instance shared across the application.
websocket_manager = WebSocketManager()
