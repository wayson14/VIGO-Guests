from django.urls import path
from .consumers import WSConsumer


ws_urlpatterns = [
    path("wss/socket_connection/", WSConsumer.as_asgi())
]