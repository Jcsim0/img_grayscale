import datetime
import json

import bluetooth
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
import io
import traceback

import cv2
import numpy as np
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from sklearn.linear_model import LinearRegression

from image_detection import least_square
from image_detection.bluetoothUtil import BluetoothConnection
from image_detection.log import logger
from image_detection.utils import DateUtil


class ImgGrayscale:

    @staticmethod
    def concentration(y):
        """
        求浓度值
        :param y: 灰度图像的平均灰度
        :return: 浓度
        """
        c = 10 ** ((y - 122.02005) / 7.69789)
        return c

    @staticmethod
    def center_crop(im, w, h):
        """
        对图片进行中心裁剪
        :param im: 图片
        :param w: 想要裁剪的宽度
        :param h: 想要裁剪的高度
        :return: 裁剪后的图片
        """

        # 根据中心点计算起始坐标
        start_x = int(im.shape[1] / 2) - int(w / 2)
        start_y = int(im.shape[0] / 2) - int(h / 2)
        # 切片
        new_img = im[start_y:start_y + h, start_x:start_x + w]
        return new_img


def get_arguments(request):
    """
    获取请求参数
    :param request:
    :return:
    """
    if request.method == 'GET':
        logger.info("收到GET请求")
        arguments = dict(request.GET)
        for arg in arguments:
            if type(arguments[arg]) == type([]):
                arguments[arg] = arguments[arg][0]
    else:
        logger.info("收到POST请求")
        logger.info("post-body")
        logger.info(request.body.decode())
        if "form" in request.content_type:
            arguments = request.POST
        else:
            arguments = json.loads(request.body.decode())
    return arguments


class WebImgGrayscale(View):
    """
    get: 通过图片灰度获取浓度
    """

    @staticmethod
    @csrf_exempt
    def post(request):
        try:
            file = request.FILES["file"]
            if not file:
                return JsonResponse({"status": 201, "msg": "请上传图片", "data": None},
                                    json_dumps_params={'ensure_ascii': False})
            file_img = file.file.read()
            # cv2读取字节流数据
            cv_img = cv2.imdecode(np.frombuffer(file_img, np.uint8), 0)
            cut_img = ImgGrayscale.center_crop(cv_img, int(cv_img.shape[1] * 0.8), int(cv_img.shape[0] * 0.8))
            mean, std = cv2.meanStdDev(cut_img)
            value_mean = mean[0, 0]
            concentration = ImgGrayscale.concentration(value_mean)
            data = {
                "value_mean": value_mean,
                "concentration": format(concentration, '.5f')
            }
            return JsonResponse({"status": 200, "msg": "success", "data": data},
                                json_dumps_params={'ensure_ascii': False})
        except Exception:
            traceback.print_exc()
            return JsonResponse({"status": 500, "msg": "异常!", "errMsg": traceback.format_exc()},
                                json_dumps_params={'ensure_ascii': False})


def get_concentration_by_least_square(request):
    try:

        file1 = request.FILES["file1"]
        file2 = request.FILES["file2"]
        file3 = request.FILES["file3"]
        file4 = request.FILES["file4"]
        file5 = request.FILES["file5"]
        file6 = request.FILES["file6"]
        file7 = request.FILES["file7"]
        file8 = request.FILES["file8"]

        # arguments = arguments = get_arguments(request)
        # img1_con = arguments.get("img1_con", None)
        # img2_con = arguments.get("img2_con", None)
        # img3_con = arguments.get("img3_con", None)
        # img4_con = arguments.get("img4_con", None)
        # img5_con = arguments.get("img5_con", None)
        # img6_con = arguments.get("img6_con", None)
        # img7_con = arguments.get("img7_con", None)
        img1_con = 0
        img2_con = 0.5
        img3_con = 1
        img4_con = 2.5
        img5_con = 5
        img6_con = 7.5
        img7_con = 10

        if not file1 or not file2 or not file3 or not file4 or not file5 or not file6 or not file7 or not file8:
            return JsonResponse({"status": 201, "msg": "请上传图片", "data": None},
                                json_dumps_params={'ensure_ascii': False})
        # if not img1_con or not img2_con or not img3_con or not img4_con or not img5_con or not img6_con or not img7_con:
        #     return JsonResponse({"status": 202, "msg": "请上传前七张图片的浓度", "data": None},
        #                         json_dumps_params={'ensure_ascii': False})
        file_img1 = file1.file.read()
        file_img2 = file2.file.read()
        file_img3 = file3.file.read()
        file_img4 = file4.file.read()
        file_img5 = file5.file.read()
        file_img6 = file6.file.read()
        file_img7 = file7.file.read()
        file_img8 = file8.file.read()

        # cv2读取字节流数据
        cv_img1 = cv2.imdecode(np.frombuffer(file_img1, np.uint8), 0)
        cut_img1 = ImgGrayscale.center_crop(cv_img1, int(cv_img1.shape[1] * 0.8), int(cv_img1.shape[0] * 0.8))
        mean1, std = cv2.meanStdDev(cut_img1)
        value_mean1 = mean1[0, 0]  # 图片灰度

        cv_img2 = cv2.imdecode(np.frombuffer(file_img2, np.uint8), 0)
        cut_img2 = ImgGrayscale.center_crop(cv_img2, int(cv_img2.shape[1] * 0.8), int(cv_img2.shape[0] * 0.8))
        mean2, std = cv2.meanStdDev(cut_img2)
        value_mean2 = mean2[0, 0]

        cv_img3 = cv2.imdecode(np.frombuffer(file_img3, np.uint8), 0)
        cut_img3 = ImgGrayscale.center_crop(cv_img3, int(cv_img3.shape[1] * 0.8), int(cv_img3.shape[0] * 0.8))
        mean3, std = cv2.meanStdDev(cut_img3)
        value_mean3 = mean3[0, 0]

        cv_img4 = cv2.imdecode(np.frombuffer(file_img4, np.uint8), 0)
        cut_img4 = ImgGrayscale.center_crop(cv_img4, int(cv_img4.shape[1] * 0.8), int(cv_img4.shape[0] * 0.8))
        mean4, std = cv2.meanStdDev(cut_img4)
        value_mean4 = mean4[0, 0]

        cv_img5 = cv2.imdecode(np.frombuffer(file_img5, np.uint8), 0)
        cut_img5 = ImgGrayscale.center_crop(cv_img5, int(cv_img5.shape[1] * 0.8), int(cv_img5.shape[0] * 0.8))
        mean5, std = cv2.meanStdDev(cut_img5)
        value_mean5 = mean5[0, 0]

        cv_img6 = cv2.imdecode(np.frombuffer(file_img6, np.uint8), 0)
        cut_img6 = ImgGrayscale.center_crop(cv_img6, int(cv_img6.shape[1] * 0.8), int(cv_img6.shape[0] * 0.8))
        mean6, std = cv2.meanStdDev(cut_img6)
        value_mean6 = mean6[0, 0]

        cv_img7 = cv2.imdecode(np.frombuffer(file_img7, np.uint8), 0)
        cut_img7 = ImgGrayscale.center_crop(cv_img7, int(cv_img7.shape[1] * 0.8), int(cv_img7.shape[0] * 0.8))
        mean7, std = cv2.meanStdDev(cut_img7)
        value_mean7 = mean7[0, 0]

        cv_img8 = cv2.imdecode(np.frombuffer(file_img8, np.uint8), 0)
        cut_img8 = ImgGrayscale.center_crop(cv_img8, int(cv_img8.shape[1] * 0.8), int(cv_img8.shape[0] * 0.8))
        mean8, std = cv2.meanStdDev(cut_img8)
        value_mean8 = mean8[0, 0]

        x = np.array([[img1_con], [img2_con], [img3_con], [img4_con], [img5_con], [img6_con], [img7_con]])  # 已知浓度
        y = np.array([[value_mean1], [value_mean2], [value_mean3], [value_mean4],
                      [value_mean5], [value_mean6], [value_mean7]])  # 根据图片求灰度

        # plt.plot(x, y, 'k.')

        features = x.reshape(-1, 1)
        target = y

        regression = LinearRegression()
        model = regression.fit(features, target)

        # model为已知直线（浓度与灰度的直线方程）。
        # 现给出直线上的点（x2[1], y2[1]） (x2[2], y2[2]) 得出斜率，再通过least_square.func，给定灰度，求浓度
        x2 = np.array([[0], [0.15], [0.25], [0.45], [0.7]])
        y2 = model.predict(x2)

        x_pre = least_square.func(x2[1], y2[1], x2[2], y2[2], value_mean8)

        return JsonResponse({"status": 200, "msg": "success", "data": format(x_pre[0], '.5f')},
                            json_dumps_params={'ensure_ascii': False})
    except Exception:
        traceback.print_exc()
        return JsonResponse({"status": 500, "msg": "异常!", "errMsg": traceback.format_exc()},
                            json_dumps_params={'ensure_ascii': False})


def search_bt(request):
    b = BluetoothConnection()
    b.find_nearby_devices()
    data = []
    if b.nearby_devices:
        for addr, name in b.nearby_devices:
            bt = {
                "bt_name": name,
                "bt_addr": addr
            }
            data.append(bt)
    return JsonResponse({"status": 200, "msg": "success", "data": data},
                        json_dumps_params={'ensure_ascii': False})


def connect_bt(request):
    try:
        arguments = get_arguments(request)
        bt_name = arguments.get("bt_name", None)
        bt_addr = arguments.get("bt_addr", None)
        if not bt_name or not bt_addr:
            return JsonResponse({"status": 201, "msg": "请选择需要连接的蓝牙设备", "data": None},
                                json_dumps_params={'ensure_ascii': False})
        logger.info(
            "===============【{}】准备连接目标设备：设备名【{}】，地址【{}】。===============".format(DateUtil.get_now_datetime(), bt_name, bt_addr))

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
                    print(datetime.datetime.now().strftime("%H:%M:%S")+"->"+data_dtr[:-2])
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


class ToView(View):
    @staticmethod
    def go_to(request, to):
        return render(request, "pay_info.html")