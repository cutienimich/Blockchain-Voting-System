from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.socket_manager import manager

router = APIRouter(tags=["WebSocket"])

# ─── ELECTION ROOM ───────────────────────────────
@router.websocket("/ws/{election_id}")
async def websocket_endpoint(websocket: WebSocket, election_id: int):
    await manager.connect(websocket)
    try:
        while True:
            # keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)