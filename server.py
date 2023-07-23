#!/usr/bin/env python

import asyncio
from websockets.server import serve

async def echo(websocket):
    async for message in websocket:
        await websocket.send(f"Received msg: {message}")

async def main():
    async with serve(echo, "localhost", 5000):
        await asyncio.Future()  # run forever

asyncio.run(main())
