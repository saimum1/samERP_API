
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json



clients = {} 
agent = None  
message_history = []  

async def client_endpoint_si(websocket: WebSocket, client_id: str):
    """Client connects here"""
    await websocket.accept()
    clients[client_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            dataready={
                        "type": "message",
                        "client_id": client_id,
                        "message": msg.get("message"),
                        "username": msg.get("username"),
                        "gmail": msg.get("gmail"),
                        "image": msg.get("image"),
                        "messageid": msg.get("messageid"),
                        "from_type": msg.get("fromType")
                    }
            if agent:
                try:
                    await agent.send_json(dataready)
                except:
                    print("agent is not active, pushong to history")
                    message_history.append(dataready)
            else:    
                print("agent is not active, pushong to history")
                message_history.append(dataready)
                
    except WebSocketDisconnect:
        del clients[client_id]
        
        if agent:
            await agent.send_json({"type": "disconnected", "client_id": client_id})


async def agent_endpoint_si(websocket: WebSocket):
    """Agent connects here"""
    global agent
    await websocket.accept()
    agent = websocket

    try:
        await agent.send_json({"type": "history", "messages": message_history})
    except Exception as e:
        print(f"Failed to send history: {e}")
        return

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            print("data from agent--->>>",msg)
            if msg.get("type") == "reply":
                client_id = msg.get("client_id")
                reply_text = msg.get("message")
                alldata=msg
                new_message = msg.get("newMessage", {})
                message_history.append({"client_id": client_id, "from_agent": True, "message": reply_text, "username": alldata.get("username"), "gmail": alldata.get("gmail"), "image": alldata.get("image"), "messageid": alldata.get("messageid"), "from_type": alldata.get("fromType")})

                if client_id in clients:
                    await clients[client_id].send_json({
                        "type": "message",
                        "message": reply_text,
                        **new_message

                    })

    except WebSocketDisconnect:
        agent = None

