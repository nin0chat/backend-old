import asyncio
import json
from collections import deque
from websockets.asyncio.server import broadcast
from websockets.asyncio.server import serve
import websockets

CONNECTIONS = set()
IMAGE_SENDERS = set()
LAST_MESSAGES = deque(maxlen=10)

async def handle(websocket):
    if websocket not in CONNECTIONS:
        CONNECTIONS.add(websocket)
        await websocket.send(json.dumps({"op": 10, "messages": list(LAST_MESSAGES)}))
    async for msg in websocket:
        ip = ""
        try:
            ip = websocket.request.headers["CF-Connecting-IP"]
        except:
            ip = websocket.remote_address[0]
        thing = {}
        try:
            thing = json.loads(msg)
            print(thing)
            
        except:
            try:
                print(websocket.request.headers["CF-Connecting-IP"] + " was killed")
            except:
                print(websocket.remote_address[0] + " was killed")
            await websocket.close()
            return
        role = 0
        try:
            if thing["key"] == "tLsnvkTS8YwYmZZcT3vG9vRUbPa4I4EBdodz7GjFB5qVY6u1uIvn8puaa941pP1Oa5cp3Ci":
                role = 2
            if thing["key"] == "98XtT1h21Kygbo40Y8hzCad3Nxgis6mUJgyaKNNRCQZNSY0oS0TCJedCCsauuUVQd273p6e":
                role = 12
            if thing["key"] == "AU8aFcU2U5s4KsMztGjvWKhtgT2PeTioaJLBiX1fEintB7BvrkvX3Kw5GogaHCjhatBYQk7":
                role = 3
        except:
            a = 1
        # Extract user, role, and content from the message
        user = thing.get("username", "")
        content = thing.get("content", "")
        # Store the message in the deque
        LAST_MESSAGES.append({"user": user, "content": content, "role": role})
        message = thing["content"]
        if "193.140.169.144" in ip:
            continue
        if "nigg" in message:
            broadcast(CONNECTIONS, json.dumps({
                "content": f"{websocket.request.headers["CF-Connecting-IP"]} said nword, laugh at this user",
                "username": "System",
                "role": 2
            }))
            return
        if len(message) > 600:
            return
        if len(thing["username"]) > 30:
            return
        message = message.replace("onclick", "**").replace("onmouseover", "**").replace("onmouseout", "**").replace("onload", "").replace("onerror", "").replace("onerror", "").replace("oncontextmenu", "")
        if message == "bad" or message == "" or "https://tiramisu.gay/devilbro.html" in message or thing["username"] == "":
            continue
        try:
            if websocket.request.headers["CF-Connecting-IP"] in IMAGE_SENDERS:
                role = 1
        except:
            if websocket.remote_address[0] in IMAGE_SENDERS:
                role = 1
        try:
            print(websocket.request.headers["CF-Connecting-IP"] + " said: \n> " + message)
        except:
            print(websocket.remote_address[0] + " said: \n> " + message)
        # Check if the message is identical to the 3 latest messages
        if len(LAST_MESSAGES) >= 3 and all(msg["content"] == message for msg in list(LAST_MESSAGES)[-3:]):
            try:
                print(websocket.request.headers["CF-Connecting-IP"] + " was killed for spamming")
            except:
                print(websocket.remote_address[0] + " was killed for spamming")
            await websocket.close()
            broadcast(CONNECTIONS, json.dumps({
            "content": "killed client above. please do not spam",
            "username": "System",
            "role": 2
            }))
            return
        broadcast(CONNECTIONS, json.dumps({
            "content": message,
            "username": thing["username"].replace("<", "&lt;"),
            "role": role
        }))


async def main():
    async with serve(handle, host="0.0.0.0", port=8765):
        await asyncio.get_running_loop().create_future()


asyncio.run(main())
