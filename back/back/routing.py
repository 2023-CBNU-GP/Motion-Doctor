from channels.routing import ProtocolTypeRouter, URLRouter
import image_socket.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': URLRouter(
        image_socket.routing.websocket_urlpatterns
    )
})