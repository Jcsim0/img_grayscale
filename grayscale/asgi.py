"""
ASGI config for grayscale project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

# import os
#
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grayscale.settings')
#
# application = get_asgi_application()

import os

import django

from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grayscale.settings')

django.setup()
application = get_default_application()
# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             aliPay.ali_routing.websocket_urlpatterns
#         )
#     ),
# })
