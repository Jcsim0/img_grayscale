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
import time
import traceback
from time import sleep

import bluetooth
from channels.generic.websocket import WebsocketConsumer
import json

from django.http import JsonResponse

from image_detection.log import logger
from image_detection.utils import DateUtil


class BtConnectConsumers(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sock = None

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        print("clossssssssssssssssssssss")
        pass

    def receive(self, text_data):
        try:
            # 这里是接受数据后的操作，下面的方法按需修改
            text_data_json = json.loads(text_data)
            code_ = text_data_json.get("code", None)
            # print("=================================================================",self.sock)
            # sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            try:
                print("==========={}:code={}=========".format(DateUtil.get_now_datetime(), code_))
                if code_ == "10":
                    if self.sock:
                        self.sock.close()
                        # self.close()
                        # self.sock = None
                    self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                    bt_name = text_data_json.get("bt_name", None)
                    bt_addr = text_data_json.get("bt_addr", None)
                    if not bt_addr:
                        return JsonResponse({"status": 201, "msg": "请选择需要连接的蓝牙设备", "data": None},
                                            json_dumps_params={'ensure_ascii': False})
                    logger.info(
                        "===============【{}】准备连接目标设备：设备名【{}】，地址【{}】。===============".format(DateUtil.get_now_datetime(),
                                                                                            bt_name, bt_addr))
                    self.sock.connect((bt_addr, 1))
                    data = {
                            "status": 200,
                            "msg": "连接成功"
                        }
                    self.send(text_data=json.dumps(data))
                    logger.info(
                        "===============【{}】连接目标设备成功。准备接受数据!===============".format(DateUtil.get_now_datetime()))
                # 以下代码根据需求更改
                if self.sock and (code_ == "0" or code_ == "1" or code_ == "2"):
                    logger.info(
                        "===============【{}】准备发送数据：{}===============".format(DateUtil.get_now_datetime(), code_))
                    self.sock.send(code_)
                    data_dtr = ""
                    while True:
                        data = self.sock.recv(1024)
                        # print(data)
                        data_dtr += data.decode()
                        if '\n' in data.decode():
                            # data_dtr[:-2] 截断"\t\n",只输出数据
                            # print(datetime.datetime.now().strftime("%H:%M:%S") + "->" + data_dtr[:-2])
                            self.send(text_data=json.dumps(data_dtr[:-2]))
                            break
                if self.sock and code_ == 20:
                    logger.info(
                        "===============【{}】 准备断开连接!===============".format(DateUtil.get_now_datetime()))
                    self.sock.close()
                    self.close()
            except Exception as e:
                traceback.print_exc()
                logger.info(
                    "===============【{}】连接目标失败，请重新连接。===============".format(DateUtil.get_now_datetime()))
                self.sock.close()
                self.close()
                return JsonResponse({"status": 202, "msg": "连接目标失败，请重新连接", "data": None},
                                    json_dumps_params={'ensure_ascii': False})
        except Exception:
            traceback.print_exc()
            return JsonResponse({"status": 500, "msg": "异常!", "errMsg": traceback.format_exc()},
                                json_dumps_params={'ensure_ascii': False})
