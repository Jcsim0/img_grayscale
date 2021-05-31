# -*- coding: utf-8 -*-
"""
Created with：PyCharm
@Author： Jcsim
@Date： 2021-5-20 15:22
@Project： grayscale
@File： utils.py
@Description： 
@Python：
"""


# 日期工具类
import datetime


class DateUtil:
    @staticmethod
    def seconds_to_day_hour_minute_second(seconds):
        s = str(seconds)
        if not s.isdigit():
            return "格式错误，请输入整数"
        elif type(seconds) == str:
            seconds = int(seconds)
        day = seconds // 86400
        hour = seconds // 3600 - day * 24
        minute = seconds // 60 - day * 1440 - hour * 60
        sec = seconds - day * 86400 - hour * 3600 - minute * 60
        result = ""
        if day != 0:
            result += str(day) + "天"
        if hour != 0:
            result += str(hour) + "小时"
        if minute != 0:
            result += str(minute) + "分"
        if sec != 0:
            result += str(sec) + "秒"
        if day == 0 and hour == 0 and minute == 0 and sec == 0:
            result = 0
        return result

    @staticmethod
    def get_now_datetime():
        """
        获取当前时间
        :return:
        """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def datetime_string():
        """
        返回时间格式的字符串
        :return:
        """
        return "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def string_datetime(str, time=True):
        """
        日期字符串转为时间格式
        :param str: 日期字符串
        :param time: 是否包括时间
        :return:
        """
        if time:
            return datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
        else:
            return datetime.datetime.strptime(str, "%Y-%m-%d")
