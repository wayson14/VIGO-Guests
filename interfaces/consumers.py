from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asyncio import sleep


class WSConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("\n\n\ntry\n\n\n")
        await self.accept()
        await self.send(text_data=json.dumps({
            "type": "connection_established",
            "message": "You are now connected"
        }))
        for i in range(100):
            await self.send(json.dumps({"message": "refresh"}))
            await sleep(1)