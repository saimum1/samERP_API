
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from app.core.socketiochat import ConnectionManager


manager = ConnectionManager()

# @app.websocket("/ws/chat")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.broadcast(data)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
