from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()
connected_clients: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    print("New client connected.")  # Debugging line

    try:
        while True:
            message = await websocket.receive_text()
            print(f"Received: {message}")

            # Broadcast to all connected clients (e.g., the bot)
            for client in connected_clients:
                if client != websocket:
                    await client.send_text(message)

    except Exception as e:
        print(f"Client disconnected: {e}")

    finally:
        connected_clients.remove(websocket)
