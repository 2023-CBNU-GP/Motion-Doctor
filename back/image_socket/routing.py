from django.urls import path
from back.image_socket import consumers

# 웹소켓 요청이 들어오면 consumers로 연결
websocket_urlpatterns = [
    path('/ws/socket_server', consumers.Consumers.as_asgi())
]
