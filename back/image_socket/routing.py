from django.urls import path
from .ImageConsumers import *
from .VideoConsumers import *

# 웹소켓 요청이 들어오면 consumers로 연결
websocket_urlpatterns = [
    path('ws/socket_server', ImageConsumers.as_asgi()),
    path('ws/webcam', VideoConsumers.as_asgi())
]