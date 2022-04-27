from channels.generic.websocket import WebsocketConsumer
import json
from asyncio import sleep
import channels.layers
from asgiref.sync import async_to_sync
from django.db import connection



class WSConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None

    def connect(self):
        self.group_name = 'vigo_guests'

        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )

        # async_to_sync(self.channel_layer.group_send)(
        #     self.group_name,
        #     {
        #         'type': 'socket_message',
        #         'message': 'Initial message',
        #     }
        # )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(f'TEXT DATA {text_data_json}')
        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'socket_message',
                'message': message,
            }
        )

    def socket_message(self, event):
        self.send(text_data=json.dumps(event))