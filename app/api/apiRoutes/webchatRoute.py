
from typing import List
from fastapi import APIRouter, Depends, HTTPException ,WebSocket, WebSocketDisconnect, Depends, Query
from app.core.socketiochat import client_endpoint_si,agent_endpoint_si
import json
from datetime import datetime, timezone
from uuid import uuid4

webchatController = APIRouter()


@webchatController.websocket("/client/{client_id}")
async def client_endpoint(websocket: WebSocket, client_id: str):
    return await client_endpoint_si(websocket, client_id)




@webchatController.websocket("/agent")
async def agent_endpoint(websocket: WebSocket):
    return await agent_endpoint_si(websocket)