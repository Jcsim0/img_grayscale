# -*- coding: utf-8 -*-
"""
Created with：PyCharm
@Author： Jcsim
@Date： 2021-5-31 16:54
@Project： grayscale
@File： routing.py
@Description： 
@Python：
"""
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application

# django_asgi_app = get_asgi_application()
import image_detection.websocket_routing

application = ProtocolTypeRouter({
    # "http": django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            image_detection.websocket_routing.websocket_urlpatterns
        )
    ),
})
