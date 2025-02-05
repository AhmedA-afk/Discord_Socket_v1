import websockets
import asyncio

async def send_message():
    uri = "ws://localhost:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            message = "Hello from Application"
            await websocket.send(message)
            print(f"Sent: {message}")
    except Exception as e:
        print(f"Failed to send message: {e}")

asyncio.run(send_message())
