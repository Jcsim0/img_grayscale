from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
import io
import traceback

import cv2
import numpy as np
from django.views import View
from django.views.decorators.csrf import csrf_exempt


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
