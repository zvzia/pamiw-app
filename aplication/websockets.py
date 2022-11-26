import asyncio
import datetime
import random
import websockets

async def send_message(websocket, user_id):
    while True:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(message)
        await asyncio.sleep(random.random() * 2 + 1)
        

async def websocket_main():
    async with websockets.serve(send_message, "localhost", 5678):
        await asyncio.Future()  # run forever