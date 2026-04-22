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

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.socket_manager import manager
from app.utils import verify_token

router = APIRouter(tags=["WebSocket"])

@router.websocket("/ws/{election_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    election_id: int,
    token: str = Query(...)   # client passes ?token=xxx
):
    # ─── AUTH CHECK ──────────────────────────────
    payload = verify_token(token)
    if not payload:
        await websocket.close(code=1008)  # 1008 = policy violation
        return

    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)