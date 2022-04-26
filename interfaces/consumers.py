from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asyncio import sleep

from django.db import connection


class WSConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        print("==============")
        self.channel_name = "stream"
        print(self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({
            "type": "connection_established",
            "message": "You are now connected"
        }))
        connection = True
        while connection:
            await self.send(json.dumps({"message": "keep alive"}))
            await sleep(20)
    
    async def disconnect(self):
        print("==============")
        await self.close()
        await self.send(text_data=json.dumps({
            "type": "connection_closed",
            "message": "Session closed"
        }))
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print(text_data_json)