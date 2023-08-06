import numpy as np
import sympy
from sympy import *
import time
from .GoldenSection import *
import matplotlib.pyplot as plt
import numexpr as ne
import matplotlib.animation as animation


class PorabolMet:
    def find(z, Xl, Xu, e, flag, iter):
        """
        Функция находит экстремум функции одной переменной методом парабол.
        Parameters
        ===========
        :param z: str
            строковая функция
        :param Xl: float
            интервал "от" по х
        :param Xu: float
            интервал "до" по х
        :param e: float
            эпсилон - точность исследования
        :param flag: int
            если 1 то промежуточные расчеты выводятся если 0 то нет
        :param iter: int
            количество итерация
        Returns
        ===========
        экстремум функции и график с движением точек
        """
        x1, x3 = Xl, Xu
        func = sympify(z)
        x = Symbol('x')
        x2 = GoldenSection.find(z, x1, x3, e, 500, 'False', iter)
        x2 = x2.x_min
        lst_x_ = []
        i = 0
        if flag == 1:
            print(f'промежуточное значение х:')
        while i <= iter:
            if x1 < x2 < x3:
                func1 = float(func.subs(x, x1))
                func2 = float(func.subs(x, x2))
                func3 = float(func.subs(x, x3))

                if (func1 >= func2 <= func3 and i == 0) or i != 0:
                    a1 = (func2 - func1) / (x2 - x1)
                    a2 = (1 / (x3 - x2)) * (((func3 - func1) / (x3 - x1)) - ((func2 - func1) / (x2 - x1)))
                    x_ = (1 / 2) * (x1 + x2 - a1 / a2)
                    lst_x_.append(x_)
                    if flag == 1:
                        print(x_)
                    if x_ > x2:
                        x1 = x2
                        x2 = x_
                    elif x1 < x_ < x2:
                        x1 = x_

                    if i > 0:
                        if abs(lst_x_[i - 1] - lst_x_[i]) < e:
                            x_min = x_
                            print(f'Минимальное значение: {x_min:>.3f}')
                            break

            i += 1

        fig, ax = plt.subplots()

        ax.set_title('Поиск экстремумов')

        x = np.linspace(Xl, Xu, 50)
        y = ne.evaluate(z)

        plt.plot(x, y, color='b')

        redDot, = plt.plot([], [], 'ro')
        blueDot, = plt.plot([], [], 'bo')

        def animate(x):
            redDot.set_data(x, ne.evaluate(z))
            blueDot.set_data(x, ne.evaluate(z))

            return redDot, blueDot,

        # create animation using the animate() function
        myAnimation = animation.FuncAnimation(fig, animate, frames=np.linspace([Xl, Xu], x_min, 100),
                                              interval=10, blit=True, repeat=False)

        plt.show()
# print("Введите функцию f(x, y). Например:  -5*x**5 + 4*x**4 - 12* x**3 + 11*x**2 - 2*x - 1")
# f = "-3*x*sin(0.75*x) + exp(-2*x)"
# print("Введите левое ограничение по x. Например: 0")
# Xl = 0
# print("Введите правое ограничение по x. Например: 6")
# Xu = 6
# print("Введите e. Например: 0.001")
# e = 0.001
# ea = 100
# flag = 'False'
# print("Введите кол-во итераций. Например: 10")
# iter = 500
# functions = PorabolMet()
# functions.find(f, Xl, Xu, e, flag, iter)
