from fastapi import WebSocket
from typing import List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    # ─── CONNECT ─────────────────────────────────
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Client connected. Total: {len(self.active_connections)}")

    # ─── DISCONNECT ──────────────────────────────
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client disconnected. Total: {len(self.active_connections)}")

    # ─── BROADCAST TO ALL ────────────────────────
    async def broadcast(self, data: dict):
        message = json.dumps(data)
        dead = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                dead.append(connection)
        # remove dead connections
        for conn in dead:
            self.active_connections.remove(conn)

# ─── SINGLE INSTANCE ─────────────────────────────
manager = ConnectionManager()