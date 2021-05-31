# -*- coding: utf-8 -*-
"""
Created with：PyCharm
@Author： Jcsim
@Date： 2021-5-31 17:12
@Project： grayscale
@File： websocket_consumers.py
@Description： 
@Python：
"""
import datetime
import traceback

import bluetooth
from channels.generic.websocket import WebsocketConsumer
import json

from django.http import JsonResponse

from image_detection.log import logger
from image_detection.utils import DateUtil


class BtConnectConsumers(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        try:
            # 这里是接受数据后的操作，下面的方法按需修改
            text_data_json = json.loads(text_data)
            # trade_no = text_data_json['tradeNo']
            bt_name = text_data_json.get("bt_name", None)
            bt_addr = text_data_json.get("bt_addr", None)
            if not bt_name or not bt_addr:
                return JsonResponse({"status": 201, "msg": "请选择需要连接的蓝牙设备", "data": None},
                                    json_dumps_params={'ensure_ascii': False})
            logger.info(
                "===============【{}】准备连接目标设备：设备名【{}】，地址【{}】。===============".format(DateUtil.get_now_datetime(),
                                                                                    bt_name, bt_addr))

            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            try:
                sock.connect((bt_addr, 1))
                logger.info(
                    "===============【{}】连接目标设备成功。准备接受数据!===============".format(DateUtil.get_now_datetime()))
                data_dtr = ""
                # 以下代码根据需求更改
                while True:
                    data = sock.recv(1024)
                    data_dtr += data.decode()
                    if '\n' in data.decode():
                        # data_dtr[:-2] 截断"\t\n",只输出数据
                        print(datetime.datetime.now().strftime("%H:%M:%S") + "->" + data_dtr[:-2])
                        data_dtr = ""
            except Exception as e:
                traceback.print_exc()
                logger.info(
                    "===============【{}】连接目标失败，请重新连接。===============".format(DateUtil.get_now_datetime()))
                connect = False
                sock.close()
                return JsonResponse({"status": 202, "msg": "连接目标失败，请重新连接", "data": None},
                                    json_dumps_params={'ensure_ascii': False})
        except Exception:
            traceback.print_exc()
            return JsonResponse({"status": 500, "msg": "异常!", "errMsg": traceback.format_exc()},
                                json_dumps_params={'ensure_ascii': False})

        # stop = False
        # status = 201
        # password = "******"
        #
        # data = {
        #     "status": status,
        #     "password": password
        # }
        # # 推送信息到前端
        # self.send(text_data=json.dumps(data))
        # # 我项目ws推送的结束逻辑
        # if stop:
        #     self.close()
