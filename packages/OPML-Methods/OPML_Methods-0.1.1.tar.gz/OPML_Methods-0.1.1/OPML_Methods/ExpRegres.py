# n - кол-во строк
# m - кол-во столбцов
from sympy import *
import re
import numpy as np
import math
import matplotlib.pyplot as plt
import numexpr as ne
from .AdjGrad import *
from .brent import *

class ExpRegres:
    def find(self, y, x, n, m, reg, L, sigma):
        
        """
        Реализует модель экспоненциалной регрессии 3 видами регуляторов: L1, L2 и Стьюдента.
        
        Parameters
        ===========
        :param y: np.array
            массив предсказываемых данных 
        :param x: list
            массив предикатов X
        :param n: int
            кол-во строк в матрице
        :param m: int
            кол-во столбцов в матрице
        :param deg: int
            степень полинома
        :param reg: str
            параметр, отвечающий за вид регуляризации
        :param L: int
            коэффициент регуляции
        :param sigma: int
            стандартное отклонение остатков
        :return:
            Возвращает вектор модельных предсказанных данных, массив коэффициентов регрессии, 
            свободный член, функция в аналитическом виде.
        """

        X = 'x1'
        for i in range(m):
            X = X + " " + f'x{i + 2}'

        m = m + 1

        ey = np.ones((len(x), 1))
        x = np.array(x)
        x = np.concatenate((ey, x), axis=1)


        if reg == 'None':

            omega = np.array([list(symbols(X))])
            loss_function = (1 / (2 * n)) * sum((y - np.dot(x, omega.transpose())) ** 2)

        elif reg == 'L1':

            omega = np.array([list(symbols(X))])
            loss_function = (1 / (2 * n)) * sum((y - np.dot(x, omega.transpose())) ** 2) + L * (omega ** 2 / 2).sum()

        elif reg == 'L2':
            omega = np.array([list(symbols(X))])
            loss_function = (1 / (2 * n)) * sum((y - np.dot(x, omega.transpose())) ** 2) + L * sum(omega ** 2)

        elif reg == 'norm':
            omega = np.array([list(symbols(X))])
            loss_function = (1 / (2 * n)) * sum((y - np.dot(x, omega.transpose())) ** 2) + (1 / (2 * sigma)) * sum(
                omega ** 2)

        func = AdjGrad()
        omega_point = [0 for i in range(m)]
        omega_min = func.find(str(loss_function[0]), omega_point, 0.00001, 0, 0, 0)

        for i in range(len(omega_min)):
            omega_min[i] = math.e ** omega_min[i]
        #print(omega_min)
        y = []

        for i in range(n):
            y_om = omega_min[0]
            for j in range(1, m):
                y_om = y_om * (omega_min[j]**x[i][j])
            y.append(y_om)

        print(f'Вектор модельных предсказанных данных: {y}')
        print(f'Массив коэффициентов регрессии: {omega_min[1:]}') 
        print(f'Свободный член: {omega_min[0]}') 
        y_str = str(omega_min[0]) 
        for i in range(1, len(omega_min)):
            y_str = y_str + f' * {omega_min[i]}**{list(symbols(X))[i - 1]}' 
        print(f'Функция в аналитическом виде: y^={y_str}')
        
        if (len(omega_min) - 1) == 1:
            fig, ax = plt.subplots(figsize=(10, 10))

            ax.set_title('Экспоненциальная регрессия', loc='left', fontweight='bold')
            ax.set_title(f'y^ = {y_str}', loc='right')
            ax.set_ylabel('y^')
            ax.set_xlabel('x1')

            x1 = np.linspace(-10, 10, 50)
            y = ne.evaluate(y_str)

            plt.plot(x1, y, color='b')
            x1 = Symbol('x1')
            for i in range(len(x)):
                ax.scatter(x[i][1], sympify(y_str).subs(x1, x[i][1]), c='r')

            plt.show()

        elif (len(omega_min) - 1) == 2:
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(projection='3d')
            ax.set_title(f'y^ = {y_str}', loc='right')
            ax.set_zlabel('y^')
            ax.set_ylabel('x2')
            ax.set_xlabel('x1')

            x1 = np.linspace(np.min(x), np.max(x), 25)
            x2 = np.linspace(np.min(x), np.max(x), 25)
            x1, x2 = np.meshgrid(x1, x2)
            y = ne.evaluate(y_str)

            surf = ax.plot_surface(x1, x2, y, cmap='viridis', shade=True, alpha=0.5)
            fig.colorbar(surf, shrink=0.5, aspect=10)
            x1, x2 = symbols('x1 x2')
            for i in range(len(x)):
                ax.scatter(x[i][1], x[i][2], sympify(y_str).subs([(x1, x[i][1]), (x2, x[i][2])]), c='r')

            plt.show()


#functionss = ExpRegres()
#functionss.find(np.array([math.log1p(5), math.log1p(2), math.log1p(2), math.log1p(5)]).reshape(-1, 1), [[2, 1], [1, 1], [1, 3], [3, 5]], 4, 2, 'L1', 0.95, 0.1)

# functionss = ExpRegres()
# functionss.find(np.array([1, 1, 1]).reshape(-1, 1), [[0, 1, 1], [-1, 1, 1], [-1, 1, 1]], 3, 3, 'None', 0.95, 0.1)

# y = []
# print("Введите кол-во строк в матрице(n). Например 3")
# n = int(input())
# print("Введите кол-во столбцов в матрице(n). Например 3")
# m = int(input())
# print("Введите массив предсказываемых данных y = (y1, y2, ..., yn)")
# for i in range(n):
#   print(f'Введите {i} значение. Например 1')
#   y.append(math.log1p(float(input())))
# print("Введите массив предикантов X размерностью n x m")
# X = []
# for i in range(n):
#   xij = []
#   for j in range(m):
#       print(f'Введите x{i, j}')
#       xij.append(float(input()))
#   X.append(xij)
#
# L = 0.95
# sigma = 0.1
# print("Хотите ввести параметр, отвечающий за вид регуляризации? 1 - да / 0 - нет")
# q = -1
# while q < 0 or q > 1:
#    q = int(input())
#    if q < 0 or q > 1:
#        print("Неправильный ввод. 1 - да / 0 - нет")
#
# if q == 1:
#    print("Введите L1, или L2, или norm ")
#    reg = 'j'
#    while reg != "L1" and reg != "L2" and reg != "norm":
#        reg = input()
#        if reg != "L1" and reg != "L2" and reg != "norm":
#            print("Такой комманды нет. Введите снова. L1, или L2, или norm")
#
#    if reg == "L1" or reg == "L2":
#        print("Введите коэффициент регуляции. Например 0.95. Значение должно быть >=0. (чем больше, тем сильнее регуляризация)")
#        L = -1
#        while L < 0 or L > 1:
#            L = float(input())
#            if L < 0 or L > 1:
#                print("Некорректно введен коэффициент регуляции. Значение должно быть >=0.")
#
#    elif reg == "norm":
#        print("Введите предполагаемое стандартное отклонение остатков. Например 0.1. Значение должно быть >=0 и <=1. (чем больше, тем слабее регуляризация)")
#        sigma = -1
#        while sigma < 0 or sigma > 1:
#            sigma = float(input())
#            if sigma < 0 or sigma > 1:
#                print("Некорректно введено предполагаемое стандартное отклонение остатков. Значение должно быть >=0 и <=1.")
# elif q == 0:
#    reg = 'None'

# functionss = ExpRegres()
# functionss.find(np.array(y).reshape(-1, 1), X, n, m, reg, L, sigma)
