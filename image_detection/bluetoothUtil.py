# -*- coding: utf-8 -*-
"""
Created with：PyCharm
@Author： Jcsim
@Date： 2021-3-17 10:15
@Project： grayscale
@File： bluetoothUtil.py
@Description： 蓝牙工具类
@Python：3.5
"""
import datetime
import time

# win10 安装蓝牙依赖包 https://blog.csdn.net/weixin_38676276/article/details/113027104
import traceback

import bluetooth

from image_detection.log import logger
from image_detection.utils import DateUtil


class BluetoothConnection:
    def __init__(self):
        # 是否找到到设备
        self.find = False
        # 附近蓝牙设备
        self.nearby_devices = None
        # sock
        self.sock = None
        # 是否连接成功
        self.connect = False

    def find_nearby_devices(self):
        logger.info("===============【{}】正在检测附近的蓝牙设备===============".format(DateUtil.get_now_datetime()))
        # print("Detecting nearby Bluetooth devices...")
        # 可传参数 duration--持续时间 lookup-name=true 显示设备名
        # 大概查询10s左右
        # 循环查找次数
        loop_num = 3
        i = 0
        try:
            # print("===============【{}】附近没有蓝牙设备!再次尝试{}===============".format(DateUtil.get_now_datetime(), str(i)))
            self.nearby_devices = bluetooth.discover_devices(lookup_names=True, duration=10)
            # print("===============【{}】附近没有蓝牙设备!再次尝试{}===============".format(DateUtil.get_now_datetime(), str(i)))
            # print(self.nearby_devices)
            while self.nearby_devices.__len__() == 0 and i < loop_num:
                self.nearby_devices = bluetooth.discover_devices(lookup_names=True, duration=10)
                if self.nearby_devices.__len__() > 0:
                    break
                i = i + 1
                time.sleep(2)
                logger.info("===============【{}】附近没有蓝牙设备!再次尝试{}===============".format(DateUtil.get_now_datetime(), str(i)))
            if not self.nearby_devices:
                logger.info(
                    "===============【{}】这附近没有蓝牙设备。程序停止!===============".format(DateUtil.get_now_datetime()))
            else:
                logger.info(
                    "===============【{}】 附近发现【{}】个蓝牙设备：{}===============".format(DateUtil.get_now_datetime(), self.nearby_devices.__len__(), self.nearby_devices))
        except Exception as e:
            # 不知是不是Windows的原因，当附近没有蓝牙设备时，bluetooth.discover_devices会报错。
            traceback.print_exc()
            logger.info(
                "===============【{}】这附近没有蓝牙设备。程序停止(2)!===============".format(DateUtil.get_now_datetime()))

    def find_target_device(self, target_name, target_address):
        self.find_nearby_devices()
        if self.nearby_devices:
            for addr, name in self.nearby_devices:
                if target_name == name and target_address == addr:
                    logger.info(
                        "===============【{}】找到目标蓝牙设备：设备名【{}】，地址【{}】===============".format(DateUtil.get_now_datetime(), target_name, target_address))
                    # print("Found target bluetooth device with address:{} name:{}".format(target_address, target_name))
                    self.find = True
                    break
            if not self.find:
                logger.info(
                    "===============【{}】这附近没有目标蓝牙设备。请打开目标设备的蓝牙。!===============".format(DateUtil.get_now_datetime()))
                # print("could not find target bluetooth device nearby. "
                #       "Please turn on the Bluetooth of the target device.")

    def connect_target_device(self, target_name, target_address):
        # self.find_target_device(target_name=target_name, target_address=target_address)
        self.find = True
        if self.find:
            logger.info(
                "===============【{}】准备连接目标设备：设备名【{}】，地址【{}】。===============".format(DateUtil.get_now_datetime(), target_name, target_address))
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            try:
                self.sock.connect((target_address, 1))
                logger.info(
                    "===============【{}】连接目标设备成功。准备接受数据!===============".format(DateUtil.get_now_datetime()))
                self.connect = True
                data_dtr = ""
                # 以下代码根据需求更改
                # while True:
                #     data = self.sock.recv(1024)
                #     data_dtr += data.decode()
                #     if '\n' in data.decode():
                #         # data_dtr[:-2] 截断"\t\n",只输出数据
                #         print(datetime.datetime.now().strftime("%H:%M:%S")+"->"+data_dtr[:-2])
                #         data_dtr = ""
            except Exception as e:
                traceback.print_exc()
                logger.info(
                    "===============【{}】连接目标失败，请重新连接。===============".format(DateUtil.get_now_datetime()))
                # print("connection fail\n", e)
                self.connect = False
                self.sock.close()
        else:
            logger.info(
                "===============【{}】请先查找设备!===============".format(DateUtil.get_now_datetime()))

    def close_target_device(self):
        # print("Ready to close")
        logger.info(
            "===============【{}】准备与目标设备断开连接。===============".format(DateUtil.get_now_datetime()))
        if self.connect:
            self.sock.close()

    def send_data(self):
        if self.connect:
            self.sock.send("0")
            data = self.sock.recv(1024)
            data_dtr = ""
            while True:
                data_dtr += data.decode()
                if '\n' in data.decode():
                    # data_dtr[:-2] 截断"\t\n",只输出数据
                    print(datetime.datetime.now().strftime("%H:%M:%S")+"->"+data_dtr[:-2])
                    data_dtr = ""
        else:
            print("not connect")


if __name__ == '__main__':
    target_name = "BT04-A"
    target_address = "B4:4B:0E:04:16:25"
    b = BluetoothConnection()
    b.find_nearby_devices()
    # b.connect_target_device(target_name=target_name, target_address=target_address)
