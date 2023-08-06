import sympy
import time
import math
from sympy import *


class BrentMet:

    def PoiskVershin(x1, y1, x2, y2, x3, y3):
        denom = (x1 - x2) * (x1 - x3) * (x2 - x3)
        a1 = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / denom
        b1 = (x3 * x3 * (y1 - y2) + x2 * x2 * (y3 - y1) + x1 * x1 * (y2 - y3)) / denom
        c1 = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / denom
        xv = -b1 / (2 * a1)
        # yv = c1 - b1 * b1 / (4 * a1)
        return xv

    def find(y, a, b, eps, iterations):
        func = sympify(y)
        x = Symbol('x')
        r = (3 - 5 ** (1 / 2)) / 2
        xx = a + r * (b - a)
        w = a + r * (b - a)
        v = a + r * (b - a)
        d_cur = b - a
        d_prv = b - a
        i = 0
        ii = 0
        while i < iterations:
            i += 1
            #print(abs(xx - a), abs(b - xx), max(abs(xx - a), abs(b - xx)))
            if max(abs(xx - a), abs(b - xx)) < eps:
                ii += 1
                #print(f'Найденное решение: x = {float(xx):>.4f} , y = {func.subs(x, xx)} за {i} шагов')
                return float(xx)
            g = d_prv / 2
            d_prv = d_cur
            u = BrentMet.PoiskVershin(xx, func.subs(x, xx), w, func.subs(x, w), v, func.subs(x, v))
            # print(f'{float(u):>.8f}')

            if u == zoo:
                u = nan

            if u == nan:
                if xx < (a + b) / 2:
                    u = xx + r * (b - xx)
                    d_prv = b - xx
                else:
                    u = xx - r * (xx - a)
                    d_prv = xx - a
            elif ((a > u) and (u > b)) or (abs(u - xx) > g):
                if xx < (a + b) / 2:
                    u = xx + r * (b - xx)
                    d_prv = b - xx
                else:
                    u = xx - r * (xx - a)
                    d_prv = xx - a

            d_cur = abs(u - xx)
            #x33 = func.subs(x, u)
            # print(simplify(sympify(x33)))
            # print(float(func.subs(x, u)), 111)
            #print(func.subs(x, u))
            #print(func.subs(x, xx))
            if float(func.subs(x, u)) > float(func.subs(x, xx)):
                if u > xx:
                    a = u
                else:
                    b = u
                if float(func.subs(x, u)) <= float(func.subs(x, w)) or (w == xx):
                    v = w
                    w = u
                elif float(func.subs(x, u)) <= float(func.subs(x, v)) or v == xx or v == w:
                    v = u
            else:
                if u < xx:
                    b = xx
                else:
                    a = xx
                v = w
                w = xx
                xx = u
        if ii != 1:
            #print(f'Найдено неточное значение: x = {xx}')
            return float(xx)
            #function3 = BrentMet()
            #function3.find(y, int(xx)-a/3, int(xx)+b/3, 0.001, 100)