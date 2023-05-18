from channels.routing import ProtocolTypeRouter, URLRouter
import image_socket.routing
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            image_socket.routing.websocket_urlpatterns
        )
    ),
})