# -*- coding: utf-8 -*-
"""
Created with：PyCharm
@Author： Jcsim
@Date： 2021-5-31 17:11
@Project： grayscale
@File： websocket_routing.py
@Description： 
@Python：
"""
from django.urls import path

# 建议url前缀使用 ws/xxx 用于区分ws请求和http请求
from image_detection.websocket_consumers import BtConnectConsumers

websocket_urlpatterns = [
    path('ws/bt/connect', BtConnectConsumers),
    # path('ws/asqosws/<tradeNo>', AsyncOrderStatusConsumers.as_asgi()),
]
