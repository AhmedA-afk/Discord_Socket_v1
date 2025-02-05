import os
import discord
import asyncio
import websockets
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

if not TOKEN:
    raise ValueError("Missing DISCORD_BOT_TOKEN in environment variables.")

if not CHANNEL_ID:
    raise ValueError("Missing DISCORD_CHANNEL_ID in environment variables.")

CHANNEL_ID = int(CHANNEL_ID)

# Initialize Discord client
intents = discord.Intents.default()
intents.messages = True  # Enable message events
client = discord.Client(intents=intents)

async def listen_to_websocket():
    await client.wait_until_ready()
    uri = "ws://127.0.0.1:8000/ws"
    
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to WebSocket")
                while True:
                    message = await websocket.recv()
                    print(f"Received from WebSocket: {message}")

                    channel = client.get_channel(CHANNEL_ID)
                    if channel:
                        await channel.send(message)
                        print(f"Sent message to Discord: {message}")
                    else:
                        print("Failed to get channel")
        except Exception as e:
            print(f"WebSocket connection error: {e}, retrying in 5 seconds...")
            await asyncio.sleep(5)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    client.loop.create_task(listen_to_websocket())

@client.event
async def on_message(message):
    # Prevent the bot from responding to its own messages
    if message.author == client.user:
        return
    
    # Debugging log
    print(f"Message from Discord: {message.content}")

    # Send the message to the WebSocket server
    uri = "ws://127.0.0.1:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send(message.content)
        print(f"Sent message to WebSocket: {message.content}")

# Run the bot (must be at the end)
client.run(TOKEN)
