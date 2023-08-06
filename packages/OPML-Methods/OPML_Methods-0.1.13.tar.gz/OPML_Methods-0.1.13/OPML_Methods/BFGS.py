import sympy
from sympy import *
import numpy as np


class BFGS:
    def find(z, Xl, Xu, Yl, Yu, point_for_start, e, iter):
        """
        Функция находит экстремум функции с помощью Алгоритма Бройдена — Флетчера — Гольдфарба — Шанно.
        Parameters
        ===========
        :param z: str
            строковая функция f(x)
        :param Xl: float
            интервал "от" по х
        :param Xu: float
            интервал "до" по х
        :param Yl: float
            интервал "от" по y
        :param Yu: float
            интервал "до" по y
        :param point_for_start: float
            точка старта
        :param e: float
            эпсилон - точность исследования
        :param flag: int
            если 1 то промежуточные расчеты выводятся если 0 то нет
        :param iter: int
            количество итераций
        Returns
        ===========
        экстремум функции
        """

        func = sympify(z)
        x, y, alpha = symbols('x y alpha')
        grad = [func.diff(x), func.diff(y)]

        i = 0
        while i < iter:
            grad_xk = np.array([[grad[0].subs([(x, point_for_start[0][0]), (y, point_for_start[1][0])])],
                                [grad[1].subs([(x, point_for_start[0][0]), (y, point_for_start[1][0])])]])

            sqrt_func = (grad_xk[0][0] ** 2 + grad_xk[1][0] ** 2) ** (1 / 2)

            if abs(sqrt_func) > e:
                I = np.array([[1, 0], [0, 1]])
                if i == 0:
                    H0 = I
                else:
                    I = H1

                p0 = -I.dot(grad_xk)

                matrix_with_alpha = point_for_start + alpha * p0

                f = func.subs([(x, matrix_with_alpha[0][0]), (y, matrix_with_alpha[1][0])])
                a = float(solve((f.diff(alpha), alpha)[0])[0])
                point_next = point_for_start + a * p0
                s0 = point_next - point_for_start

                grad_xk_1 = np.array([[grad[0].subs([(x, point_next[0][0]), (y, point_next[1][0])])],
                                      [grad[1].subs([(x, point_next[0][0]), (y, point_next[1][0])])]])

                y0 = grad_xk_1 - grad_xk

                k = 1 / np.dot(y0.transpose(), s0)

                A1 = I - k * (s0 * y0.transpose())
                A2 = I - k * (y0 * s0.transpose())

                H1 = np.dot(A1, np.dot(H0, A2)) + k * np.dot(s0, s0.transpose())

                point_for_start = point_next
                H0 = H1


            else:
                if (Xl <= point_for_start[0][0] <= Xu) and (Yl <= point_for_start[1][0] <= Yu):
                    print((point_for_start[0][0], point_for_start[1][0]))
                else:
                    print("Экстремум min не найден")
                break

            i += 1
