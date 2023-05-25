from django.urls import path
from . import ImageConsumers

# 웹소켓 요청이 들어오면 consumers로 연결
websocket_urlpatterns = [
    path('ws/socket_server', ImageConsumers.Consumers.as_asgi())
]
