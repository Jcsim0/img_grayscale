# -*- coding: utf-8 -*-
"""
Created with：PyCharm
@Author： Jcsim
@Date： 2021-4-28 10:54
@Project： grayscale
@File： least_square.py
@Description： 
@Python：
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def func(x1, y1, x2, y2, y):
    """
    求 （x1,y1） (x2,y2) 的直线方程
    结合方程，根据 y(灰度值) 求 x（浓度） 值
    返回 x 值
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :param y:
    :return:
    """
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2
    return (-C - B * y) / A


x = np.array([[0.1], [0.2], [0.3], [0.4], [0.5]])  # 已知浓度
y = np.array([[110], [135], [140], [149], [168]])  # 根据图片求灰度

plt.plot(x, y, 'k.')

features = x.reshape(-1, 1)
target = y

regression = LinearRegression()
model = regression.fit(features, target)

x2 = np.array([[0], [0.15], [0.25], [0.45], [0.7]])
y2 = model.predict(x2)


x_pre = func(x2[1], y2[1], x2[2], y2[2], 141)

print(x_pre)

# plt.plot(x2, y2, 'g-')
# plt.show()

# print(model.intercept_)
#
# print(model.coef_)
#
# print(model.predict([[0.7]]))
